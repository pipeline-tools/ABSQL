build-image:
	docker build . -t absql-testing

run-image:
	docker run -d -v ${ABSQL_HOME}:/ABSQL --name absql-testing absql-testing

exec:
	docker exec -it absql-testing /bin/bash

start-container:
	docker start absql-testing

stop-container:
	docker stop absql-testing

remove-container:
	docker rm absql-testing

test:
	docker run --rm -v ${ABSQL_HOME}:/ABSQL --name absql-make-test absql-testing pytest

lint:
	docker run --rm -v ${ABSQL_HOME}:/ABSQL --name absql-make-lint absql-testing flake8

coverage:
	docker run --rm -v ${ABSQL_HOME}:/ABSQL --name absql-make-lint absql-testing pytest --cov=absql --cov-report=html tests/

browse-coverage:
	see htmlcov/index.html

fmt:
	black .
	flake8
