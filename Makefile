PYTHON=python3
ENVDIR=./env

env:
	virtualenv -p $(PYTHON) $(ENVDIR)

.PHONY: test
test: env
	$(ENVDIR)/bin/pip install tox
	$(ENVDIR)/bin/tox

.PHONY: clean
clean:
	rm -rf $(ENVDIR)
