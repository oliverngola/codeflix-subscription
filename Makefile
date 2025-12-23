sql:
	@sqlite3 -column -header subscription_service.db

pg:
	docker-compose exec db psql -U postgres -d subscription_service

kc:
	docker-compose exec app python -m scripts.test_keycloak