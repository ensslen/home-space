select ST_X(address_point), ST_Y(address_point), address_id from
    ( select distinct address_id from trademe_addr) x
    join wgtn_addresses using (address_id);