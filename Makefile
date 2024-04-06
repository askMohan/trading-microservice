build:			
	docker compose -f docker-compose.yaml build

up:
	docker compose -f docker-compose.yaml up -d

up-new:
	docker compose -f docker-compose.yaml up --build -d