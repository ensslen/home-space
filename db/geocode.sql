BEGIN;


DROP TABLE IF EXISTS trademe_addr;
CREATE TABLE trademe_addr (
    listing_id INTEGER NOT NULL,
    address_id INTEGER NOT NULL REFERENCES wgtn_addresses,
    score INTEGER
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


DROP FUNCTION IF EXISTS extract_digits(house TEXT);
CREATE FUNCTION extract_digits(house TEXT)
RETURNS TEXT
LANGUAGE sql AS $$
    SELECT SUBSTRING(house FROM '(\d+)');
$$;


DROP FUNCTION IF EXISTS extract_digitsplus(house TEXT);
CREATE FUNCTION extract_digitsplus(house TEXT)
RETURNS TEXT
LANGUAGE sql AS $$
    SELECT SUBSTRING(house FROM '(\d+[A-Z]*)');
$$;


DROP FUNCTION IF EXISTS geomatch_score(TRADEME, WGTN_ADDRESSES);
CREATE FUNCTION geomatch_score(listing TRADEME, address WGTN_ADDRESSES)
RETURNS INT
LANGUAGE plpgsql AS $$
DECLARE
    score INT := 0; 
BEGIN
    -- +40 pts for exact match of unit
    -- +40 pts if neither address has a unit
    -- +30 pts for digit+alpha match of unit
    -- +20 pts for digit match of unit
    IF (listing.unit = address.unit) THEN
        score := score + 40;
    ELSIF (listing.unit IS NULL AND address.unit IS NULL) THEN
        score := score + 40;
    ELSIF (extract_digitsplus(listing.unit) = extract_digitsplus(address.unit)) THEN
        score := score + 30;
    ELSIF (extract_digits(listing.unit) = extract_digits(address.unit)) THEN
        score := score + 20;
    END IF;

    -- +40 pts for exact match of house number
    -- +30 pts for digit+alpha match of house number
    -- +20 pts for digit match of house number
    IF (listing.house = address.house) THEN
        score := score + 40;
    ELSIF (extract_digitsplus(listing.house) = extract_digitsplus(address.house)) THEN
        score := score + 30;
    ELSIF (extract_digits(listing.house) = extract_digits(address.house)) THEN
        score := score + 20;
    END IF;

    -- +10 pts for suburb match
    IF (listing.suburb = address.suburb) THEN
        score := score + 10;
    END IF;

    RETURN score;
END;
$$;


\echo 'Starting the geocoding...'
INSERT INTO trademe_addr (listing_id, address_id, score)
WITH matches AS (
    -- Join to addresses using street name, then score each candidate
    SELECT listing_id, address_id, geomatch_score(tm, addr) AS score,
           row_number() OVER (PARTITION BY listing_id ORDER BY geomatch_score(tm, addr) DESC) AS ranking
    FROM trademe tm 
    JOIN wgtn_addresses addr 
    ON (canonical_street(tm.street) = addr.street AND
        extract_digits(tm.house) = extract_digits(addr.house))
)
-- Use a window query to select the best-ranked address point for each listing
SELECT listing_id, address_id, score
FROM matches
WHERE ranking = 1
;


-- Report geocoding success
\echo '\n\nGeocoding success report\n'
select
    count(distinct trademe.listing_id) as "Total listings",
    count(distinct addr.listing_id) as "Listings with location",
    TO_CHAR(count(distinct addr.listing_id)::float/count(distinct trademe.listing_id)*100, '99D9%') as "Success rate"
from trademe
left join (select distinct listing_id from trademe_addr) addr using (listing_id)
;

\echo '\n\nDetailed scoring report\n'
select score as "Score",
       count(*) as "Count",
       TO_CHAR(sum(count(*)) over (order by score desc)::float/sum(count(*)) over ()*100, '999D9%') as "Cumulative percentage" 
from trademe_addr
group by score
order by score desc;


COMMIT;
