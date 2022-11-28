SHELL := /bin/bash
# you can set the value of `GECKO_VER` to particular version number instead of latest one (for ex. 0.22.0)
# GECKO_VER=$(shell curl --silent https://github.com/mozilla/geckodriver/releases.atom 2>/dev/null| grep -e ">v[0-9]" |head -1|sed "s/[\/\ \<\>a-z]//g")
GECKO_VER=0.26.0

# you can set the value of `CHROME_VER` to particular version number instead of latest one
# CHROME_VER=$(shell curl --silent https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
CHROME_VER=107.0.5304.62

ENVIRONMENT=dev
PYTHON_VER=3.11.0
NODE_VER=18.12.0
DOMAIN=kora.1kb.pl
URL_SCHEME=https
DJAPP_PORT=8000
FASTAPP_PORT=8888
ENVDIR=$(shell pwd)/.envs
PRJDIR=$(shell pwd)
TOPDIR=$(shell dirname ${PRJDIR})
LOGDIR=$(TOPDIR)/logs
BINDIR=$(TOPDIR)/bin
ETCDIR=$(TOPDIR)/etc
RUNDIR=$(TOPDIR)/run
BDIR=$(TOPDIR)/build
PYBDIR=$(TOPDIR)/build/Python-${PYTHON_VER}
SHAREDIR=$(TOPDIR)/share
INCDIR=$(TOPDIR)/include
ORACLE_HOME=$(TOPDIR)/oracle
APPDIR=$(PRJDIR)/app
PYTHON=$(BINDIR)/python3
PIP=$(BINDIR)/pip3
UNAME=$(shell uname)
BRANCH=$(shell git branch 2>/dev/null | grep '^*' | colrm 1 2|sed "s/[ \(\)]//g")
COMMIT_BRANCH=$(shell echo $${CI_COMMIT_BRANCH:-$(BRANCH)})
PATH=$(BINDIR):$(PRJDIR)/e2e/node_modules/.bin:/bin:/usr/bin:/sbin:/usr/sbin:${HOME}/.local/bin
APPUSER=$(shell id -un)
APPUID=$(shell id -u $(APPUSER))
APPGROUP=$(shell id -gn $(APPUSER))
APPGID=$(shell id -g $(APPUSER))
PPDIR=$(BDIR)/++
VARS=$(shell cat $(PRJDIR)/.vars)
MAKE_ENV := $(shell echo $(VARS) | awk -v RS=' ' '/^[a-zA-Z0-9_]+$$/')
SHELL_EXPORT := $(foreach v,$(MAKE_ENV),$(v)='$($(v))')
DOCKER_ENVS := $(foreach v,$(MAKE_ENV),-e $(v))


all: env

clean:
	cd $(BDIR) && rm -rf ++ done.* Python-* node-* dist geckodriver* chromedriver*

distclean:
	rm -rf $(BDIR) $(BINDIR) $(LOGDIR) $(ETCDIR) $(INCDIR)

download: $(BDIR)/done.download
python: $(BDIR)/done.python
install: $(BDIR)/done.install
packages: $(BDIR)/done.packages
env: $(BDIR)/done.env
pre-commit: $(BDIR)/done.pre-commit
node: $(BDIR)/done.node


$(BDIR)/Python-${PYTHON_VER}.tgz: $(BDIR)/done.download.python

$(PYBDIR): $(BDIR)/Python-${PYTHON_VER}.tgz
	cd $(BDIR) && tar zxf $<

$(BDIR)/done.download.python: $(BDIR)/done.dirs
	@echo "downloading python ${PYTHON_VER} ..."
	curl --silent -o $(BDIR)/Python-${PYTHON_VER}.tgz https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tgz
	touch $@

$(BDIR)/done.download: $(BDIR)/done.download.python
	touch $@

$(BDIR)/done.python: $(PYBDIR)
	cd $< && ./configure --prefix=$(TOPDIR) --enable-optimizations
	cd $< && make
	touch $@

$(BDIR)/done.install: $(BDIR)/done.python
	cd $(PYBDIR) && make install
	@if [ -x $(BINDIR)/python ] ; then echo "make: *** Python link already exists. Skipping." ; else ln -s python3 $(BINDIR)/python ; fi
	touch $@

$(BDIR)/done.pre-commit: $(BDIR)/done.packages
	pre-commit install
	touch $@

$(BDIR)/done.pip: $(BDIR)/done.install
	$(PIP) install --upgrade pip
	$(PIP) install wheel
	touch $@

$(BDIR)/done.packages: $(BDIR)/done.pip node
	$(PIP) install -r requirements/$(ENVIRONMENT).txt
	touch $@

$(BDIR)/node-v${NODE_VER}-linux-x64.tar.xz:
	curl -o $@ https://nodejs.org/dist/v${NODE_VER}/node-v${NODE_VER}-linux-x64.tar.xz

$(BDIR)/node-v${NODE_VER}-linux-x64: $(BDIR)/node-v${NODE_VER}-linux-x64.tar.xz
	cd ${BDIR} && tar xf $<
	touch $@

$(BDIR)/done.node: $(BDIR)/node-v${NODE_VER}-linux-x64
	cd $< ; tar cf - * | (cd ${TOPDIR} ; tar xf -)
	${BINDIR}/npm install -g npm
	${BINDIR}/npm install -g yarn
	touch $@

$(BDIR):
	mkdir -p $(BDIR)

$(BDIR)/done.dirs: $(BDIR)
	mkdir -p ${ETCDIR}
	mkdir -p ${BINDIR}
	mkdir -p ${LOGDIR}
	touch $@

$(BDIR)/done.env: $(BDIR)/done.packages
	@touch $(PRJDIR)/.env.local
	touch $@

build:
	docker compose -f .docker/dev/compose.yaml build
	docker compose -f .docker/dev/compose.yaml run -it kora-ui npm install

run:
	docker compose -f .docker/dev/compose.yaml up

shell:
	docker compose -f .docker/dev/compose.yaml run -it kora-app ./manage.py shell_plus
