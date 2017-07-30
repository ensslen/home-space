#!/usr/bin/python3

import json


def row(flat):
    direct_sun = 'Unknown'
    if flat['sunlight']['direct_kwh']:
        direct_sun = '{:d} kwh/m2'.format(flat['sunlight']['direct_kwh'])
    else:
        flat['sunlight']['direct_kwh'] = 0
    total_sun = 'Unknown'
    if flat['sunlight']['total_kwh']:
        total_sun = '{:d} kwh/m2'.format(flat['sunlight']['total_kwh'])
    else:
        flat['sunlight']['total_kwh'] = 0
    return '''
    <tr>
        <td><a href="{flat[trademe][link]}" class="thumb"><img src="{flat[trademe][thumbnail]}"></a></td>
        <td><a href="{flat[trademe][link]}">{flat[address_text]}</a></td>
        <td>{flat[address][suburb]}</td>
        <td>{flat[trademe][bedrooms]}</td>
        <td>{flat[trademe][bathrooms]}</td>
        <td data-sort="{flat[trademe][rent]}">${flat[trademe][rent]:,d}/wk</td>
        <td data-sort="{flat[trademe][available_epoch]}">{flat[trademe][available]}</td>
        <td data-sort="{flat[sunlight][direct_kwh]}">{direct_sun}</td>
        <td data-sort="{flat[sunlight][total_kwh]}">{total_sun}</td>
    </tr>
    '''.format(**locals())


def gen():
    data = json.load(open('data.json'))
    style = '''
        body { width: 960px; margin: 0 auto; font-family: 'Open Sans', sans-serif; font-size: 16px; }
        h1 { font-size: 2.4em; font-family: 'Poiret One', sans-serif; }
        p { font-size: 1.2em; font-family: 'Poiret One', sans-serif; }
        table#flats { font-family: 'Open Sans Condensed'; font-size: 0.9em; margin-top: 5em; }
        table#flats td { white-space: nowrap; }
        table#flats th { white-space: nowrap; padding-right: 10px; position: relative; }

        /* tablesort.css */
        th[role=columnheader]:not(.no-sort) { cursor: pointer; }
        th[role=columnheader]:not(.no-sort):after {
            content: '';
            position: absolute;
            top: 50%;
            right: 2px;
            border-width: 0 4px 4px;
            border-style: solid;
            border-color: #404040 transparent;
            visibility: hidden;
            opacity: 0;
            -ms-user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            user-select: none;
        }
        th[aria-sort=ascending]:not(.no-sort):after { border-bottom: none; border-width: 4px 4px 0; }
        th[aria-sort]:not(.no-sort):after { visibility: visible; opacity: 0.4; }
        th[role=columnheader]:not(.no-sort):hover:after { visibility: visible; opacity: 1; }
    '''
    fonts = 'Open+Sans|Open+Sans+Condensed:300,700|Poiret+One'
    tbody = '\n'.join(row(flat) for flat in data)
    return '''
        <!DOCTYPE html>
        <html>
          <head>
            <title>welly.space</title>
            <script src="https://cdn.rawgit.com/tristen/tablesort/v5.0.1/dist/tablesort.min.js"></script>
            <script src="https://cdn.rawgit.com/tristen/tablesort/v5.0.1/dist/sorts/tablesort.number.min.js"></script>
            <link rel="stylesheet" href="https://cdn.rawgit.com/tristen/tablesort/v5.0.1/demo/style.css">
            <style>@import url('https://fonts.googleapis.com/css?family={fonts}');</style>
            <style>{style}</style>
          </head>
          <body>
            <h1>welly.space</h1>
            <p>Sunlight is at a premium in this town, so we're helping you to find the
            sunniest flats possible!</p>
            <table id="flats">
              <thead>
                <tr>
                    <th colspan=7>Flat info</th>
                    <th colspan=2>Sunlight</th>
                </tr>
                <tr class="sort-header" data-sort-method="thead">
                    <th data-sort-method="none">Photo</th>
                    <th data-sort-method="none">Address</th>
                    <th class="sortable">Suburb</th>
                    <th class="sortable">Bedrooms</th>
                    <th class="sortable">Bathrooms</th>
                    <th class="sortable">Rent</th>
                    <th class="sortable">Available</th>
                    <th class="sortable">Direct</th>
                    <th class="sortable" data-sort-default>Total</th>
                </tr>
              </thead>
              <tbody>
                {tbody}
              </tbody>
            </table>
            <script>
              new Tablesort(document.getElementById("flats"), {{descending: true}});
            </script>
          </body>
        </html>'''.format(**locals())



if __name__ == '__main__':
    with open('data.html', 'w') as f:
        f.write(gen())
