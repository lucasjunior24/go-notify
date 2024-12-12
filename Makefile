deploy-local:
		docker build -t go_notify_local:1.0 .
		docker-compose -f compose/compose-local/docker-compose.yml up -d
		
deploy-develop:
		docker build -t go_notify_develop .
		docker-compose -f compose/compose-develop/docker-compose.yml up -d