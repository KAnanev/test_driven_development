mtest:
	-python manage.py test

ftest:
	-python functional_tests.py

run:
	-python manage.py runserver