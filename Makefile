SERVER = genosmus.com
APPNAME = harp
TODAY = $(shell date '+%Y-%m-%d')

runserver:
	./manage.py runserver

install:
	pip install -r requirements.txt

clean:
	find . -name *.pyc -exec rm {} \;
	find . -name "__pycache__" -exec rm -rf {} \;


deploy: push
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && git pull && make deploy-server"

push:
	git push

deploy-server:
	$(MAKE) migrate
	$(MAKE) update-static-files
	$(MAKE) restart-server

migrate:
	./manage-production.py migrate analysis


update-static-files:
	./manage-production.py collectstatic -v0 --noinput


restart-server:
	../apache2/bin/restart
