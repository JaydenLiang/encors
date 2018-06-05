FROM python:3.6-slim

RUN mkdir /root/encors-py

COPY ./requirements.txt /root/encors-py/requirements.txt

COPY ./src /root/encors-py/src

RUN pip install -r /root/encors-py/requirements.txt

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", ":8000", "--chdir", "/root/encors-py/src", "encors:app"]