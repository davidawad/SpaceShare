##
# Makefile
# @Author David Awad
#

all: clear theshit

help: clear
	@echo "Hello $(LOGNAME)!, This makefile will automate your github commits code for submission."
	@echo "Type <make commit message=\"first commit\">\n\n\n"

theshit:
	docker-compose up --build

# TODO make sass and jsx just an assets makefile task.
# or use gulp because it's faster and like, event loop.
sass: clear
	sass --watch app/static/sass/stylesheet.scss:app/static/css/stylesheet.css
jsx:
	jsx --watch static/jsx static/js

# TODO make sure this actually compiles all assets for dev
setup: clear
	mkdir -p data/redis
	mkdir -p data/mongo
	virtualenv venv
	source venv/bin/activate && pip install -r requirements.txt

## TODO this should run unit tests on everything lol
test: clear
	casperjs test headless.js

clear:
	docker-compose rm -f
	docker rmi -f $(docker images -qf dangling=true)
	docker volume rm $(docker volume ls -qf dangling=true)
	clear
	@echo "\n\n"
