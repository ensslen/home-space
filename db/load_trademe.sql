BEGIN;


DROP TABLE IF EXISTS trademe;


CREATE TABLE trademe (
    listing_id INTEGER PRIMARY KEY,
    listed DATE NOT NULL,
    available DATE NOT NULL,

    -- address fields
    unit TEXT,
    house TEXT,
    street TEXT NOT NULL,
    suburb TEXT NOT NULL,
    city TEXT NOT NULL,
    
    -- weekly rental in NZD
    price INTEGER CHECK (price > 0),
    
    bedrooms TEXT,
    bathrooms TEXT,
    href TEXT,
    photo TEXT
);


ALTER TABLE trademe OWNER TO govhack_user;


\copy trademe (listing_id, listed, available, unit, house, street, suburb, city, price, bedrooms, bathrooms, href, photo) from ../trademe/trademe-sample-data.csv with csv header


COMMIT;
