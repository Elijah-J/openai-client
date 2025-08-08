@echo off
echo Installing test dependencies...
pip install --user -r requirements-test.txt

echo.
echo Running tests with coverage...
pytest --cov=. --cov-report=term-missing --cov-report=html

echo.
echo Test run complete. Coverage report saved to htmlcov/index.html