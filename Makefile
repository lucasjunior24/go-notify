deploy-local:
	docker build -t go-notify-local .
	docker-compose -f compose/compose-local/docker-compose.yaml up -d
		
deploy-develop:
	docker build -t go_notify_develop .
	docker-compose -f compose/compose-develop/docker-compose.yaml up -d


deploy-teste:
	docker build -t go-notify-local .
	docker-compose -f docker-compose.yml up -d

test:
	python -m pytest tests

cov-total:
	python -m pytest --cov=app tests

# coverage:
# 	py.test app/application_manager.py --cov-report xml:cov.xml --cov .
	
coverage:
	py.test app/__init__.py --cov-report xml:cov.xml --cov=app tests


deploy-nginx:
	docker-compose -f compose/compose-local/nginx.yaml up