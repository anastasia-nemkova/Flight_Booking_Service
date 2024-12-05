from repositories.payment import PaymentRepository

class PaymentService:
    def __init__(self) :
        self.repo = PaymentRepository()
        
    def create_payment(self, booking_id : int, amount : int, card_number : int, card_expiry : int, card_cvc : int) :
        return self.repo.create_payment(booking_id, amount, card_number, card_expiry, card_cvc)
    
    def update_payment_status(self, payment_id : int, status : str) :
        return self.repo.update_payment_status(payment_id, status)
    
    def cancel_payment(self, booking_id : int) :
        return self.repo.cancel_payment(booking_id)