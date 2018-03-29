# A hasty example I tend to follow when I'm doing this. 
for better documentation, check out [https://csvkit.readthedocs.io/en/1.0.3/]

## Optional: First, is your data a csv? If not, do this
If needed, you can change the delimiter using in2csv:
The catch is, even if your data is delimited by something else, just rename it to .csv. It's the only way this will work. 

in2csv basicincident.csv –d ‘^’ > basicincident_fixed.csv

Not sure what your data is? use head -n 200 (or 1,000 or 20 or whatever) to see.
head -n 200 incidentaddress.csv 

## Get csvkit to make a create table statement for you and put that into a sql file
head -n 20 account_apprl_year.csv | csvsql --no-constraints --table account_apprl_year > create_account_apprl_year.sql

Couldn't get in2csv to work? You might still have a shot. Try something like this:

head -n 200 incidentaddress.csv | csvsql --no-constraints –d ‘^’ --table incidentaddress_2014 > create_incidentaddress_2014.sql

# Once you've got your SQL create table statement, open it in a text editor
(ignore the import warning) 
Touch up that sql file in a text editor.

## In postico, create your database
Copy and paste the create table statement you just made in the SQL input within your Postico database. Run that. You now have a table. 

## Optional: Cleaning up "" marks around strings in the command line 
sed 's/\""//g' account_apprl_year.csv > account_apprl_year_clean.csv

## Get your data into your table
Start your database (open postgres and connect, then a comman line will appear)
run 'psql;' first if you're not already there
then run: 
COPY account_apprl_year FROM '/Users/slamm/Documents/ abatements /DCAD2017_CURRENT/account_apprl_year_clean.csv' DELIMITER ',' CSV HEADER;

Or if you couldn't get that csv format working: 
COPY arson_2014 FROM '/Users/slamm/Documents/STEPHANIE_FIRE_DATA/2014/NFIRS_2014_030216/2014_csv/arson.csv' DELIMITER '^' CSV HEADER;

## Common Errors:
ERROR:  invalid byte sequence for encoding "UTF8": 0xc4, etec (sometimes encoding needs cleaning up)
Can run: 'file -I filename' to see what the encoding is
You can try the 'find and peck' method of changing individual problem characters by looking up their encoding, finding the offending character, and find-replacing in a text editor. Sometimes this won't work if the file is too large, though.
Common characters found:
Ä
Â
¿
ñ
Ã
Á
Í
Õ
É
Try searching *[^\x00-\x7F]* in sublime to give you all sorts of non-UTF8 characters you can find/replace if you're in a hurry.


You can also try to change the encoding using iconv:
iconv -f old-encoding -t new-encoding file.txt > newfile.txt

[http://www.fileformat.info/tip/linux/iconv.htm]

