DOCKER_IMAGE_NAME=us-central1-docker.pkg.dev/demos-375017/demo-images/test:latest

docker_build:
	docker build -t $(DOCKER_IMAGE_NAME) .


docker_push:
	docker push $(DOCKER_IMAGE_NAME)


run_test:
	modal run model.py
