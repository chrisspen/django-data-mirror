#!/bin/bash
# Note, this should be used rarely, and instead the pre-commit hook relied upon.
yapf --in-place --recursive django_data_mirror ./*.py
