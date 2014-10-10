SHELL = bash

main:
	cat schema.sql > tmpfile.sql
	./make_users.py $(year) > tmpfile.sql
	./make_problems.py $(year) > tmpfile.sql
	mysql -u root -p < tmpfile.sql

clean:
	rm -f tmpfile.sql
