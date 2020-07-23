ubuntuでsolrの設定を行うスクリプトファイル

便利コマンド
```
# 検索
$ curl "http://localhost:8983/solr/fukuoka/select?q=%E7%A6%8F%E5%B2%A1%E3%80%80%E5%9B%BD%E9%9A%9B%E4%BC%9A%E8%AD%B0%E5%A0%B4&q.op=OR"

# コアのリロード
$ curl 'http://localhost:8983/solr/admin/cores?wt=json&action=RELOAD&core=fukuoka'

# データの再import （予めfukuoka_preprocess.shを実行しcsvが作成されていること）
# 予め全ドキュメントを削除
curl 'http://localhost:8983/solr/fukuoka/update?commit=true&indent=true' --data '<delete><query>*:*</query></delete>'
# csvをポスト
curl 'http://localhost:8983/solr/fukuoka/update?commit=true&indent=true' --data-binary @fukuoka_converted.csv -H 'Content-Type: text/csv'

# features_definition.jsonのデプロイ
curl -XPUT 'http://localhost:8983/solr/fukuoka/schema/feature-store' --data-binary @feature_definition.json -H 'Content-type:application/json'
```