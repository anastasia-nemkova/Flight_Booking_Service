import streamlit as st
import re
from datetime import datetime
from services.payment_service import PaymentService
from services.flight_service import FlightService

def render_payment_page() :
    st.title("Оплата билета")
    
    if "user_id" not in st.session_state:
        st.error("Ошибка: пользователь не авторизован.")
        return

    if "booking_id" not in st.session_state:
        st.error("Ошибка: бронирование не найдено.")
        return

    booking_id = st.session_state.booking_id
    flight_service = FlightService()
    booking_info = flight_service.get_booking_info(booking_id) 
    amount = booking_info['price']
    
    st.write(f"Бронирование для пассажира: {booking_info['passenger_name']}")
    st.write(f"Стоимость билета: {booking_info['price']} руб.")

    card_number = st.text_input("Введите номер карты")
    card_expiry = st.text_input("Введите срок действия карты (MM/YY)")
    card_cvc = st.text_input("Введите CVC")
    
    if card_number and not re.match(r"^\d{16}$", card_number):
        st.error("Номер карты должен содержать 16 цифр.")
        return

    if card_expiry and not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", card_expiry):
        st.error("Срок действия карты должен быть в формате MM/YY.")
        return

    if card_cvc and not re.match(r"^\d{3}$", card_cvc):
        st.error("CVC код должен содержать 3 цифры.")
        return
    
    if st.button("Оплатить"):
        if not card_number or not card_expiry or not card_cvc:
            st.error("Пожалуйста, заполните все поля.")
            return
        
        payment_service = PaymentService()
        try:
            payment_id = payment_service.create_payment(
                booking_id=booking_id,
                amount=amount,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvc=card_cvc
            )
            payment_service.update_payment_status(payment_id, 'Оплачено')
            st.success("Оплата прошла успешно!")

            st.session_state.page = "home"
        except Exception as e:
            st.error(f"Ошибка при оплате: {str(e)}")
            
def render_payments_page() :
    st.title("Мои билеты")
    
    if "user_id" not in st.session_state:
        st.error("Ошибка: пользователь не авторизован.")
        return
    
    user_id = st.session_state.user_id
    flight_service = FlightService()
    payment_service = PaymentService()
    
    bookings = flight_service.get_bookings(user_id)
    
    if not bookings:
        st.write("Вы еще не приобрели билеты((")
    else:
         for booking in bookings:
            status = booking['status']
            booking_id = booking['booking_id']
            flight_id = booking['flight_id']
            passenger_name = booking['passenger_name']
            passport_number = booking['passport_number']
            passport_seria = booking['passport_seria']
            booking_date = booking['booking_date']

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Бронирование ID**: {booking_id}")
                st.markdown(f"**Рейс ID**: {flight_id}")
                st.markdown(f"**ФИ пассажира**: {passenger_name}")
                st.markdown(f"**Паспорт**: {passport_seria} {passport_number}")
                booking_date_str = booking_date.strftime('%d %b %Y') if isinstance(booking_date, datetime) else str(booking_date)
                st.markdown(f"**Дата бронирования**: {booking_date_str}")
                st.markdown(f"**Статус**: {status}")

            with col2:
                if status != "Отменен":
                    if st.button("Вернуть", key=f"cancel_{booking_id}"):
                        try:
                            payment_service.cancel_payment(booking_id)
                            st.success(f"Оплата успешно отменена {booking['status']}!")
                            st.session_state.page = "payments"
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ошибка при отмене: {str(e)}")

            st.markdown("---")

