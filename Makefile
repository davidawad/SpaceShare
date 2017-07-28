##
# Makefile
# @Author David Awad
#

all: help

help:
	@echo "Hello $(whoami)!, This makefile will automate your dev setup for spaceshare."
	@echo "I use docker-compose to create multiple containers for the isolated components"
	@echo "of spaceshare. To set up a local dev instance try running `make run`."
	@echo "This could kill any dangling images and other docker images you might be running on your machine."

run: clean
	cp -r app/static nginx/static
	docker-compose up

# TODO make assets task for sass and jsx gulp tasks.
assets:
	gulp assets

# TODO this should run unit tests on everything
# Too bad I don't have any yet lol google don't judge me.
test: clean setup
	casperjs test headless.js

clean:
	docker-compose stop
	docker-compose rm -f
	rm -rf nginx/static
	clear
