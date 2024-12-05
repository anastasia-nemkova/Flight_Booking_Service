import streamlit as st
import re
from services.flight_service import FlightService
from services.auth_service import AuthService


def render_book_flight_page() :
    st.title("Бронирование рейса")
    
    if "selected_flight" not in st.session_state:
        st.error("Ошибка: рейс не выбран.")
        return

    flight = st.session_state.selected_flight
    st.write(f"Рейс {flight['flight_id']} - {flight['departure_city']} -> {flight['arrival_city']}")
    st.write(f"Дата и время вылета: {flight['departure_date']} {flight['departure_time']}")
    st.write(f"Аэропорт отправления: {flight['departure_airport']}")
    st.write(f"Стоимость билета: {flight['price']}")
    st.write(f"Количество доступных билетов: {flight['available_tickets']}")
    
    user_service = AuthService()
    user_info = user_service.get_user_info(st.session_state.user_id)
    
    expected_name = f"{user_info['first_name']} {user_info['last_name']}"
    
    passenger_name = st.text_input("Введите ФИ")
    passport_seria = st.text_input("Введите серию паспорта")
    passport_number = st.text_input("Введите номер паспорта")
    
    if st.button("Оплатить"):
        if not passenger_name or not passport_number or not passport_seria:
            st.error("Пожалуйста, заполните все поля.")
            return
        
        if passenger_name != expected_name:
            st.error("Ошибка: введенные ФИО не совпадают с данными пользователя.")
            return
        
        if passport_seria and not re.match(r"^\d{4}$", passport_seria):
            st.error("Серия паспорта должна содержать 4 цифры.")
            return

        if passport_number and not re.match(r"^\d{6}$", passport_number):
            st.error("Номер паспорта должен содержать 6 цифр.")
            return
        
        booking_service = FlightService()
        try:
            booking_id = booking_service.create_booking(
                user_id=st.session_state.user_id,
                flight_id=flight['flight_id'],
                passport_number=passport_number,
                passport_seria=passport_seria
            )
            if booking_id:
                booking_service.update_booking_status(booking_id)
                booking_service.update_available_tickets(flight['flight_id'])
                st.session_state.booking_id = booking_id
                st.success("Бронирование успешно оформлено!")
                
                st.session_state.page = "payment"
                st.rerun()
            else:
                st.error("Ошибка при создании бронирования.")
        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
