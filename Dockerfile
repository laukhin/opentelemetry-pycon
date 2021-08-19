FROM python:3.9.6

COPY pyproject* ./
COPY poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .
