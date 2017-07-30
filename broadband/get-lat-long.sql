select ST_X(wgtn_addr.address_point), ST_Y(wgtn_addr.address_point), tr_addr.address_id from trademe tm
    inner join trademe_addr tr_addr on (
      tr_addr.listing_id = tm.listing_id
    )
    inner join wgtn_addresses wgtn_addr on (
      wgtn_addr.address_id = tr_addr.address_id
    );