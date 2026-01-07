FROM python:3.11.9-slim AS base

WORKDIR /Project_plane_build

COPY . .

RUN pip install -r frontend/requirements_Frontend.txt

WORKDIR /Project_plane_build/frontend

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]

