import pandas as pd
import requests
import random
random.seed(0)

from janome.tokenizer import Tokenizer
tokenizer = Tokenizer()

solr_endpoint="http://localhost:8983/solr/fukuoka/select"

# ランダムにtokenに誤変換や脱字を発生させるメソッド
def token_diversificate(token):
    rand = random.random()
    if rand < 0.7:
        return token.surface
    elif rand < 0.80:
        return token.reading
    elif rand < 0.90:
        return token.surface[:len(token.surface)-1]
    else:
        return token.surface[1:]

# queryの一部tokenにtoken_diversificateを適用し、汚いクエリを疑似的に発生させるメソッド
def query_diversificate(query):
    return "".join([token_diversificate(token) for token in tokenizer.tokenize(query)])

# requestsを送ってid2scoreをgetする関数
def get_query2scores(query, field):
    payload = {
        "q":f"{field}:({query})",
        "fl":"id,score",
        "rows":"100"
    }
    r = requests.get(solr_endpoint, params=payload)
    dict_query2scores = r.json()["response"]["docs"]
    return pd.DataFrame.from_dict(dict_query2scores).rename(columns={"score":f"{field}_score"})

def get_query2scores_with_qid(query, field, qid):
    query2scores = get_query2scores(query, field)
    query2scores["qid"] = qid
    return query2scores

# Solrから全件取得することで、idと施設名の対応を取得する
# 今回の例では施設が100件に満たないためrows=100でリクエストを送っている
r = requests.get(solr_endpoint, params={"q":"*:*", "rows":"100"})
dict_all_spots = r.json()["response"]["docs"]
df_all_spots = pd.DataFrame.from_dict(dict_all_spots)

# nameに誤変換や脱字を加えることで揺らしたクエリを作成する
df_all_spots["query"] = df_all_spots["name"].map(query_diversificate)

# 学習時に必要となるリクエストごとの通し番号`qid`を振る
df_all_spots["qid"] = range(len(df_all_spots))

# qidに対する施設のidが正例となるので、ここで結び付けて置く、のちに特徴量テーブルとjoinする
df_query2id_poslabel = df_all_spots[["qid", "id"]].copy()
df_query2id_poslabel["label"]=1

# 各フィールドでのスコアを取得
scores_name = pd.concat([get_query2scores_with_qid(query, "name", qid) for query,qid in zip(df_all_spots["query"], df_all_spots["qid"])])
scores_name_yomi = pd.concat([get_query2scores_with_qid(query, "name_yomi", qid) for query,qid in zip(df_all_spots["query"], df_all_spots["qid"])])
scores_name_ngram  = pd.concat([get_query2scores_with_qid(query, "name_ngram", qid) for query,qid in zip(df_all_spots["query"], df_all_spots["qid"])])

# scoreをjoinする、あるフィールドへの検索で出たがあるフィールドで出なかったアイテムはSolr上でスコア0となるため、outer joinして0埋めしている
scores = scores_name.merge(scores_name_yomi, how="outer", on=["qid", "id"]).merge(scores_name_ngram, how="outer", on=["qid", "id"]).fillna(0)

# qidに対する正解施設IDをjoinし、それ以外の施設はラベルを0埋めする
scores_with_label = scores.merge(df_query2id_poslabel, on=["qid", "id"],how="left").fillna(0)
scores_with_label["label"] = scores_with_label["label"].astype("int")

# pair-wise学習では同じqid内の異なるラベル同士でのスコア差を用いて学習する
# 1つのqidに対して1つのlabelしか結び付いていない場合は学習にも評価にも使用できない
# そのためqid2unique_label_cntが1のデータは除いている
qid2unique_label_cnt = scores_with_label.groupby("qid")["label"].nunique().reset_index()
qid_only_same_label = qid2unique_label_cnt[qid2unique_label_cnt["label"] == 1]["qid"]
scores_dropped_only_same_label = scores_with_label[~scores_with_label["qid"].isin(qid_only_same_label)].sort_values("qid")


# データのうち半分を学習用のtrain・残り半分を精度検証用のtestに分ける。
# 分ける際、同じqidのデータがtrainとtestで混入しないようにしている
train_qid = scores_dropped_only_same_label["qid"].drop_duplicates().sample(frac=0.5, random_state=0)
df_train = scores_dropped_only_same_label[scores_dropped_only_same_label["qid"].isin(train_qid)]
df_test = scores_dropped_only_same_label[~scores_dropped_only_same_label["qid"].isin(train_qid)]

# SVM-rankが前提とする形式に合わせて特徴量を`通し番号:数値`の形式に書き換えている
df_train4svm_rank = df_train[["label"]].copy()
df_train4svm_rank["qid"] = df_train["qid"].map(lambda x:f"qid:{x}")
df_train4svm_rank["name_score"] = df_train["name_score"].map(lambda x:f"1:{x}")
df_train4svm_rank["name_yomi_score"] = df_train["name_yomi_score"].map(lambda x:f"2:{x}")
df_train4svm_rank["name_ngram_score"] = df_train["name_ngram_score"].map(lambda x:f"3:{x}")
df_train4svm_rank.to_csv("./train.dat", index=False, header=False, sep=" ")

df_test = scores_dropped_only_same_label[~scores_dropped_only_same_label["qid"].isin(train_qid)]
df_test.to_csv("./test.tsv", index=False, sep="\t")
