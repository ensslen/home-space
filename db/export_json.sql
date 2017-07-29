WITH rentals AS (
    select tm.*,
        extract(epoch from tm.available) as available_epoch,
        extract(epoch from tm.listed) as listed_epoch,
        ROUND(AVG(direct_solar_mean),0) AS avg_sunlight_kwh
    from trademe tm 
    left join trademe_addr using (listing_id)
    left join wgtn_addresses addr using (address_id)
    left join wgtn_parcels on (ST_Contains(parcel_poly, address_point))
    left join wgtn_sunlight on (ST_Contains(parcel_poly, building_poly))
    group by listing_id
)
SELECT array_to_json(array_agg(row_to_json(rentals.*)),TRUE)
FROM rentals
;
