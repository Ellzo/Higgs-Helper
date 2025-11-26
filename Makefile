.PHONY: install test coverage format lint clean run-ui build-index docker-build docker-run help

help:
	@echo "Higgs-Helper - Makefile Commands"
	@echo "================================="
	@echo "install       - Install all dependencies"
	@echo "test          - Run test suite"
	@echo "coverage      - Run tests with coverage report"
	@echo "format        - Format code with black"
	@echo "lint          - Run linting (flake8, mypy)"
	@echo "clean         - Remove build artifacts and cache"
	@echo "run-ui        - Launch Streamlit UI"
	@echo "build-index   - Build FAISS search index from corpus"
	@echo "docker-build  - Build Docker image"
	@echo "docker-run    - Run Docker container"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

format:
	black src/ tests/

lint:
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	mypy src/ --ignore-missing-imports

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/

run-ui:
	streamlit run src/ui/streamlit_app.py

build-index:
	python src/main.py build-index --corpus-path $(CORPUS_PATH) --output-path $(INDEX_PATH)

docker-build:
	docker build -t higgs-helper:latest .

docker-run:
	docker run -p 8501:8501 --env-file .env higgs-helper:latest
