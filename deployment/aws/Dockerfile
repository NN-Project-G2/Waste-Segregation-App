FROM python:3.9.9-buster

ENV DB_HOST=waste-segregation.c8hu6dz2s7jp.ca-central-1.rds.amazonaws.com
ENV DB_PORT=3306
ENV DB_NAME=waste_segregation
ENV DB_USER=admin
ENV DB_PASSWORD=admin#123
ENV BUCKET_NAME=waste-segregation-project
ENV AWS_ACCESS_KEY_ID=AKIA3EVY7NYRX6I4R7NJ
ENV AWS_SECRET_ACCESS_KEY=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

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

COPY . /usr/src/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]