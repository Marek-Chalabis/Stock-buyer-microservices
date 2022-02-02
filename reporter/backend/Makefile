full_test_code:
	# flake8 -> pflake8 allows to set rules in pyproject.toml
	pflake8 ./
	pytest \
		-n auto \
		--cov=. \
		--junitxml=.tests_reports/junit.xml
	mypy ./
	poetry check
	safety check --bare --full-report

full_format_code:
	black ./
	isort ./