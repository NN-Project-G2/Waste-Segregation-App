FROM python:3.9.9-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y dos2unix ffmpeg libsm6 libxext6

COPY ./deployment/requirements.txt /usr/src/app/
RUN dos2unix /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./deployment/wait-for-it.sh /usr/local/bin/
RUN dos2unix /usr/local/bin/wait-for-it.sh
RUN chmod u+x /usr/local/bin/wait-for-it.sh

COPY ./deployment/custom-entrypoint /usr/local/bin/
RUN dos2unix /usr/local/bin/custom-entrypoint
RUN chmod u+x /usr/local/bin/custom-entrypoint
ENTRYPOINT ["custom-entrypoint"]

EXPOSE 8000