#!/usr/bin/python3

import json


def row(flat):
    address = flat['house'] + ' ' + flat['street']
    if flat['unit']:
        address = flat['unit'] + '/' + address
    sunlight = 'Unknown' if not flat['avg_sunlight_kwh'] else '{:d} kwh/m2'.format(flat['avg_sunlight_kwh'])
    return '''
    <tr>
        <td><img src="{flat[photo]}"></td>
        <td>{address}</td>
        <td>{flat[suburb]}</td>
        <td>{flat[bedrooms]}</td>
        <td>{flat[bathrooms]}</td>
        <td data-sort="{flat[price]}">${flat[price]:,d}</td>
        <td data-sort="{flat[available_epoch]}">{flat[available]}</td>
        <td data-sort="{flat[avg_sunlight_kwh]}">{sunlight}</td>
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
                <th>Sunshine</th>
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
