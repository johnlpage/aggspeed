
mysql -u root  -e ' DROP TABLE practices' nhs
mysql -u root -e ' CREATE TABLE practices (period int,code char(6),name varchar(42),add1 varchar(30), add2 varchar(30),town varchar(30),county varchar(30),postcode char(9), primary key (code,period));' nhs



for f in Practises_*.csv
do
		echo $f
		if [ ! -f "$f.loaded" ]; then
        	mysql -u root  -e  "LOAD DATA LOCAL INFILE '"$f"' INTO TABLE practices FIELDS TERMINATED BY ',' IGNORE 1 LINES" nhs && touch "$f.loaded"
        fi
done
