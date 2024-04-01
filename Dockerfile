FROM python:3.10

WORKDIR /app

COPY clueless/ /app/clueless
COPY pyproject.toml /app/
COPY LICENSE /app/
COPY README.md /app/

RUN chmod +x -R /app/

RUN pip install .

ENV BACKEND_PORT=80
ENV BACKEND_HOST="0.0.0.0"

CMD ["clue", "serve", "--host", "$BACKEND_HOST", "--port", "$BACKEND_PORT"]