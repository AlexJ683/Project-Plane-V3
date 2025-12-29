FROM python:3.11.9-slim AS base

WORKDIR /PROJECT_PLANE_V3

COPY . .

ENV PYTHONPATH=/PROJECT_PLANE_V3:$PYTHONPATH

RUN pip install --upgrade pip

RUN pip install pymysql

RUN pip install -r testing/requirements_testing.txt

# CMD ["sh", "-c", "pytest -s test_backend.py && pytest -s test_frontend.py"]
CMD ["pytest", "-s", "testing"]

