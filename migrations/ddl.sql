-- Таблица для хранения информации об аэропортах
CREATE TABLE airports (
    airport_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    iata_code VARCHAR(3) NOT NULL,
    city VARCHAR(50) NOT NULL
);

COMMENT ON TABLE airports IS 'Информация об аэропортах';
COMMENT ON COLUMN airports.airport_id IS 'Уникальный идентификатор аэропорта';
COMMENT ON COLUMN airports.name IS 'Название аэропорта';
COMMENT ON COLUMN airports.iata_code IS 'Код ИАТА аэропорта';
COMMENT ON COLUMN airports.city IS 'Город расположения аэропорта';

-- Таблица для хранения информации о самолетах
CREATE TABLE airplanes (
    airplane_id SERIAL PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    available_tickets INT NOT NULL CHECK (available_tickets >= 0)
);

COMMENT ON TABLE airplanes IS 'Информация о самолетах';
COMMENT ON COLUMN airplanes.airplane_id IS 'Уникальный идентификатор самолета';
COMMENT ON COLUMN airplanes.model IS 'Модель самолета';
COMMENT ON COLUMN airplanes.available_tickets IS 'Количество свободных мест';

-- Таблица для хранения информации о пользователях
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'admin'))
);

COMMENT ON TABLE users IS 'Информация о пользователях';
COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN users.first_name IS 'Имя пользователя';
COMMENT ON COLUMN users.last_name IS 'Фамилия пользователя';
COMMENT ON COLUMN users.email IS 'Email пользователя';
COMMENT ON COLUMN users.password_hash IS 'Хеш пароля пользователя';
COMMENT ON COLUMN users.role IS 'Роль пользователя (например, "admin", "user")';

-- Таблица для хранения информации о рейсах
CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    departure_airport_id INT NOT NULL,
    arrival_airport_id INT NOT NULL,
    airplane_id INT NOT NULL,
    arrival_date DATE NOT NULL,
    departure_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    ticket_price DECIMAL(10, 2) NOT NULL CHECK (ticket_price > 0),
    FOREIGN KEY (departure_airport_id) REFERENCES airports(airport_id),
    FOREIGN KEY (arrival_airport_id) REFERENCES airports(airport_id),
    FOREIGN KEY (airplane_id) REFERENCES airplanes(airplane_id)
);

COMMENT ON TABLE flights IS 'Информация о рейсах';
COMMENT ON COLUMN flights.flight_id IS 'Уникальный идентификатор рейса';
COMMENT ON COLUMN flights.departure_airport_id IS 'Идентификатор аэропорта отправления';
COMMENT ON COLUMN flights.arrival_airport_id IS 'Идентификатор аэропорта прибытия';
COMMENT ON COLUMN flights.airplane_id IS 'Идентификатор самолета';
COMMENT ON COLUMN flights.arrival_date IS 'Дата прибытия';
COMMENT ON COLUMN flights.departure_date IS 'Дата отправления';
COMMENT ON COLUMN flights.arrival_time IS 'Время прибытия';
COMMENT ON COLUMN flights.departure_time IS 'Время отправления';
COMMENT ON COLUMN flights.ticket_price IS 'Стоимость билета';

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY, 
    user_id INT NOT NULL,
    flight_id INT NOT NULL, 
    passport_number INT NOT NULL,
    passport_seria INT NOT NULL,
    booking_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);

COMMENT ON TABLE bookings IS 'Информация о бронированиях';
COMMENT ON COLUMN bookings.booking_id IS 'Уникальный идентификатор бронирования';
COMMENT ON COLUMN bookings.user_id IS 'Идентификатор пользователя, который сделал бронирование';
COMMENT ON COLUMN bookings.flight_id IS 'Идентификатор рейса, на который было сделано бронирование';
COMMENT ON COLUMN bookings.passport_number IS 'Номер паспорта';
COMMENT ON COLUMN bookings.passport_seria IS 'Серия паспорта';
COMMENT ON COLUMN bookings.booking_date IS 'Дата бронирования';
COMMENT ON COLUMN bookings.status IS 'Статус бронирования';

-- Таблица для хранения информации о платежах
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    status VARCHAR(50) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    card_expiry VARCHAR(7) NOT NULL,
    card_cvc VARCHAR(4) NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);

COMMENT ON TABLE payments IS 'Информация о платежах';
COMMENT ON COLUMN payments.payment_id IS 'Уникальный идентификатор платежа';
COMMENT ON COLUMN payments.booking_id IS 'Идентификатор бронирования, к которому привязан платеж';
COMMENT ON COLUMN payments.payment_date IS 'Дата платежа';
COMMENT ON COLUMN payments.amount IS 'Сумма платежа';
COMMENT ON COLUMN payments.status IS 'Статус платежа';
COMMENT ON COLUMN payments.card_number IS 'Номер карты';
COMMENT ON COLUMN payments.card_expiry IS 'Срок действия карты';
COMMENT ON COLUMN payments.card_cvc IS 'CVC';

-- Создание таблицы для логирования добавления рейсов
CREATE TABLE flight_logs (
    log_id SERIAL PRIMARY KEY,
    flight_id INT NOT NULL,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action VARCHAR(50) NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);


-- Функция для логирования добавления рейсов
CREATE OR REPLACE FUNCTION log_flight_insertion() 
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO flight_logs (flight_id, action, action_time)
    VALUES (NEW.flight_id, 'Flight Added', CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для записи в журнал при добавлении рейса
CREATE TRIGGER flight_insert_trigger
AFTER INSERT ON flights
FOR EACH ROW
EXECUTE FUNCTION log_flight_insertion();