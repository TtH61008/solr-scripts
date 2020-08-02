import pandas as pd

df_test = pd.read_csv("./test.tsv", sep="\t")

# svm rank結果の取得
# Solrの仕様でscoreの係数をマイナスにすることはできないので、マイナスの場合は0に置き換えている
with open("svm_struct_model") as f:
    svm_rank_result = f.readlines()[-1].split()

coef_name_score = float(svm_rank_result[1].split(":")[1]) if float(svm_rank_result[1].split(":")[1]) > 0 else 0 
coef_name_yomi_score = float(svm_rank_result[2].split(":")[1]) if float(svm_rank_result[2].split(":")[1]) > 0 else 0
coef_name_ngram_score = float(svm_rank_result[3].split(":")[1]) if float(svm_rank_result[3].split(":")[1]) > 0 else 0

df_test["ml_score"] = coef_name_score* df_test["name_score"] + coef_name_yomi_score*df_test["name_yomi_score"] + coef_name_ngram_score*df_test["name_ngram_score"]

df4eval = df_test.groupby("qid").idxmax().reset_index()
for field in ["name_score", "name_yomi_score", "name_ngram_score", "ml_score"]:
    recall = len(df4eval[df4eval["label"] == df4eval[field]])/len(df4eval)
    print(f"{field}ソートのrecall: {int(recall*100)}%")