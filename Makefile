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
	twine upload dist/*

publish-testpypi:
	. venv/bin/activate && \
	twine upload -r testpypi dist/*

publish-gitlab:
	. venv/bin/activate && \
	twine upload --repository-url ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi dist/*