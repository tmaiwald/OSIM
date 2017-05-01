@echo off

echo "baue.."
python setup.py build_ext --inplace
set /p id=".."