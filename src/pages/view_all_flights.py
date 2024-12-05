import streamlit as st
from services.flight_service import FlightService
from datetime import datetime

def show_flights_page():
    st.title("Рейсы")
    flight_service = FlightService()
    try:
        flights = flight_service.get_all_flights()
        if flights:
            st.write("Список всех рейсов:")
            for flight in flights:
                flight_id = flight[0]
                departure_city = flight[1]
                arrival_city = flight[2]
                departure_date = flight[3]
                departure_time = flight[4]
                arrival_date = flight[5]
                arrival_time = flight[6]
                airplane_model = flight[7]

                departure_date_str = departure_date.strftime('%d %b %Y') if isinstance(departure_date, datetime) else str(departure_date)
                arrival_date_str = arrival_date.strftime('%d %b %Y') if isinstance(arrival_date, datetime) else str(arrival_date)
                departure_time_str = departure_time.strftime('%H:%M') if isinstance(departure_time, datetime) else str(departure_time)
                arrival_time_str = arrival_time.strftime('%H:%M') if isinstance(arrival_time, datetime) else str(arrival_time)

                st.markdown(f"**Рейс ID**: {flight_id}")
                st.markdown(f"**Город отправления**: {departure_city}")
                st.markdown(f"**Город назначения**: {arrival_city}")
                st.markdown(f"**Дата вылета**: {departure_date_str}")
                st.markdown(f"**Время вылета**: {departure_time_str}")
                st.markdown(f"**Дата прибытия**: {arrival_date_str}")
                st.markdown(f"**Время прибытия**: {arrival_time_str}")
                st.markdown(f"**Модель самолета**: {airplane_model}")
                
                if st.button(f"Удалить рейс {flight_id}", key=f"delete_{flight_id}"):
                    try:
                        flight_service.delete_flight(flight_id)
                        flight_service.update_airplane_availability(flight_id)
                        st.success(f"Рейс {flight_id} успешно удален.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Ошибка при удалении рейса {flight_id}: {str(e)}")
                
                st.markdown("---") 
        else:
            st.write("Нет доступных рейсов.")
    except Exception as e:
        st.error(f"Ошибка при загрузке рейсов: {str(e)}")