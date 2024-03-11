#!/bin/sh

mkdir tmp || true
venv/bin/python -m venv venv || python -m venv venv || true
venv/bin/pip install -r requirements.txt || pip install -r requirements.txt || true