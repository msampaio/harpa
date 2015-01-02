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
	$(MAKE) update-static-files
	$(MAKE) restart-server

update-static-files:
	/usr/local/bin/python3.4 ./manage-production.py collectstatic -v0 --noinput

internationalization:
	./manage.py makemessages -l en_US
	./manage.py makemessages -l pt_BR

restart-server:
	../apache2/bin/restart
