# Install dependencies
install:
	pip3 install -r requirements.txt
# Run migrations
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
# Seed database
seed:
	python3 manage.py seed_db
# Run development server
run:
	python3 manage.py runserver
# Test
test:
	python3 manage.py test tasks -v 2  
# Clean up
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete