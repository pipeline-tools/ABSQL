docker-build:
	docker build . -t absql-testing

docker-run:
	docker run -d -v $ABSQL_HOME:/ABSQL --name absql-testing absql-testing

docker-exec:
	docker exec -it absql-testing /bin/bash

docker-start:
	docker start absql-testing

docker-stop:
	docker stop absql-testing
