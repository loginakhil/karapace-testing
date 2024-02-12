.PHONY:
deps:
	@pip3 install --user --ignore-installed requests

# Test Case 1 
# in this test case we have aggregated message called "Baz"
# it has "oneof" attribute to handle multiple event types
# first "foo" is added
# then if we try to add "bar" as a new type under oneof, we receive compatibility error
.PHONY:
test-case-1: clean deps test-with-karapace
	python3 test_case_1.py

# Test Case 2
# same case with Test Case 1 but runs with confluent
.PHONY:
test-case-2: clean deps test-with-confluent
	python3 test_case_2.py

# Test Case 3
# in this case we try to add "Corge" child message to parent "Qux" 
# we receive compatibility error since adding new message type is not compatible
# to solve it we can create separate proto for "Corge" and import in parent proto
# please check Test Case 4 for this workaround
.PHONY:
test-case-3: clean deps test-with-karapace
	python3 test_case_3.py

# Test Case 4
# this test case is representation of workaround for the issue in test case 3
# simply we separate child message to different proto and import in parent proto
# this workaround works successfully as expected
.PHONY:
test-case-4: clean deps test-with-karapace
	python3 test_case_4.py

# Test Case 5
# please check "Fuga" proto, it has messages, enums etc.
# if we add new message by importing as we do in previous test case, it gets error 500
# it looks parsing issue on karapace side
.PHONY:
test-case-5: clean deps test-with-karapace
	python3 test_case_5.py

# Test Case 6
# same test case with #5 but runs on confluent
# it works well
.PHONY:
test-case-6: clean deps test-with-confluent
	python3 test_case_6.py

# Test Case 7
.PHONY:
test-case-7: clean deps test-with-karapace
	python3 test_case_7.py

# Test Case 8
# test saving same schema again
.PHONY:
test-case-8: clean deps test-with-karapace
	python3 test_case_8.py

.PHONY:
test-with-confluent: deps
	@docker-compose -f confluent-docker-compose.yml up --detach --wait

.PHONY:
test-with-karapace: deps
	@docker-compose up --detach --wait

.PHONY:
clean:
	@docker-compose stop
	@docker-compose -f confluent-docker-compose.yml stop
	@docker-compose rm --force
	@docker-compose -f confluent-docker-compose.yml rm --force
