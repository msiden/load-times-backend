build-deploy:
	docker build --no-cache -t lt-backend:latest .

build-local:
	docker build \
		--no-cache \
		-t lt-backend \
		-f ./Dockerfile.dev .

run-local-docker: build-local
	docker run -ti --network="host" -p 8000:8000 lt-backend

run-local:
	cd src/lt-backend/ && gunicorn -w 1 -b 0.0.0.0:8000 "app:app()" && cd ../../
