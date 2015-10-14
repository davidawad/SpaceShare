# This is a simple makefile to automate commits for personal projects.
# Although this isn't good practice in general, you're probably only committing to master anyway.
# This assumes you've cloned over SSH, you could clone over HTTPS in which case you could just put in your credentials.

# run make -j2 to parallelize build steps
all: clear run sass

help: clear
	@echo "Hello $(LOGNAME)!, This makefile will automate your github commits code for submission."
	@echo "Type <make commit message=\"first commit\">\n\n\n"

# If you've cloned your git repo over SSH then this is the way to do it.
# Just fill the .gitignore first!
commit: clear clean
ifdef message
	@echo "Committing with $(message)"
	git add -A
	git commit -m"$(message)"
	git push
else
	@echo "please specify message"
endif

sass: clear
	sass --watch app/static/sass/stylesheet.scss:app/static/css/stylesheet.css

jsx:
	jsx --watch static/jsx static/js

run:
	clear
	python spaceshare/server.py

setup: clear
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt

test: clear
	casperjs test headless.js

clean:
	#put something to get rid of unwanted files.
	#rm *.pyc

clear:
	clear
	@echo "\n\n\n"
