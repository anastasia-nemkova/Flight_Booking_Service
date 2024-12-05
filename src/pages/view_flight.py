import streamlit as st
from services.flight_service import FlightService

def render_view_flight_page() :
    st.title("Поиск рейсов")
    
    flight_service = FlightService()
    cities = flight_service.get_cities()

    departure_city = st.selectbox("Выберите город отправления", options=cities)
    arrival_city = st.selectbox("Выберите город прибытия", options=cities)
    flight_date = st.date_input("Выберите дату полета")

    if "found_flights" not in st.session_state:
        st.session_state.found_flights = None

    if st.button("Найти рейсы"):
        try:
            flights = flight_service.view_flights(departure_city, arrival_city, str(flight_date))
            if flights:
                st.session_state.found_flights = flights
                st.success("Рейсы найдены! Прокрутите вниз, чтобы посмотреть.")
            else:
                st.session_state.found_flights = []
        except ValueError as e:
            st.error(str(e))

    if st.session_state.found_flights is not None:
        if not st.session_state.found_flights:
            st.error("Нет доступных рейсов на выбранную дату.")
        else:
            st.write("Доступные рейсы:")
            for flight in st.session_state.found_flights:
                st.write(f"Рейс {flight['flight_id']} - {flight['departure_city']} -> {flight['arrival_city']}")
                st.write(f"Аэропорт отправления: {flight['departure_airport']}")
                st.write(f"Аэропорт прибытия: {flight['arrival_airport']}")
                st.write(f"Дата и время вылета: {flight['departure_date']} {flight['departure_time']}")
                st.write(f"Дата и время прибытия: {flight['arrival_date']} {flight['arrival_time']}")
                st.write(f"Самолёт: {flight['airplane_model']}")
                st.write(f"Стоимость билета: {flight["price"]}")

                if st.button(f"Забронировать рейс", key=f"book_{flight['flight_id']}"):
                    st.session_state.page = "booking"
                    st.session_state.selected_flight = flight
                    st.rerun()
                st.write("---")
