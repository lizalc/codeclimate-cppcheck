.PHONY: image

IMAGE_NAME ?= ghcr.io/lizalc/codeclimate-cppcheck-addons

image:
	docker build --platform linux/amd64 --rm -t $(IMAGE_NAME) .

clean:
	docker rmi $(IMAGE_NAME)
