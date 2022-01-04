build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down -v
test: # Single-click build and test
	docker-compose build
	docker-compose up -d
	docker-compose run flask_web_service flask tests
	docker-compose down
