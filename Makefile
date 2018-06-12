init:
	pip install -r requirements.txt

test:
	pytest tests

build:
	python setup.py sdist
	python setup.py bdist_wheel --universal

install: clean build uninstall
	pip install ./dist/expiringdict_with_default-*.tar.gz

publish: clean build
	twine upload dist/*

uninstall:
	pip uninstall expiringdict_with_default -y

clean:
	rm -fr build dist expiringdict_with_default.egg-info

.PHONY: init test build install publish uninstall clean<Paste>
