import psycopg2.extras
from typing import List, Dict
from repositories.connector import get_connection

class FlightRepository:
    
    def get_list_cities(self) -> List[str]:
        query = """
            SELECT DISTINCT city FROM airports;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [row[0] for row in cur.fetchall()]
    
    def get_flights(self, departure_city: str, arrival_city: str, departure_date: str):
        query = """
            SELECT f.flight_id, f.departure_airport_id, f.arrival_airport_id, f.airplane_id, 
                f.departure_date, f.arrival_date, f.departure_time, f.arrival_time,
                a1.city AS departure_city, a2.city AS arrival_city,
                a1.name AS departure_airport, a2.name AS arrival_airport,
                air.model AS airplane_model, f.ticket_price AS price, air.available_tickets AS available_tickets
            FROM flights f
            JOIN airports a1 ON f.departure_airport_id = a1.airport_id
            JOIN airports a2 ON f.arrival_airport_id = a2.airport_id
            JOIN airplanes air ON f.airplane_id = air.airplane_id
            WHERE a1.city = %(departure_city)s AND a2.city = %(arrival_city)s
            AND f.departure_date = %(departure_date)s AND air.available_tickets > 0
        """
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query, {
                    "departure_city": departure_city, 
                    "arrival_city": arrival_city, 
                    "departure_date": departure_date
                })
                return cur.fetchall()  
    
    def get_airports(self, cities : str):
        query = """
            SELECT airport_id, name, city
            FROM airports
            WHERE city = ANY(%(cities)s);
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {"cities": cities})
                return cur.fetchall()
    
    
    def get_available_airplanes(self, departure_date: str, departure_time: str) -> List[Dict]:
        query = """
            WITH flight_counts AS (
                SELECT flights.airplane_id, COUNT(*) AS flight_count
                FROM flights
                WHERE flights.departure_date = %(departure_date)s
                GROUP BY flights.airplane_id
            )
            SELECT airplanes.airplane_id, airplanes.model
            FROM airplanes
            LEFT JOIN flights ON airplanes.airplane_id = flights.airplane_id
            LEFT JOIN flight_counts ON airplanes.airplane_id = flight_counts.airplane_id
            WHERE
                (
                    flights.airplane_id IS NULL
                    OR 
                    (flights.departure_date != %(departure_date)s)
                    OR 
                    (
                        flights.departure_date = %(departure_date)s 
                        AND (flights.departure_time + INTERVAL '10 hour' <= %(departure_time)s
                            OR flights.departure_time - INTERVAL '10 hour' >= %(departure_time)s)
                    )
                )
                AND (flight_counts.flight_count IS NULL OR flight_counts.flight_count != 2)
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {
                    "departure_date": departure_date, 
                    "departure_time": departure_time
                })
                return cur.fetchall()
        
    def add_flight(self, departure_airport_id : int, arrival_airport_id : int, airplane_id : int, departure_date : str, arrival_date : str, departure_time :str , arrival_time : str, ticket_price : float):
        query_check_cities = """
            SELECT a1.city, a2.city
            FROM airports a1
            JOIN airports a2 ON a1.airport_id = %s AND a2.airport_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query_check_cities, (
                    departure_airport_id, 
                    arrival_airport_id
                ))
                cities = cur.fetchone()
                
                if cities and cities[0] == cities[1]:
                    raise ValueError("Нельзя забронировать рейс из одного города в тот же город.")
        
        query_add_flight = """
            INSERT INTO flights (departure_airport_id, arrival_airport_id, airplane_id, departure_date, arrival_date, departure_time, arrival_time, ticket_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query_add_flight, (
                    departure_airport_id, 
                    arrival_airport_id, 
                    airplane_id, 
                    departure_date, 
                    arrival_date, 
                    departure_time, 
                    arrival_time,
                    ticket_price
                ))
                conn.commit()
                
    def create_return_flight(self, departure_airport_id: int, arrival_airport_id: int, airplane_id: int, departure_date: str, arrival_date: str, departure_time: str, arrival_time: str, ticket_price : float):
        query_add_return_flight = """
            INSERT INTO flights (departure_airport_id, arrival_airport_id, airplane_id, departure_date, arrival_date, departure_time, arrival_time, ticket_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query_add_return_flight, (
                    departure_airport_id,
                    arrival_airport_id, 
                    airplane_id, 
                    departure_date,
                    arrival_date,
                    departure_time,
                    arrival_time,
                    ticket_price
                ))
                conn.commit()  

    def create_booking(self, user_id: int, flight_id: int, passport_number: int, passport_seria : int, status : str = "Ожидает"):
        query = """
            INSERT INTO bookings (user_id, flight_id, passport_number, passport_seria, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING booking_id;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    user_id, 
                    flight_id, 
                    passport_number,
                    passport_seria,
                    status
                ))
                result = cur.fetchone()
                if result:
                    booking_id = result[0] 
                else:
                    booking_id = None
            conn.commit()

        return booking_id



    def update_available_tickets(self, flight_id : int):
        query = """
            UPDATE airplanes
            SET available_tickets = available_tickets - 1
            WHERE airplane_id = (SELECT airplane_id FROM flights WHERE flight_id = %s)
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    flight_id,
                ))
            conn.commit()
    
    def get_all_flights(self):
        query = """
            SELECT f.flight_id, a1.city AS departure_city, a2.city AS arrival_city, 
                   f.departure_date, f.departure_time, f.arrival_date, f.arrival_time, 
                   air.model AS airplane_model
            FROM flights f
            JOIN airports a1 ON f.departure_airport_id = a1.airport_id
            JOIN airports a2 ON f.arrival_airport_id = a2.airport_id
            JOIN airplanes air ON f.airplane_id = air.airplane_id
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
            
    def delete_flight(self, flight_id: int):
        query = """
            DELETE FROM flights
            WHERE flight_id = %(flight_id)s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {
                    "flight_id": flight_id
                })
                conn.commit()
    
    def update_airplane_availability(self, flight_id: int):
        query = """
            SELECT airplane_id FROM flights WHERE flight_id = %(flight_id)s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {
                    "flight_id": flight_id
                })
                airplane_id = cur.fetchone()
                
                if airplane_id:
                    update_query = """
                        UPDATE airplanes SET is_available = TRUE
                        WHERE airplane_id = %(flight_id)s
                    """
                    cur.execute(update_query, {
                        "airplane_id": airplane_id[0]
                    })
                    conn.commit()
            
    def update_booking_status(self, booking_id : int, status : str = "Подтверждено"):
        query = """
        UPDATE bookings
        SET status = %s
        WHERE booking_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    status,
                    booking_id
                ))
            conn.commit()
            
    def get_bookings(self, user_id : int):
        query = """
            SELECT 
                b.booking_id, 
                b.flight_id, 
                u.first_name || ' ' || u.last_name AS passenger_name,  
                b.passport_number, 
                b.passport_seria, 
                b.booking_date, 
                COALESCE(p.status, 'Не оплачено') AS status
            FROM bookings b
            LEFT JOIN payments p ON b.booking_id = p.booking_id
            LEFT JOIN users u ON b.user_id = u.user_id
            WHERE b.user_id = %s AND (p.status != 'Отменен' OR p.status IS NULL)
            ORDER BY b.booking_date DESC
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    user_id,
                ))
                columns = [desc[0] for desc in cur.description]
                bookings = [dict(zip(columns, row)) for row in cur.fetchall()]
        
        return bookings
    
    def get_booking_info(self, booking_id : int):
        query = """
            SELECT u.first_name || ' ' || u.last_name AS passenger_name, f.ticket_price AS price
            FROM bookings b
            JOIN flights f ON b.flight_id = f.flight_id
            JOIN airplanes air ON f.airplane_id = air.airplane_id
            JOIN users u ON b.user_id = u.user_id
            WHERE b.booking_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    booking_id,
                ))
                result = cur.fetchone()
                if result:
                    return {
                        'passenger_name': result[0],
                        'price': result[1]
                    }
                else:
                    return None
    