build:
	docker build . -t absql-testing

run:
	docker run -d -v ${ABSQL_HOME}:/ABSQL --name absql-testing absql-testing

exec:
	docker exec -it absql-testing /bin/bash

start:
	docker start absql-testing

stop:
	docker stop absql-testing

test:
	docker run --entrypoint pytest --rm -v ${ABSQL_HOME}:/ABSQL --name absql-make-test absql-testing

lint:
	docker run --entrypoint flake8 --rm -v ${ABSQL_HOME}:/ABSQL --name absql-make-lint absql-testing
