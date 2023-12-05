build:
	docker build --no-cache -t lt-backend:latest .

run-docker: build
	docker run -ti --network="host" -p 8000:8000 lt-backend

run-local:
	cd src/lt-backend/ && gunicorn -w 1 -b 0.0.0.0:8000 "app:app()" && cd ../../
