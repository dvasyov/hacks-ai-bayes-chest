import streamlit as st


def get_categories():
    pass


st.title("Валидация сведений о продукции")
st.markdown('')

name = ''
user_input = st.text_input("Текстовое описание продукции", name)

category = st.selectbox('Подкатегория', ('Кобикорм', 'Посуда', 'Интернет'))

# st.write('You selected:', category)
for i in range(15):
    st.markdown('')
st.markdown('Также можно загрузить сразу множество примеров через .csv файл')
uploaded_file = st.file_uploader("Выберите csv")

