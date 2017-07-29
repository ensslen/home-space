WITH rentals AS (
    select tm.*,
        ROUND(AVG(direct_solar_mean),0) AS avg_sunlight_kwh
    from trademe tm 
    left join wgtn_addresses addr on (
        (tm.unit IS NULL OR tm.unit = addr.unit)
    AND (tm.house = addr.house)
    AND (tm.street = addr.street)
    )
    left join wgtn_parcels on (ST_Contains(parcel_poly, address_point))
    left join wgtn_sunlight on (ST_Contains(parcel_poly, building_poly))
    group by listing_id
)
SELECT array_to_json(array_agg(row_to_json(rentals.*)),TRUE)
FROM rentals
;
