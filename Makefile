IMAGE_NAME ?= file-resizer-app
PORT ?= 8080

.PHONY: build docker-build run docker-run test docker-test sbom trivy bandit

build:
	cd frontend && npm ci && npm run build

docker-build:
	docker build -t $(IMAGE_NAME) -f backend/Dockerfile .

run:
	uvicorn backend.app.main:app --reload --port $(PORT)

docker-run: docker-build
	docker run --rm -p $(PORT):8080 -e PYTHONPATH=/app -e DISABLE_CAPTCHA=true $(IMAGE_NAME)

test:
	pytest -q backend/tests

docker-test: docker-build
	docker run --rm -e PYTHONPATH=/app -e DISABLE_CAPTCHA=true $(IMAGE_NAME) pytest -q tests

sbom:
	# Requires syft installed locally: https://github.com/anchore/syft
	syft packages dir:. -o cyclonedx-json > sbom.cdx.json

trivy:
	# Requires trivy installed locally: https://aquasecurity.github.io/trivy
	trivy image --exit-code 0 --severity HIGH,CRITICAL $(IMAGE_NAME)

bandit:
	bandit -q -r backend/app -x backend/tests
