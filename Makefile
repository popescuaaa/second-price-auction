REQ=requirements.txt

install:
	pip3 install < REQ

run:
	python3 src/example.py
	
test:
	python3 src/solver.test.py

