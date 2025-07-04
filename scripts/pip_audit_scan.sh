#!/bin/bash
# Run pip-audit and output summary
pip install pip-audit || true
pip-audit || true
