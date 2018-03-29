COPYCOMMAND LINE
head -n 20 account_apprl_year.csv | csvsql --no-constraints --table account_apprl_year > create_account_apprl_year.sql

(ignore the import warning) 
Touch up that sql file in a text editor

POSTICO
Run sql file you just created in the SQL input within your Postico database 

COMMAND LINEhea
sed 's/\""//g' account_apprl_year.csv > account_apprl_year_clean.csv

POSTGRES COMMAND LINE
psql;

COPY account_apprl_year FROM '/Users/slamm/Documents/ abatements /DCAD2017_CURRENT/account_apprl_year_clean.csv' DELIMITER ',' CSV HEADER;


in2csv basicincident.csv –d ‘^’ > basicincident_fixed.csv


head -n 200 incidentaddress.csv | csvsql --no-constraints –d ‘^’ --table incidentaddress_2014 > create_incidentaddress_2014.sql


COPY arson_2014 FROM '/Users/slamm/Documents/STEPHANIE_FIRE_DATA/2014/NFIRS_2014_030216/2014_csv/arson.csv' DELIMITER '^' CSV HEADER;

Errors:
ERROR:  invalid byte sequence for encoding "UTF8": 0xc4 0x20
0xc2 0x22
0xbf
0xf1 0x61 0x64 0x61
0xc3 0x65
Characters found:
Ä
Â
¿
ñ
Ã
Á
Í
Õ
É

Try searching [^\x00-\x7F]
