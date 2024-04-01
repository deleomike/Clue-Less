FROM python:3.10

USER root
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ntp netbase

COPY clueless/ /app/clueless
COPY pyproject.toml /app/
COPY LICENSE /app/
COPY README.md /app/

RUN chmod +x -R /app/

RUN pip install .

ENV BACKEND_PORT=80
ENV BACKEND_HOST="0.0.0.0"

EXPOSE $BACKEND_PORT

CMD ["clue", "serve"]