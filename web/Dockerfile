FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -U -r requirements.txt

ENV PYTHONIOENCODING=utf8
ENV LC_ALL="en_US.UTF-8"
ENV TZ=Asia/Yekaterinburg.

CMD streamlit run /app/app.py --server.maxUploadSize=1028 --theme.primaryColor="#364EB9"