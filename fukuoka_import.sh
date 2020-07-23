# 予め全ドキュメントを削除
curl 'http://localhost:8983/solr/fukuoka/update?commit=true&indent=true' --data '<delete><query>*:*</query></delete>'

# csvをポスト
curl 'http://localhost:8983/solr/fukuoka/update?commit=true&indent=true' --data-binary @fukuoka_converted.csv -H 'Content-Type: text/csv'