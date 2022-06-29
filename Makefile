server:
	poetry run uvicorn main:app --reload

test:
	poetry run pytest -v