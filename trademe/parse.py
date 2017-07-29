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


def parse_price(price_text):
    m = re.match(r'^\$([0-9,]+) per week', price_text)
    assert m is not None
    return int(m.group(1).replace(',', ''))


# TODO:  clean up this parser
def parse_avail(avail_text):
    m = re.search(r'Available (.+?)[\s]*$', avail_text)
    if m is None:
        print('parse_avail: cannot parse {!r}'.format(avail_text))
    assert m is not None
    return m.group(1)


def parse_bedrooms(bedroom_text):
    m = re.search(r'(\d+\+?)', bedroom_text)
    assert m is not None
    return m.group(1)


def extract_listings(html):
    listings = {}
    import lxml.html
    doc = lxml.html.fromstring(html)
    #data = extract_json(html)
    for li in doc.cssselect('li.listingCard'):
        link = li.cssselect('a.dotted')[0]
        listing_id = re.search(r'(?x) auction-(\d+) \. htm $', link.get('href')).group(1)
        subtitle = li.cssselect('div.property-card-subtitle')[0].text_content()
        price = parse_price(li.cssselect('div.list-view-card-price')[0].text)
        available = parse_avail(li.cssselect('span.list-view-card-available')[0].text)
        bedrooms = parse_bedrooms(li.cssselect('div.property-card-bedrooms')[0].text_content())
        listings[listing_id] = {
            'listing_id':   listing_id,
            'href':         'http://www.trademe.co.nz' + link.get('href'),
            'address':      link.text_content(),
            'suburb':       subtitle.split(',')[0].strip(),
            'city':         subtitle.split(',')[1].strip(),
            'price':        price,
            'available':    available,
            'bedrooms':     bedrooms,
        }
    return listings


if __name__ == '__main__':
    html = open('wgtn-flats.html').read()
    listings = extract_listings(html)
    pprint.pprint(listings)
