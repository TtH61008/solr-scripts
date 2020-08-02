import requests

solr_endpoint="http://localhost:8983/solr/fukuoka/select"

with open("svm_struct_model") as f:
    svm_rank_result = f.readlines()[-1].split()

coef_name_score = float(svm_rank_result[1].split(":")[1]) if float(svm_rank_result[1].split(":")[1]) > 0 else 0 
coef_name_yomi_score = float(svm_rank_result[2].split(":")[1]) if float(svm_rank_result[2].split(":")[1]) > 0 else 0
coef_name_ngram_score = float(svm_rank_result[3].split(":")[1]) if float(svm_rank_result[3].split(":")[1]) > 0 else 0

def ml_ranked_search(query):
    payload = {
        "q":f"name:({query})^{coef_name_score} OR name_yomi:({query})^{coef_name_yomi_score} OR name_ngram:({query})^{coef_name_ngram_score}",
        "fl":"name,score"
    }
    r = requests.get(solr_endpoint, params=payload)
    print(r.url)
    return r.json()["response"]["docs"]

print(ml_ranked_search("ふくおか　体育"))
