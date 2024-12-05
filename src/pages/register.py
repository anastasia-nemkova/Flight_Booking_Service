import streamlit as st
from services.auth_service import AuthService

def render_register_page() :
    st.title("Регистрация пользователя")
    
    first_name = st.text_input("Имя")
    last_name = st.text_input("Фамилия")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    password_confirm = st.text_input("Подтвердите пароль", type="password")

    if st.button("Зарегистрироваться"):
        if password != password_confirm:
            st.error("Пароли не совпадают!")
        else:
            try:
                auth_service = AuthService()
                auth_service.register_user(first_name, last_name, email, password)
                st.success("Пользователь успешно зарегистрирован!")
            except ValueError as e:
                st.error(str(e))
