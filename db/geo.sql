BEGIN;

-- Load the original source data
\i ../geo/sql/building_solar_radiation.sql
\i ../geo/sql/nz_land_parcels.sql
\i ../geo/sql/nz_street_address.sql


-- Reproject the solar radiation data
CREATE TABLE wgtn_sunlight AS
SELECT objectid		AS building_id,
	   mean_direc	AS direct_solar_mean,
	   max_direct   AS direct_solar_max,
	   mean_globa   AS total_solar_mean,
	   max_sol_kw   AS total_solar_max,
	   ST_Transform(building_poly, 2193)::GEOMETRY(Polygon,2193) AS building_poly
FROM building_solar_radiation
;

CREATE INDEX wgtn_sunlight_idx ON wgtn_sunlight USING GIST (building_poly);


-- Partition the Wellington parcels
CREATE TABLE wgtn_parcels AS
SELECT id           AS parcel_id,
       appellatio   AS legal_desc,
       titles,
       survey_are   AS survey_area,
       parcel_poly
FROM nz_land_parcels
WHERE land_distr='Wellington'
;

CREATE INDEX wgtn_parcels_idx ON wgtn_parcels USING GIST (parcel_poly);


-- Partition the Wellington addresses
CREATE TABLE wgtn_addresses AS
SELECT UPPER(substring(full_addre from '([^/]*)/.*'))       AS unit,
       UPPER(substring(full_addre from '(?:[^/]*/)?(.*)'))  AS house,
       UPPER(full_road_)                                    AS street,
       UPPER(suburb_loc)                                    AS suburb,
       address_point
FROM nz_street_address
WHERE town_city='Wellington'
;

CREATE INDEX wgtn_addresses_idx ON wgtn_addresses USING GIST (address_point);
CREATE INDEX wgtn_addresses_street ON wgtn_addresses (suburb, street, house, unit);


COMMIT;
