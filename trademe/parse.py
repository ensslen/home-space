#!/usr/bin/python3

import json
import pprint
import re
#import StringIO


import lxml.etree


def etree_parse(html):
    parser = lxml.etree.HTMLParser()
    tree = lxml.etree.parse(StringIO(html), parser)
    return tree




def extract_json(html):
    m = re.search(r'(?x) MapBasedSearch \. initialiseMbs \( ( { .* ) \) ;', html)
    assert m
    data = json.loads(m.group(1))
    return data

def extract_addresses(html):
    import lxml.html
    doc = lxml.html.fromstring(html)
    links = doc.cssselect('a.dotted')
    listings = {}
    for link in links:
        href = link.get('href')
        listing_id = re.search(r'(?x) auction-(\d+) \. htm $', href).group(1)
        address = link.text_content()
        listings[listing_id] = {'href': href, 'address': address}
    return listings


if __name__ == '__main__':
    html = open('wgtn-flats.html').read()
    listings = extract_addresses(html)
    listing_data = extract_json(html)
    for listing_id, data in listing_data['MarkerInfoViewModels'].items():
        assert listing_id in listings
        suburb, town = data['LocationDetails'].split(',')
        listings[listing_id].update(
            bedrooms=data['NumberOfBedrooms'],
            bathrooms=data['NumberOfBathrooms'],
            suburb=data['LocationDetails'],
            available=data['Availability'],         # TODO parse
            price=data['PropertyPrice'],            # TODO parse
        )

    pprint.pprint(listings)

    #print('data keys:\n', data['MarkerInfoViewModels'].keys())
    #pprint.pprint(data['MarkerInfoViewModels'].popitem())

