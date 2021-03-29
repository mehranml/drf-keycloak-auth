default: build-package

build-package:
	rm -rf dist/*
	. venv/bin/activate
	python setup.py sdist bdist_wheel

publish-pypi:
	twine upload dist/*

publish-testpypi:
	twine upload -r testpypi dist/*
