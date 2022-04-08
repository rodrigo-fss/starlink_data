test: 
	pip install -r requirements.txt
	pytest

run: 
	docker-compose up --build