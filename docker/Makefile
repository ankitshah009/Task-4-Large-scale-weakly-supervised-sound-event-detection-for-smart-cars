help:
	@cat Makefile

DOCKER_NAME=task4-dcase-env
DOCKER_FILE=Task4Dockerfile
BACKEND=theano
SRC=$(shell dirname `pwd`)

build:
	docker build -t $(DOCKER_NAME) -f $(DOCKER_FILE) .

bash: build
	docker run -it -v $(SRC):/Task-4-Large-scale-weakly-supervised-sound-event-detection-for-smart-cars $(DOCKER_NAME) bash

task4: build
	sudo sh -c "whoami; whoami" && docker run -it -v $(SRC):/Task-4-Large-scale-weakly-supervised-sound-event-detection-for-smart-cars $(DOCKER_NAME) /bin/bash -c "python task4.py -p task4.defaults.yaml"

task4_challenge: build
	docker run -it -v $(SRC) $(DOCKER_NAME) /bin/bash -c "python task4.py -s dcase2017 -m challenge -o"

test4: build
	docker run -it -v $(SRC) $(DOCKER_NAME) /bin/bash -c "python task4.py -s minimal; python task4.py -show_eval"
