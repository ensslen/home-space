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
        /*table#flats { font-family: 'Open Sans Condensed'; font-size: 0.9em; margin-top: 5em; } */
        .dataTables_wrapper { font-family: 'Open Sans Condensed'; font-size: 0.9em; }
        table#flats { margin-top: 5em; }
        table#flats img { width: 160px; min-height: 120px; max-height: 120px; }
        table#flats a { font-weight: bold; color: #666; }
        table#flats td { white-space: nowrap; vertical-align: top; }
        table#flats th { white-space: nowrap; }
        table#flats tbody td { border-bottom: 1px solid #aaa; }
    '''
    fonts = 'Open+Sans|Open+Sans+Condensed:300,700|Poiret+One'
    tbody = '\n'.join(row(flat) for flat in data)
    return '''
        <!DOCTYPE html>
        <html>
          <head>
            <title>welly.space</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/datatables/1.10.15/js/jquery.dataTables.min.js"></script>
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css">
            <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family={fonts}">
            <style>{style}</style>
          </head>
          <body>
            <h1>welly.space</h1>
            <p>Sunlight is at a premium in this town, so we're helping you to find the
            sunniest flats possible!</p>
            <table id="flats">
              <thead>
                <tr>
                    <th colspan=7></th>
                    <th colspan=2>Sunlight</th>
                </tr>
                <tr class="sort-header">
                    <th data-orderable="false">Photo</th>
                    <th data-orderable="false">Address</th>
                    <th class="sortable">Suburb</th>
                    <th class="sortable">Bedrooms</th>
                    <th class="sortable">Bathrooms</th>
                    <th class="sortable">Rent</th>
                    <th class="sortable">Available</th>
                    <th class="sortable">Direct</th>
                    <th class="sortable">Total</th>
                </tr>
              </thead>
              <tbody>
                {tbody}
              </tbody>
            </table>
            <script>
                $(document).ready(function(){{
                    $('#flats').DataTable({{
                        "order": [[8, "desc"]],
                        "pageLength": 25,
                        "lengthChange": false,
                    }});
                }});
            </script>
          </body>
        </html>'''.format(**locals())



if __name__ == '__main__':
    with open('data.html', 'w') as f:
        f.write(gen())
