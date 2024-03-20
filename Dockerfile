FROM python:3.10

WORKDIR /app

COPY clueless/ /app/clueless
COPY pyproject.toml /app/
COPY LICENSE /app/
COPY README.md /app/

RUN chmod +x -R /app/

RUN pip install .

CMD ["clue", "serve", "--host", "0.0.0.0", "--port", "80"]