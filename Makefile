deploy-local:
	docker build -t go-notify-local .
	docker build -t mongo .
	docker-compose -f compose/compose-local/docker-compose.yaml up -d
		
deploy-develop:
	docker build -t go_notify_develop .
	docker-compose -f compose/compose-develop/docker-compose.yaml up -d


deploy-teste:
	docker build -t go-notify-local .
	docker-compose -f docker-compose.yml up -d