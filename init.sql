CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    hashed_password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    id_number TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    address TEXT,
    photo_url TEXT
);

CREATE TABLE cars (
    car_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    license_plate TEXT UNIQUE NOT NULL
);

CREATE TABLE police (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    badge_number TEXT UNIQUE NOT NULL,
    photo TEXT,
    hashed_password TEXT NOT NULL
);

CREATE TABLE reports (
    report_id SERIAL PRIMARY KEY,
    license_plate TEXT NOT NULL,
    report_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    photo_url TEXT,
    photo_data BYTEA,
    photo_content_type TEXT,
    full_address TEXT NOT NULL
);

CREATE TABLE violations (
    violation_id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(car_id) ON DELETE CASCADE,
    report_id INTEGER REFERENCES reports(report_id) ON DELETE SET NULL,
    report_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    has_appealed BOOLEAN DEFAULT FALSE
);

CREATE TABLE appeals (
    appeal_id SERIAL PRIMARY KEY,
    violation_id INTEGER UNIQUE NOT NULL REFERENCES violations(violation_id) ON DELETE CASCADE,
    police_id INTEGER NOT NULL REFERENCES police(id),
    status TEXT NOT NULL,
    appeal_reason TEXT
);

CREATE OR REPLACE FUNCTION create_violation_from_report()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO violations (car_id, report_id, report_time, has_appealed)
    SELECT car_id, NEW.report_id, NEW.report_time, FALSE
    FROM cars
    WHERE UPPER(license_plate) = UPPER(NEW.license_plate)
    ON CONFLICT DO NOTHING;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER reports_after_insert_create_violation
AFTER INSERT ON reports
FOR EACH ROW
EXECUTE FUNCTION create_violation_from_report();
