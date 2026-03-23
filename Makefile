.PHONY: dev-up dev-down prod-up prod-down streamlit predict

dev-up:
	docker compose --env-file config/dev/.env up -d

dev-down:
	docker compose --env-file config/dev/.env down

prod-up:
	docker compose --env-file config/prod/.env up -d

prod-down:
	docker compose --env-file config/prod/.env down

dev-streamlit:
	export $DEV && cd streamlit && streamlit run Home.py

dev-jupyter:
	export $DEV && jupyter notebook

dev-predict:
	export $DEV && python -m prediction.src.predict
