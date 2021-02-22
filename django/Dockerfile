FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY entrypoint.sh /run/entrypoint.sh
RUN \
  chmod a+rx /run/entrypoint.sh&& \
  apt-get update && \
  apt-get install -y python-django

ENTRYPOINT ["/run/entrypoint.sh"]
