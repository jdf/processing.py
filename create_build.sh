#!/bin/bash

echo -n 'Bumping version...'
version=$(ant bumpversion | perl -lne '/Bumped to version (\d+)/ && print $1')
echo $version
git commit -am "Build $version." && \
	git tag $version && \
	git push && \
	git push --tags && \
	ant mode.upload

