
mysql -u root -e ' DROP TABLE patientcounts' nhs
mysql -u root -e ' CREATE TABLE patientcounts (publication char(16),extractdate char(9),type char(2),ccgcode char(3),onsccgcode char(9),code char(6),postcode char(9),sex char(3),age char(3),numpatients int, primary key (code,extractdate));' nhs

for f in Count_*.csv
do
		echo $f
		if [ ! -f "$f.loaded" ]; then
        	mysql -u root  -e  "LOAD DATA LOCAL INFILE '"$f"' INTO TABLE patientcounts FIELDS TERMINATED BY ',' IGNORE 1 LINES" nhs && touch "$f.loaded"
        fi
done
