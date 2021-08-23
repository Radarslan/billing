:: format app
isort --force-single-line-imports app
black app
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place app --exclude=__init__.py

:: format tests
isort --force-single-line-imports tests
black tests
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place tests --exclude=__init__.py