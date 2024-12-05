import streamlit as st
from services.auth_service import AuthService

def render_login_page() :
    st.title("Вход в систему")

    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        auth_service = AuthService()
        user = auth_service.authenticate_user(email, password)
        
        if user:
            role = user[5]
            st.session_state.user_role = role
            st.session_state.user_id = user[0]
            st.rerun()
        else:
            st.error("Неверный email или пароль.")
