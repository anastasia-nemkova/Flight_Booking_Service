-- Добавление информации о аэропортах 
INSERT INTO 
    airports (name, iata_code, city) 
VALUES 
    (
        'Шереметьево', 
        'SVO', 
        'Москва'
    ),
    (
        'Домодедово', 
        'DME', 
        'Москва'
    ),
    (
        'Пулково', 
        'LED', 
        'Санкт-Петербург'
    ),
    (
        'Кольцово', 
        'SVX', 
        'Екатеринбург'
    ),
    (
        'Толмачево', 
        'OVB', 
        'Новосибирск'
    ),
    (
        'Внуково', 
        'VKO', 
        'Москва'
    ),
    (
        'Казань', 
        'KZN', 
        'Казань'
    ),
    (
        'Сочи', 
        'AER', 
        'Сочи'
    ),
    (
        'Уфа', 
        'UFA', 
        'Уфа'
    ),
    (
        'Краснодар', 
        'KRR', 
        'Краснодар'
    );

-- Добавлении информации о самолётах
INSERT INTO 
    airplanes (model, available_tickets) 
VALUES 
    (
        'Airbus A320', 
        180
    ),
    (
        'Boeing 737', 
        200
    ),
    (
        'Sukhoi Superjet 100', 
        98
    ),
    (
        'Bombardier CRJ-200', 
        50
    ),
    (
        'Ту-204', 
        210
    ),
    (
        'Ил-96-300', 
        262
    ),
    (
        'Embraer E190', 
        106
    );

--- Добавим несколько админов
INSERT INTO 
    users (first_name, last_name, email, password_hash, role)
VALUES
    (
        'Алекс', 
        'Иванов', 
        'admin@example.com', 
        '$2b$12$WWivymLjMT2MYLQxwY7UsOuU21u52rbPckBK1XB5guOQUC/FlQ0Uu', --admin123
        'admin'
    ),
    (
        'Сергей', 
        'Романов', 
        'superadmin@example.com', 
        '$2b$12$1eQRCLcl0QfQ2jUunoHVx.hLwV.zaPiB8NtaP8k9b6nEBWmjsuMbO', --superadmin123
        'admin'
    );