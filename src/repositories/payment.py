from datetime import datetime
from repositories.connector import get_connection

class PaymentRepository:
    def create_payment(self, booking_id : int, amount : int, card_number : int, card_expiry : int, card_cvc : int) :
        query = """
            INSERT INTO payments (booking_id, payment_date, amount, status, card_number, card_expiry, card_cvc)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING payment_id;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                payment_date = datetime.now().date()
                cur.execute(query, (
                    booking_id, 
                    payment_date, 
                    amount, 
                    "Не оплачено", 
                    card_number, 
                    card_expiry, 
                    card_cvc
                ))
                payment_id = cur.fetchone()[0]
            conn.commit()
        return payment_id

    def update_payment_status(self, payment_id : int, status : str) :
        query = """
            UPDATE payments
            SET status = %s
            WHERE payment_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    status, 
                    payment_id
                ))
            conn.commit()
            
    def cancel_payment(self, booking_id: int) :
        query_update_booking = """
            UPDATE bookings
            SET status = 'Отменен'
            WHERE booking_id = %s
        """
        query_update_payment = """
            UPDATE payments
            SET status = 'Отменен'
            WHERE booking_id = %s
        """
        query_increase_tickets = """
            UPDATE airplanes
            SET available_tickets = available_tickets + 1
            WHERE airplane_id = (
                SELECT airplane_id
                FROM flights
                WHERE flight_id = (
                    SELECT flight_id
                    FROM bookings
                    WHERE booking_id = %s
                )
            )
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query_update_booking, (
                    booking_id,
                ))
                cur.execute(query_update_payment, (
                    booking_id,
                ))
                cur.execute(query_increase_tickets, (
                    booking_id,
                ))
            conn.commit()