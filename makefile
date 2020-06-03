ROOT_DIR:=./
SRC_DIR:=./src
TEST_DIR:=./tests

#Test it works with 'make hello'
# hello:
# 	@echo "Hello, World!"

make:
	python3 $(SRC_DIR)/main.py
	rm -rf src/*.pyc

test:
	python3 $(TEST_DIR)/gedcom_test.py

clean:
	rm -rf src/*.pyc
