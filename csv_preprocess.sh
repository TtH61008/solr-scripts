echo "type,id,name,post_number,address,phone_number,service,business_hours,remarks,latitude,longitude,url," > convenience.csv
nkf -w ローソン店舗情報.csv  | sed -e "1d" | sed -e 's/^/"ローソン",/g' >> convenience.csv 
nkf -w セブンイレブン店舗情報.csv  | sed -e "1d" | sed -e 's/^/"セブンイレブン",/g' >> convenience.csv 
nkf -w ファミリーマート店舗情報.csv  | sed -e "1d" | sed -e 's/^/"ファミリーマート",/g' >> convenience.csv 
curl 'http://localhost:8983/solr/convenience_store/update?commit=true&indent=true' --data-binary @convenience.csv -H 'Content-Type: text/csv'



