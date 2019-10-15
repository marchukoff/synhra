FROM python:3

RUN apt update -y && apt install -y default-jre

RUN pip install pipenv

RUN curl -o allure-2.12.1.tgz -L \
http://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.12.1/allure-commandline-2.12.1.tgz && \
tar -zxvf allure-2.12.1.tgz -C /opt/ && \
ln -s /opt/allure-2.12.1/bin/allure /usr/bin/allure

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

CMD ["python"]
