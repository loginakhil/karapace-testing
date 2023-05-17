.PHONY:
deps:
	@pip3 install --user --ignore-installed requests

.PHONY:
test: deps
	@docker-compose up --detach --wait
	python3 test.py

.PHONY:
clean:
	@docker-compose stop
	@docker-compose rm --force