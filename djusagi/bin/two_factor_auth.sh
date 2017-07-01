#!/usr/bin/env bash

# Informix crap
INFORMIXSERVER=wilson
DBSERVERNAME=wilson
ONCONFIG=onconf.cars
INFORMIXDIR=/opt/ibm/informix
INFORMIXSQLHOSTS=$INFORMIXDIR/etc/sqlhosts
LD_LIBRARY_PATH=$INFORMIXDIR/lib:$INFORMIXDIR/lib/esql:$INFORMIXDIR/lib/tools:$INFORMIXDIR/lib/cli:/usr/local/lib/;
LD_RUN_PATH=$LD_LIBRARY_PATH
# unixodbc
ODBCINI=/etc/odbc.ini

for group in staff faculty students
do
    /usr/bin/python /d2/django_projects/djusagi/bin/two_factor_auth.py --who=$group --test
done
