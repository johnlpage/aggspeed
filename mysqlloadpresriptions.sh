mysql  -u root -ppassword -e "CREATE DATABASE nhs;"


mysql -u root -ppassword -e ' CREATE TABLE prescriptions ( sha char(3),pct char(3),practice char(6), bnfcode char(16),name varchar(32),nitems integer,nic real,cost real,quantity integer,period integer, primary key(practice,period,bnfcode));' nhs


for f in Prescriptions*.csv
do
		echo $f
		if [ ! -f "$f.loaded" ]; then
        	mysql -u root -ppassword  -e  "LOAD DATA LOCAL INFILE '"$f"' INTO TABLE prescriptions FIELDS TERMINATED BY ',' IGNORE 1 LINES" nhs && touch "$f.loaded"
        fi
done
