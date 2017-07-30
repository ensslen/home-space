BEGIN;


DROP TABLE IF EXISTS nz_broadband;


CREATE TABLE nz_broadband (
    address_id      INTEGER     PRIMARY KEY REFERENCES wgtn_addresses,
    technologies    TEXT[]      NOT NULL,
    providers       TEXT[]      NOT NULL,
    top_speed       INTEGER     NOT NULL
);


ALTER TABLE nz_broadband OWNER TO govhack_user;


\copy nz_broadband (address_id, technologies, providers, top_speed) from ../broadband/broadband.csv with csv header


COMMIT;
