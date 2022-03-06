docker-test-build:
	docker build . -t absql-testing

docker-run-test-image:
	docker run -d -v $ABSQL_HOME:/ABSQL --name absql-testing absql-testing

docker-test-exec:
	docker exec -it absql-testing /bin/bash
