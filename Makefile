# -*- makefile -*-

# definitions
SHELL = /bin/bash
PROJECT       = basic
HOST          = 127.0.0.1
PORT          = 8895
CURRPATH      = $(shell pwd)

PROJECT_TEST_TARGETS=general
PYTHONPATH=.:..

MANAGE=cd $(PROJECT) && PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings django-admin.py

manage:
ifndef CMD
	@echo Please, specify CMD argument to execute Django management command
else
	$(MAKE) clean
	$(MANAGE)  $(CMD)
endif

run:
	$(MAKE) clean
	$(MANAGE) runserver $(HOST):$(PORT)

shell:
	$(MAKE) clean
	$(MANAGE) shell

migrate:
	$(MAKE) clean
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	@echo Done

createsuperuser:
	$(MAKE) clean
	$(MANAGE) createsuperuser
	@echo Done

collectstatic:
	$(MAKE) clean
	$(MANAGE) collectstatic
	@echo Done

clean:
	@echo Cleaning up *.pyc files
	-find . | grep '.pyc$$' | xargs -I {} rm {}

test:
	$(MAKE) clean
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(PROJECT_TEST_TARGETS)

install:
	( \
		virtualenv --no-site-packages -p/usr/bin/python2.7 .env; \
		source $(CURRPATH)/.env/bin/activate; \
		pip install -r requirements.txt; \
	)
