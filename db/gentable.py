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
        <td><img src="{flat[trademe][thumbnail]}"></td>
        <td>{flat[address_text]}</td>
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
    style = 'body { width: 960px; margin: 0 auto; }'
    tbody = '\n'.join(row(flat) for flat in data)
    return '''
        <!DOCTYPE html>
        <html>
          <head>
            <title>WELLY.SPACE</title>
            <script src="https://cdn.rawgit.com/tristen/tablesort/v5.0.1/dist/tablesort.min.js"></script>
            <script src="https://cdn.rawgit.com/tristen/tablesort/v5.0.1/dist/sorts/tablesort.number.min.js"></script>
            <link rel="stylesheet" href="https://cdn.rawgit.com/tristen/tablesort/v5.0.1/demo/style.css">
            <style>{style}</style>
          </head>
          <body>
            <h1>WELLY.SPACE</h1>
            <table id="flats">
              <thead>
                <th>Photo</th>
                <th>Address</th>
                <th>Suburb</th>
                <th>Bedrooms</th>
                <th>Bathrooms</th>
                <th>Rent</th>
                <th>Available</th>
                <th>Direct sun</th>
                <th>Total sun</th>
              </thead>
              <tbody>
                {tbody}
              </tbody>
            </table>
            <script>
              new Tablesort(document.getElementById("flats"));
            </script>
          </body>
        </html>'''.format(style=style, tbody=tbody)



if __name__ == '__main__':
    with open('data.html', 'w') as f:
        f.write(gen())
