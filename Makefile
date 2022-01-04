build:
	docker-compose build
test: # Single-click build and test
	docker-compose build
	docker-compose up -d
	docker-compose run flask_web_service flask tests
	docker-compose down
