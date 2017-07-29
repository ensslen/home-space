BEGIN;


DROP TABLE IF EXISTS trademe_addr;
CREATE TABLE trademe_addr (
    listing_id INTEGER NOT NULL,
    address_id INTEGER NOT NULL REFERENCES wgtn_addresses
);


DROP FUNCTION IF EXISTS geomatch(TRADEME, WGTN_ADDRESSES);
CREATE FUNCTION geomatch(listing TRADEME, address WGTN_ADDRESSES)
RETURNS BOOLEAN
LANGUAGE sql AS $$
    SELECT (listing.unit IS NULL OR listing.unit = address.unit)
       AND (listing.house = address.house)
       AND (listing.street = address.street);
$$;


\echo 'Starting the geocoding...'
INSERT INTO trademe_addr (listing_id, address_id)
SELECT listing_id, address_id
FROM trademe tm LEFT JOIN wgtn_addresses addr ON (geomatch(tm, addr))
WHERE addr.address_point IS NOT NULL
;


COMMIT;
