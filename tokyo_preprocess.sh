wget http://www.sinfonica.or.jp/kanko/estrela/refer/s29/tokyo3.csv
echo "name,address,longitude,latitude" > tokyo_conv.csv 
nkf -w tokyo3.csv >> tokyo_conv.csv
curl 'http://localhost:8983/solr/tokyo_conv/update?commit=true&indent=true' --data-binary @tokyo_conv.csv -H 'Content-Type: text/csv'
