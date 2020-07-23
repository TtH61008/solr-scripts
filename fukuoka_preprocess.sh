wget https://ckan.open-governmentdata.org/dataset/6255d72b-991f-48a3-8439-20b11fc106ab/resource/c554a222-013f-43e9-aa9c-39fc82b217d3/download/401307_public_facility_sports.csv
wget https://ckan.open-governmentdata.org/dataset/6255d72b-991f-48a3-8439-20b11fc106ab/resource/d1ddf432-d1bd-4a88-b5fa-77caeab0cc16/download/401307_public_facility_library.csv
wget https://ckan.open-governmentdata.org/dataset/6255d72b-991f-48a3-8439-20b11fc106ab/resource/c4e98f54-2ef5-4f1a-a8b8-3361036ef716/download/401307_public_facility_culture.csv
wget https://ckan.open-governmentdata.org/dataset/6255d72b-991f-48a3-8439-20b11fc106ab/resource/fa5da814-6fb9-4800-845f-7387ca0b9fd4/download/401307_public_facility_museum.csv

#echo "city_code,no,prefecture,city,name,name_kana,name_pop,poi,address,calligraphy,latitude,longitude,phone_number,extension_number,corporate_number,org_name,available_days,start_time,end_time,available_time_remarks,explanation,easy_access_info,url,remarks" > fukuoka_converted.csv 

# concatedファイルの初期化
echo "" > fukuoka_concated.csv

tail -n +2 401307_public_facility_sports.csv |  awk 'BEGIN {FS=",";OFS=","} {print $5,$6,$7,$9,$11,$12,"\""$11,$12"\"",$13,"sports"} ' >> fukuoka_concated.csv
tail -n +2 401307_public_facility_library.csv  | awk 'BEGIN {FS=",";OFS=","} {print $5,$6,$7,$9,$11,$12,"\""$11,$12"\"",$13,"library"} ' >> fukuoka_concated.csv 
tail -n +2 401307_public_facility_culture.csv  | awk 'BEGIN {FS=",";OFS=","} {print $5,$6,$7,$9,$11,$12,"\""$11,$12"\"",$13,"culture"} ' >> fukuoka_concated.csv 
tail -n +2 401307_public_facility_museum.csv | awk 'BEGIN {FS=",";OFS=","} {print $5,$6,$7,$9,$11,$12,"\""$11,$12"\"",$13,"museum"} ' >> fukuoka_concated.csv 

# ヘッダの挿入
echo "name,name_kana,name_pop,address,latitude,longitude,geo_p,phone_number,category" > fukuoka_converted.csv 

# 緯度経度を格納するgeo-pは空の場合","となりますが、これはインポート時にエラーを起こすので空文字に置き換えます。
cat fukuoka_concated.csv | sed 's/","/""/g' >> fukuoka_converted.csv

# curl 'http://localhost:8983/solr/tokyo_conv/update?commit=true&indent=true' --data-binary @tokyo_conv.csv -H 'Content-Type: text/csv'
