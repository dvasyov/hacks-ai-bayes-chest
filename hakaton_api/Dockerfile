FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -U -r requirements.txt

ENV PYTHONIOENCODING=utf8
ENV LC_ALL="en_US.UTF-8"
ENV TZ=Asia/Yekaterinburg.

CMD export PYTHONPATH=$PWD && python ./src/app/main.py