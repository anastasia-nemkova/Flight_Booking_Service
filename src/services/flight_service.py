from repositories.flight import FlightRepository
from datetime import datetime, timedelta

class FlightService:
    def __init__(self) :
        self.repo = FlightRepository()
        
    def get_cities(self) :
        return self.repo.get_list_cities()
    
    def view_flights(self, departure_city: str, arrival_city: str, departure_date: str) :
        return self.repo.get_flights(departure_city, arrival_city, departure_date)
        
    def get_airports_for_cities(self, cities : str) :
        airports = self.repo.get_airports(cities)
        return [{"airport_id": airport[0], "name": f"{airport[1]} ({airport[2]})"} for airport in airports]

    def get_available_airplanes(self, departure_date : str, departure_time: str) :
        airplanes = self.repo.get_available_airplanes(departure_date, departure_time)
        if not airplanes:
            raise ValueError("Нет доступных самолётов на указанное время.")
        return [{"airplane_id": airplane[0], "model": airplane[1]} for airplane in airplanes]
        
    def add_flight(self, departure_airport_id : int, arrival_airport_id : int, airplane_id : int, departure_date : str, arrival_date : str, departure_time : str, arrival_time : str, ticket_price : float) :
        self.repo.add_flight(departure_airport_id, arrival_airport_id, airplane_id, arrival_date, departure_date, arrival_time, departure_time, ticket_price)

    def create_return_flight(self, departure_airport_id: int, arrival_airport_id: int, airplane_id: int, departure_date: str, arrival_date: str, departure_time: str, arrival_time: str, ticket_price : float):
        if isinstance(departure_date, str):
            departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
        if isinstance(arrival_date, str):
            arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()

        if isinstance(departure_time, str):
            departure_time = datetime.strptime(departure_time, '%H:%M').time()
        if isinstance(arrival_time, str):
            arrival_time = datetime.strptime(arrival_time, '%H:%M').time()

        departure_datetime = datetime.combine(departure_date, departure_time)
        arrival_datetime = datetime.combine(arrival_date, arrival_time)
        
        time_difference = arrival_datetime - departure_datetime
        time_difference_minutes = time_difference.total_seconds() / 60
        
        return_departure_datetime = arrival_datetime + timedelta(hours=5)
        return_departure_date = return_departure_datetime.date().isoformat()
        
        return_departure_time = return_departure_datetime.time()

        return_arrival_date = (return_departure_datetime + timedelta(minutes=time_difference_minutes)).date().isoformat()
        return_arrival_time = (datetime.combine(datetime.today(), return_departure_time) + timedelta(minutes=time_difference_minutes)).time().isoformat()
        
        self.repo.create_return_flight(arrival_airport_id, departure_airport_id, airplane_id, return_departure_date, return_arrival_date, return_departure_time.isoformat(), return_arrival_time, ticket_price)

    def create_booking(self, user_id: int, flight_id: int, passport_number: int, passport_seria : int, status : str = "Ожидает") :
        return self.repo.create_booking(user_id, flight_id, passport_number, passport_seria, status)
    
    def update_available_tickets(self, flight_id: int) :
        return self.repo.update_available_tickets(flight_id)
    
    def get_all_flights(self) :
        return self.repo.get_all_flights()
    
    def delete_flight(self, flight_id: int) :
        return self.repo.delete_flight(flight_id)
    
    def update_airplane_availability(self, flight_id : int) :
        return self.repo.update_airplane_availability(flight_id)
    
    def update_booking_status(self, booking_id : int, status : str = "Подтверждено") :
        return self.repo.update_booking_status(booking_id, status)
    
    def get_bookings(self, user_id : int) :
        return self.repo.get_bookings(user_id)
    
    def get_booking_info(self, booking_id : int) :
        return self.repo.get_booking_info(booking_id)