FROM tiangolo/uvicorn-gunicorn:python3.8 AS base

WORKDIR /usr/src/versa
COPY requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY versa/api ./api
COPY versa/app ./app
COPY versa/nist_model ./nist_model

FROM base AS runapp
RUN groupadd -r versa && useradd -r -g versa versa
USER versa
WORKDIR /usr/src

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "versa.app:create_app()"]