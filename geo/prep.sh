#!/bin/sh
set -e      # errexit
set -u      # nounset

# Make sure our datadirs exist
[ -d data ] || mkdir data
[ -d sql ] || mkdir sql

abort() {
    echo $1
    exit 1
}

# Fetch/verify that data exists
fetch() {
    local file="$1"
    local url="${2:-}"
    echo " * Checking '$file'..."
    if ! [ -f "$file" ]; then
        if [ -z "$url" ]; then
            abort "Need file but don't have a URL for it!"
        fi
        wget -O "$file" "$url"
    fi
}


###


# WCC Building Solar Radiation
#
# url:      http://data-wcc.opendata.arcgis.com/datasets/794ab26ae3004fa4ab553470adb9215f_0
# format:   shapefile
# proj:     ?
fetch data/building_solar_radiation.zip http://data-wcc.opendata.arcgis.com/datasets/794ab26ae3004fa4ab553470adb9215f_0.zip
if ! [ -f sql/building_solar_radiation.sql ]; then
    curdir=$(pwd)
    tmpdir=$(mktemp --directory)
    (cd $tmpdir; unzip "$curdir"/data/building_solar_radiation.zip)
    # data is in WGS84 (SRID 4326) so we need to reproject
    #   -I  create index
    #   -S  don't need MULTIPOLYGON
    shp2pgsql -c -D -I -S -s 2193 -g "building_poly" $tmpdir/Building_Solar_Radiation.shp building_solar_radiation > sql/building_solar_radiation.sql
    [ -d "$tmpdir" ] && rm -r "$tmpdir"
fi

# NZ Primary Land Parcels
# Must create a 'download request' via LINZ Data Service to get this data.
#
# url:      https://data.linz.govt.nz/layer/823-nz-primary-land-parcels/
# format:   shapefile
# proj:     NZGD2000
fetch data/nz_land_parcels.zip
if ! [ -f sql/nz_land_parcels.sql ]; then
    curdir=$(pwd)
    tmpdir=$(mktemp --directory)
    (cd $tmpdir; unzip "$curdir"/data/nz_land_parcels.zip)
    # parcel data is spread over three files...
    P1="$tmpdir/nz-primary-land-parcels/nz-primary-land-parcels-1.shp"
    P2="$tmpdir/nz-primary-land-parcels/nz-primary-land-parcels-2.shp"
    P3="$tmpdir/nz-primary-land-parcels/nz-primary-land-parcels-3.shp"
    # first create the schema
    #   -p  schema only
    #   -I  index the geom column
    shp2pgsql -p -s 2193 -I -g "parcel_poly" $P1 nz_land_parcels > sql/nz_land_parcels.sql
    # now the data; no need to reproject, already in NZGD2000 (SRID 2193)
    #   -a  append to existing table
    #   -D  binary dump format
    #   -g  set name of geom column
    shp2pgsql -a -D -s 2193 -g "parcel_poly" $P1 nz_land_parcels >> sql/nz_land_parcels.sql
    shp2pgsql -a -D -s 2193 -g "parcel_poly" $P2 nz_land_parcels >> sql/nz_land_parcels.sql
    shp2pgsql -a -D -s 2193 -g "parcel_poly" $P3 nz_land_parcels >> sql/nz_land_parcels.sql
    [ -d "$tmpdir" ] && rm -r $tmpdir
fi


# NZ Street Address
#
# url:      https://data.linz.govt.nz/layer/3353-nz-street-address/
# format:   shapefile
# proj:     NZGD2000
fetch data/nz_street_address.zip
if ! [ -f sql/nz_street_address.sql ]; then
    curdir=$(pwd)
    tmpdir=$(mktemp --directory)
    (cd $tmpdir; unzip "$curdir"/data/nz_street_address.zip)
    # parcel data is spread over three files...
    P1="$tmpdir/nz-street-address/nz-street-address-1.shp"
    P2="$tmpdir/nz-street-address/nz-street-address-2.shp"
    P3="$tmpdir/nz-street-address/nz-street-address-3.shp"
    # first create the schema
    #   -p  schema only
    #   -I  index the geom column
    #   -S  don't need MULTIPOLYGON
    shp2pgsql -p -S -s 2193 -I -g "address_point" $P1 nz_street_address > sql/nz_street_address.sql
    # now the data; no need to reproject, already in NZGD2000 (SRID 2193)
    #   -a  append to existing table
    #   -D  binary dump format
    #   -g  set name of geom column
    #   -S  don't need MULTIPOLYGON
    shp2pgsql -a -D -S -s 2193 -g "address_point" $P1 nz_street_address >> sql/nz_street_address.sql
    shp2pgsql -a -D -S -s 2193 -g "address_point" $P2 nz_street_address >> sql/nz_street_address.sql
    shp2pgsql -a -D -S -s 2193 -g "address_point" $P3 nz_street_address >> sql/nz_street_address.sql
    [ -d "$tmpdir" ] && rm -r $tmpdir
fi

