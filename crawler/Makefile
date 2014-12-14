SHELL = bash

main:
	cat schema.sql > tmpfile.sql
	./make_users.py $(year) >> tmpfile.sql
	./make_problems.py $(year) >> tmpfile.sql
	./make_answers.py $(year) >> tmpfile.sql
	mysql -u root -p < tmpfile.sql

unzip:
	for file in ../sourcezip/*.zip; do unzip -q $$file -d ../source/$${file%.zip}; done

test:
	for file in ../sourcezip/*.zip; do zip -qT $$file; done

clean:
	rm -f tmpfile.sql
