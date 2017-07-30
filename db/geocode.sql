BEGIN;


DROP TABLE IF EXISTS trademe_addr;
CREATE TABLE trademe_addr (
    listing_id INTEGER NOT NULL,
    address_id INTEGER NOT NULL REFERENCES wgtn_addresses
);
ALTER TABLE trademe_addr OWNER TO govhack_user;


DROP FUNCTION IF EXISTS canonical_street(TEXT);
CREATE FUNCTION canonical_street(name TEXT)
RETURNS TEXT
LANGUAGE plpgsql AS $$
DECLARE
    street_name TEXT := SUBSTRING(name FROM '^(.+?)\s+[A-Z]+$');
    street_suffix TEXT := SUBSTRING(name FROM '^.+?\s+([A-Z]+)$');
BEGIN
    RETURN street_name||' '||CASE street_suffix
        WHEN 'ST'   THEN 'STREET'
        WHEN 'RD'   THEN 'ROAD'
        WHEN 'TCE'  THEN 'TERRACE'
        WHEN 'PDE'  THEN 'PARADE'
        WHEN 'AVE'  THEN 'AVENUE'
        ELSE street_suffix
    END;
END;
$$;


DROP FUNCTION IF EXISTS house_digits(house TEXT);
CREATE FUNCTION house_digits(house TEXT)
RETURNS TEXT
LANGUAGE sql AS $$
    SELECT SUBSTRING(house FROM '(\d+)');
$$;


DROP FUNCTION IF EXISTS geomatch_score(TRADEME, WGTN_ADDRESSES);
CREATE FUNCTION geomatch_score(listing TRADEME, address WGTN_ADDRESSES)
RETURNS INT
LANGUAGE plpgsql AS $$
DECLARE
    score INT := 0; 
BEGIN
    -- +40 pts for exact match of unit
    -- +20 pts if neither address has a unit
    IF (listing.unit IS NULL AND address.unit IS NULL) THEN score := score + 20;
    ELSIF (listing.unit = address.unit) THEN score := score + 40;
    END IF;

    -- +40 pts for exact match of house numbers
    IF (listing.house = address.house) THEN
        score := score + 40;
    END IF;

    -- +10 pts for suburb match
    IF (listing.suburb = address.suburb) THEN score := score + 10; END IF;

    RETURN score;
END;
$$;


\echo 'Starting the geocoding...'
INSERT INTO trademe_addr (listing_id, address_id)
WITH matches AS (
    -- Join to addresses using street name, then score each candidate
    SELECT listing_id, address_id, geomatch_score(tm, addr) AS score,
           row_number() OVER (PARTITION BY listing_id ORDER BY geomatch_score(tm, addr) DESC) AS ranking
    FROM trademe tm 
    JOIN wgtn_addresses addr 
    ON (canonical_street(tm.street) = addr.street AND
        house_digits(tm.house) = house_digits(addr.house))
)
-- Use a window query to select the best-ranked address point for each listing
SELECT listing_id, address_id
FROM matches
WHERE ranking = 1
;


COMMIT;
