build:
	docker-compose build
run:
	docker-compose up -d
test: # Single-click build and test
	docker-compose build
	docker-compose up -d
	docker-compose run flask_web_service flask tests
	docker-compose down
seed:
	docker-compose run flask_web_service flask seed
clean:
	docker-compose run flask_web_service flask clean
