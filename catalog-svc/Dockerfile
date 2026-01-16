#Build variable with default of 'dev'
ARG build_env="dev"

# common base image
FROM python:3.12.0-alpine3.18 AS base

# set a non root user
RUN adduser -D hafsa
USER hafsa

WORKDIR /home/hafsa
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python","app/catalog-app.py"]

FROM base AS branch-dev 

# builds using the 'base' and copies the app files
FROM base AS branch-prod
COPY ./ /home/hafsa/app/

FROM branch-${build_env} AS final