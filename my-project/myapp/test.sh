pytest -vv \
 --cov=myapp \
 --cov-config=.coveragerc \
 --cov-report=html \
 --cov-report=term \
 --cov-report=term-missing \
 --ignore=_zrb
