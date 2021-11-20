import base64
from io import BytesIO
import streamlit as st
import pandas as pd
import requests
import json

api_host = '10.106.3.204:8095'
# api_host = 'localhost:8080'

categories = []


def get_categories():
    categories_df = pd.read_csv('./web/data/categories.csv')
    return categories_df['category'].unique()


def check_sample(sample_name, sample_category):
    data = json.dumps({
        'production_description': sample_name,
        'production_subcategory': sample_category
    })
    sample_response = requests.post(f"http://{api_host}/get_predict_sample", data=data).json()
    return int(sample_response['match'])


st.title("Валидация сведений о продукции")
st.markdown('')

name = ''
name = st.text_input("Введите текстовое описание продукции", name)

category = st.selectbox('Выберите подкатегорию', get_categories())

if st.button('Отправить'):
    quality = check_sample(name, category)
    # st.write(quality)
    if quality <= 33:
        result = f'<p style=" ' \
                 f'font-family:sans-serif; ' \
                 f'color:Red; font-size: 18px;">' \
                 f'Соответствие {quality} %</p>'
        st.write(result, unsafe_allow_html=True)
    elif 33 < quality <= 66:
        result = f'<p style="' \
                 f'font-family:sans-serif; ' \
                 f'color:#F8AA35; font-size: 18px;">' \
                 f'Соответствтие {quality} %</p>'
        st.write(result, unsafe_allow_html=True)
    elif 66 < quality <= 100:
        result = f'<p style="' \
                 f'font-family:sans-serif; ' \
                 f'color:Green; font-size: ' \
                 f'18px;">' \
                 f'Соответствие {quality} %</p>'
        st.write(result, unsafe_allow_html=True)

else:
    pass


for i in range(8):
    st.markdown('')
st.markdown('#### Можно загрузить сразу множество примеров через .csv файл')
st.markdown('Формат строк файла: *описание*, *подкатегория*')

uploaded_file = st.file_uploader("Выберите csv")

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    filename = 'web/data/uploaded.csv'
    dataframe.to_csv(filename, index=False)
    files = {'csv_file': open('web/data/uploaded.csv', 'rb')}
    csv_response = requests.post(f"http://{api_host}/get_predict_csv", files=files)
    download_df = pd.read_csv(BytesIO(csv_response.content))
    csv = download_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a download="file.csv" href="data:file/csv;base64,{b64}">Скачать csv файл</a>'
    st.write(href, unsafe_allow_html=True)
