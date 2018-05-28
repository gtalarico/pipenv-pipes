REM Release from Windows
rm -rdf build dist
python setup.py sdist bdist_wheel
twine upload dist/*
