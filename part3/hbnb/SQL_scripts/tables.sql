-- Table USERS
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Table PLACES
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TRIGGER update_places_updated_at
AFTER UPDATE ON places
FOR EACH ROW
BEGIN
    UPDATE places SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Table REVIEWS
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY, 
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    CONSTRAINT user_unique_place_review UNIQUE (user_id, place_id)
);

CREATE TRIGGER update_reviews_updated_at
AFTER UPDATE ON reviews
FOR EACH ROW
BEGIN
    UPDATE reviews SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Table AMENITIES
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY, 
    name VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_amenities_updated_at
AFTER UPDATE ON amenities
FOR EACH ROW
BEGIN
    UPDATE amenities SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Table PLACE_AMENITY
CREATE TABLE place_amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
