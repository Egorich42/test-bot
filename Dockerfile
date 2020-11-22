FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

RUN apt-get update -y
RUN /usr/local/bin/python -m pip install --upgrade pip 

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["run.py"]
