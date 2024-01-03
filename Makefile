.PHONY:
deps:
	@pip3 install --user --ignore-installed requests

.PHONY:
test: deps
	@docker-compose up --detach --wait
	python3 test.py

.PHONY:
test-with-confluent: deps
	@docker-compose -f confluent-docker-compose.yml up --detach --wait
	python3 test.py

.PHONY:
clean:
	@docker-compose stop
	@docker-compose -f confluent-docker-compose.yml stop
	@docker-compose rm --force
	@docker-compose -f confluent-docker-compose.yml rm --force
