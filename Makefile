test:
	-python manage.py test

f-test:
	-python manage.py test functional_tests
	
lists-test:
	-python manage.py test lists

run:
	-python manage.py runserver

test-list-item-validation:
	-python manage.py test functional_tests.test_list_item_validation