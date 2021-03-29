default: build-package

install-dependencies:
	python3 -m venv venv --clear && \
	. venv/bin/activate && \
	pip install --upgrade pip setuptools wheel && \
	pip install twine

build-package:
	rm -rf dist/* && \
	. venv/bin/activate && \
	python setup.py sdist bdist_wheel

publish-pypi:
	. venv/bin/activate && \
	twine upload -r pypi dist/*

publish-testpypi:
	. venv/bin/activate && \
	twine upload -r testpypi dist/*
