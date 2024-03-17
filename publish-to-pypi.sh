#!/bin/sh

rm -rf dist
rm -rf build
rm -rf ayapingping_py.egg-info
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
