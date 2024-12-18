FROM python:3.11.9

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

#CMD alembic upgrade head; python src/main.py
CMD ["python", "src/main.py"]