WITH
sunlight AS (
    SELECT listing_id,
           ROUND(AVG(direct_solar_mean),0)  AS direct_solar_mean,
           ROUND(MAX(direct_solar_max),0)   AS direct_solar_max,
           ROUND(AVG(total_solar_mean),0)   AS total_solar_mean,
           ROUND(MAX(total_solar_max),0)    AS total_solar_max
    FROM trademe_addr
    LEFT JOIN wgtn_addresses addr USING (address_id)
    LEFT JOIN wgtn_parcels ON (ST_Contains(parcel_poly, address_point))
    LEFT JOIN wgtn_sunlight ON (ST_Contains(parcel_poly, building_poly))
    GROUP BY listing_id
),
data AS (
    SELECT json_build_object(
        'id',           listing_id,
        'address',      json_build_object(
            'unit',                 trademe.unit,
            'house',                trademe.house,
            'street',               trademe.street,
            'suburb',               trademe.suburb,
            'city',                 trademe.city
        ),
        'address_text', COALESCE(trademe.unit||'/','')||trademe.house||' '||trademe.street,
        'trademe',      json_build_object(
            'listed',               trademe.listed,
            'listed_epoch',         EXTRACT(epoch FROM trademe.listed),
            'available',            trademe.available,
            'available_epoch',      EXTRACT(epoch FROM trademe.available),
            'rent',                 trademe.price,
            'bedrooms',             trademe.bedrooms,
            'bathrooms',            trademe.bathrooms,
            'link',                 trademe.href,
            'thumbnail',            trademe.photo
        ),
        'sunlight',     json_build_object(
            'direct_kwh',           sunlight.direct_solar_mean,
            'total_kwh',            sunlight.total_solar_mean
        ),
        'broadband',    json_build_object(
            'max_speed',            nz_broadband.top_speed,
            'technologies',         nz_broadband.technologies
        )
    ) AS obj
    FROM trademe
    LEFT JOIN sunlight USING (listing_id)
    LEFT JOIN trademe_addr USING (listing_id)
    LEFT JOIN nz_broadband USING (address_id)
    ORDER BY listed DESC
)

SELECT array_to_json(array_agg(obj), TRUE)
FROM data
;
