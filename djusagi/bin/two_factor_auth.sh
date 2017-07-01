#!/bin/bash

for group in staff faculty students
do
    echo "Group: $group"
    /usr/bin/python /d2/django_projects/djusagi/bin/two_factor_auth.py --who=$group --cache --test
done
