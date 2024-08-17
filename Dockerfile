FROM python:3.10-slim

WORKDIR /fapi_app

COPY . /fapi_app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /fapi_app/requirements/base.txt