.ONESHELL:
.EXPORT_ALL_VARIABLES:
include $(env).sh

build:
	docker build -t $(TAG) --label versio=$(VERSION) .

deploy:
	docker run -d -p $(PORT):8000 $(TAG)
