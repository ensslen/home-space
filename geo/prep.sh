#!/bin/sh
set -e      # errexit
set -u      # nounset


abort() {
    echo $1
    exit 1
}

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
    

[ -d data ] || mkdir data

# WCC Building Solar Radiation
#
# url:      http://data-wcc.opendata.arcgis.com/datasets/794ab26ae3004fa4ab553470adb9215f_0
# format:   shapefile
# proj:     ?
fetch data/building_solar_radiation.zip http://data-wcc.opendata.arcgis.com/datasets/794ab26ae3004fa4ab553470adb9215f_0.zip

# NZ Primary Land Parcels
# Must create a 'download request' via LINZ Data Service to get this data.
#
# url:      https://data.linz.govt.nz/layer/823-nz-primary-land-parcels/
# format:   shapefile
# proj:     NZGD2000
fetch data/nz_land_parcels.zip
