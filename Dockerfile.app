FROM python:3.9 as compile-image
WORKDIR /app

RUN apt-get update && apt-get upgrade -y && \
apt-get install libsasl2-dev python3-dev libldap2-dev libssl-dev -y

COPY ./requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt

RUN git clone https://github.com/catemohi/naumen_api.git && \ 
cd naumen_api && python3 setup.py install

COPY ./src ./.venv ./