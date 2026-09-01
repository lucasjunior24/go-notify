deploy-local:
	docker build -t go-notify-local .
	docker-compose -f compose/compose-local/docker-compose.yaml up -d
		
deploy-develop:
	docker build -t go_notify_develop .
	docker-compose -f compose/compose-develop/docker-compose.yaml up -d


deploy-test:
	docker build -t go-notify-local .
	docker-compose -f docker-compose.yml up -d

test:
	python -m pytest --cov=app tests --cov-report=xml 

cov-total:
	python -m pytest --cov=app tests



deploy-nginx:
	docker-compose -f compose/compose-local/nginx.yaml up