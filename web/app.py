import streamlit as st


st.title("Валидация сведений о продукции")
st.markdown('')
name = ''
user_input = st.text_input("Текстовое описание продукции", name)
code = ''
st.text_input('Код ЕП РФ', code)
category = ''
st.text_input('Подкатегория', category)
for i in range(15):
    st.markdown('')
st.markdown('asd')
uploaded_file = st.file_uploader("Выберите csv")

