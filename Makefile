.PHONY: run lint test docker-build docker-up docker-down

# 🧪 Testiranje
test:
	pytest -v

# 🧼 Lintanje (PEP8 via flake8)
lint:
	flake8 src tests

# 🚀 Pokreni lokalno
run:
	uvicorn src.main:app --reload

# 🐳 Docker build
docker-build:
	docker-compose build

# 🐳 Pokreni preko Dockera
docker-up:
	docker-compose up --build

# 🧹 Zaustavi i očisti kontejnere
docker-down:
	docker-compose down
