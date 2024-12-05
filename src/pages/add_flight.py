import streamlit as st
from services.flight_service import FlightService


def render_add_flight_page() :
    st.title("Добавление рейса")

    flight_service = FlightService()

    cities = flight_service.get_cities()

    departure_city = st.selectbox("Город отправления", cities)
    arrival_city = st.selectbox("Город прибытия", cities)
    
    departure_airports = flight_service.get_airports_for_cities([departure_city])
    arrival_airports = flight_service.get_airports_for_cities([arrival_city])

    departure_airport_options = {airport["name"]: airport["airport_id"] for airport in departure_airports}
    arrival_airport_options = {airport["name"]: airport["airport_id"] for airport in arrival_airports}

    selected_departure_airport = st.selectbox("Аэропорт отправления", list(departure_airport_options.keys()))
    selected_arrival_airport = st.selectbox("Аэропорт прибытия", list(arrival_airport_options.keys()))

    departure_date = st.date_input("Дата отправления")
    departure_time = st.time_input("Время отправления")

    arrival_date = st.date_input("Дата прибытия")
    arrival_time = st.time_input("Время прибытия")

    if arrival_date < departure_date or (arrival_date == departure_date and arrival_time <= departure_time):
        st.error("Дата и время прибытия должны быть позже даты и времени отправления.")
        return
    
    available_airplanes = flight_service.get_available_airplanes(str(departure_date), str(departure_time))
    airplane_options = {airplane["model"]: airplane["airplane_id"] for airplane in available_airplanes}
    selected_airplane_model = st.selectbox("Выберите самолет", list(airplane_options.keys()))
    selected_airplane_id = airplane_options[selected_airplane_model]
    
    flight_price = st.number_input("Стоимость рейса", min_value=0.0, step=0.01, format="%.2f")

    if st.button("Добавить рейс"):
        try:
            if not departure_city or not arrival_city or not selected_departure_airport or not selected_arrival_airport:
                st.error("Пожалуйста, выберите все необходимые данные.")
                return

            flight_service.add_flight(
                departure_airport_id=departure_airport_options[selected_departure_airport],
                arrival_airport_id=arrival_airport_options[selected_arrival_airport],
                airplane_id=selected_airplane_id,
                departure_date=departure_date,
                arrival_date=arrival_date,
                departure_time=departure_time,
                arrival_time=arrival_time,
                ticket_price=flight_price,
            )
            
            flight_service.create_return_flight(
                departure_airport_id=departure_airport_options[selected_departure_airport],
                arrival_airport_id=arrival_airport_options[selected_arrival_airport],
                airplane_id=selected_airplane_id,
                departure_date=departure_date,
                arrival_date=arrival_date,
                departure_time=departure_time,
                arrival_time=arrival_time,
                ticket_price=flight_price,
            )
            
            st.success("Рейс успешно добавлен!")
        except Exception as e:
            st.error(f"Ошибка: {e}")