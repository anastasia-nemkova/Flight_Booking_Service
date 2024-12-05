from repositories.connector import get_connection

class UserRepository:
    def get_user_by_email(self, email: str):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {
                    "email": email
                })
                return cur.fetchone()

    def add_user(self, first_name: str, last_name: str, email: str, password_hash: str, role: str = "user"):
        query = """
            INSERT INTO users (first_name, last_name, email, password_hash, role)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, %(role)s);
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password_hash": password_hash,
                    "role": role
                })
                conn.commit()
                
    def get_user_info(self, user_id):
        query = "SELECT first_name, last_name FROM users WHERE user_id = %s"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    user_id,
                ))
                result = cur.fetchone()
                if result:
                    return {'first_name': result[0], 'last_name': result[1]}
                else:
                    raise Exception("Пользователь не найден.")
