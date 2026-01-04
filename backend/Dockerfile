FROM python:3.11.9-slim AS base

WORKDIR /Project_plane_build

COPY . .

RUN pip install -r requirements_Backend.txt

WORKDIR /Project_plane_build/backend

COPY . . 

EXPOSE 8000

CMD ["uvicorn", "Backend:app", "--host", "0.0.0.0", "--port", "8000"]
