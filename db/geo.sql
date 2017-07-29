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


COMMIT;
