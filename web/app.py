import base64
import random
from io import BytesIO
import streamlit as st
import pandas as pd
import requests
import json

api_host = 'api:8090'
# api_host = 'localhost:8080'

categories = []


def get_categories():
    categories_df = pd.read_csv('/app/data/categories.csv')
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
    # quality = random.randint(0, 100)
    # st.write(quality)
    default_style = '<p style=" ' \
                    'padding: 10px;' \
                    'background-color:#f0f2f6;' \
                    'font-family:sans-serif; ' \
                    'font-size: 18px;'
    if quality <= 33:
        result = default_style + \
                 f'color:Red;">' \
                 f'Соответствие {quality} %</p>'
        st.write(result, unsafe_allow_html=True)
    elif 33 < quality <= 66:
        result = default_style + \
                 f'color:#F8AA35;">' \
                 f'Соответствие {quality} %</p>'
        st.write(result, unsafe_allow_html=True)
    elif 66 < quality <= 100:
        result = default_style + \
                 f'color:Green;">' \
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
    filename = 'app/data/uploaded.csv'
    dataframe.to_csv(filename, index=False)
    files = {'csv_file': open('app/data/uploaded.csv', 'rb')}
    csv_response = requests.post(f"http://{api_host}/get_predict_csv", files=files)
    download_df = pd.read_csv(BytesIO(csv_response.content))
    csv = download_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a download="file.csv" href="data:file/csv;base64,{b64}">Скачать csv файл</a>'
    st.write(href, unsafe_allow_html=True)
