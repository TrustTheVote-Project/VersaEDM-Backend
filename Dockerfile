FROM tiangolo/uvicorn-gunicorn:python3.8 AS base

WORKDIR /opt/electos/versadm
COPY requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY src/electos/versadm/app ./app
COPY src/electos/versadm/api ./api
COPY src/electos/versadm/models ./models

FROM base AS runapp
RUN groupadd -r versadm && useradd -r -g versadm versadm
USER versadm
WORKDIR /opt/electos

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "versadm.app.main:create_app()"]