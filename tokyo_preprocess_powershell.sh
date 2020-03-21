wget http://www.sinfonica.or.jp/kanko/estrela/refer/s29/tokyo3.csv -OutFile tokyo3.csv
$tokyo3 = Import-Csv -Encoding default  -Path ".\tokyo3.csv" -Header name,address,longitude,latitude,geo-p |select name,address,longitude,latitude,geo_p
foreach($r in $tokyo3){
$r.geo_p=$r.latitude+","+$r.longitude
}
$tokyo3 | Export-Csv "tokyo_conv.csv" -not -Encoding UTF8

