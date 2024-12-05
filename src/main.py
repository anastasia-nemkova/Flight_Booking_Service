import streamlit as st
import time
from pages.login import render_login_page
from pages.register import render_register_page
from pages.add_flight import render_add_flight_page
from pages.view_flight import render_view_flight_page
from pages.booking import render_book_flight_page
from pages.payment import render_payment_page, render_payments_page
from pages.view_all_flights import show_flights_page
from pages.data_base_page import admin_page

def show_message(mes : str):
    message = st.success(mes)
    time.sleep(1)
    message.empty()


def main():
    st.markdown("""
        <style>
        .big-button {
            font-size: 24px;
            padding: 20px;
            width: 100%;
            text-align: center;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Добро пожаловать в сервис по бронированию авиабилетов")
    
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "page" not in st.session_state:
        st.session_state.page = None
    if "selected_flight" not in st.session_state:
        st.session_state.selected_flight = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "booking_id" not in st.session_state:
        st.session_state.booking_id = None

    if st.session_state.user_role is None:
        col1 = st.columns(1)[0]
        
        with col1:
            if st.button("Войти", key="login_button", help="Перейти на страницу входа", use_container_width=True):
                st.session_state.page = "login"
        
        with col1:
            if st.button("Зарегистрироваться", key="register_button", help="Перейти на страницу регистрации", use_container_width=True):
                st.session_state.page = "register"
        
        if st.session_state.page == "login":
            render_login_page()
        elif st.session_state.page == "register":
            render_register_page()
    
    else:
        col2 = st.columns(1)[0]
        
        if st.session_state.user_role == "admin":
            with col2:
                st.success("Добро пожаловать, Администратор!")
                if st.button("Добавить рейсы", key="add_flight_button", use_container_width=True):
                    st.session_state.page = "add_flights"
                if st.button("Все рейсы", key="view_flights", use_container_width=True):
                    st.session_state.page = "flights"
                if st.button("Администрирование", key="admin",  use_container_width=True):
                    st.session_state.page = "admin"

        elif st.session_state.user_role == "user":
            with col2:
                st.success("Добро пожаловать, Пользователь!")
                if st.button("Найти рейсы!", key="find_flights_button", use_container_width=True):
                    st.session_state.page = "view_flights"
                if st.button("Просмотреть купленные билеты", key="view_pay_tickets", use_container_width=True):
                    st.session_state.page = "payments"
                    
        with col2:
            if st.button("Выйти", key="logout_button", use_container_width=True):
                st.session_state.page = "exit"
                           
        if st.session_state.page == "add_flights":
            render_add_flight_page()
        elif st.session_state.page == "flights":
            show_flights_page()
        elif st.session_state.page == "admin":
            admin_page()
        elif st.session_state.page == "view_flights":
            render_view_flight_page()
        elif st.session_state.page == "booking":
           render_book_flight_page()
        elif st.session_state.page == "payments":
            render_payments_page()
        elif st.session_state.page == "payment":
            render_payment_page()
        elif st.session_state.page == "exit":
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
