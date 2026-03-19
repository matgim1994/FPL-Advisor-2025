.PHONY: dev-up dev-down prod-up prod-down streamlit

dev-up:
	docker compose --env-file config/dev/.env up -d

dev-down:
	docker compose --env-file config/dev/.env down

prod-up:
	docker compose --env-file config/prod/.env up -d

prod-down:
	docker compose --env-file config/prod/.env down

streamlit:
	export $(grep -v '^#' config/dev/.env | grep -v '^$' | xargs) && cd streamlit && streamlit run Home.py
