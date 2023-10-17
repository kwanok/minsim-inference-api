.PHONY: image
image:
	docker build -t ghcr.io/kwanok/minsim-inference-api:latest . --no-cache

.PHONY: push
push:
	docker push ghcr.io/kwanok/minsim-inference-api:latest

.PHONY: buildx
buildx:
	docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/kwanok/minsim-inference-api:latest --push .

.PHONE: docker-run
docker-run:
	docker run -p 5000:80 ghcr.io/kwanok/minsim-inference-api:latest

.PHONY: run
run:
	poetry run gunicorn -w 10 --threads 4 -k uvicorn.workers.UvicornWorker src.main:app --bind=0.0.0.0:9600

.PHONY: format
format:
	poetry run black .
	poetry run isort .
	poetry run ruff check . --fix

.PHONY: ci
ci: format image push
