#!/usr/bin/python3

import json
import pprint
import re
import sys
import time


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


def parse_avail(avail_text):
    m = re.search(r'Available (.+?)[\s]*$', avail_text)
    if not m:
        raise ParseError('parse_avail cannot parse {!r}'.format(avail_text))
    return parse_date(m.group(1))


def parse_listing_date(elem):
    text = elem.cssselect('.list-view-listed-date')[0].text_content()
    m = re.search(r'Listed (.+)$', text)
    return parse_date(m.group(1))


def parse_date(d_text):
    # Convert d_text to 'struct tm'
    if d_text == 'Now':
        d = time.localtime()
    elif d_text == 'Yesterday':
        d = time.localtime(time.time() - 86400)
    else:
        d = time.strptime(d_text.replace(',', ''), '%a %d %b')
    # Parsing strategy:  use current year, if parsed date is 'really old'
    # (more than 180 days ago) then increment year by 1 (the date's in the future).
    year = time.localtime().tm_year
    old = time.localtime(time.time() - 86400*180)
    if (d.tm_mon, d.tm_mday) < (old.tm_mon, old.tm_mday):
        year += 1
    return '{:04d}/{:02d}/{:02d}'.format(year, d.tm_mon, d.tm_mday)


def parse_bedrooms(bedroom_text):
    m = re.search(r'(\d+\+?)', bedroom_text)
    bedrooms = m.group(1)
    return bedrooms if '+' in bedrooms else int(bedrooms)


def parse_bathrooms(elem):
    text = elem.cssselect('div.property-card-bathrooms')[0].text_content()
    m = re.search(r'(\d+)', text)
    return int(m.group(1))


def parse_listing_id(elem):
    link = elem.cssselect('a.dotted')[0]
    listing_id = re.search(r'(?x) auction-(\d+) \. htm $', link.get('href')).group(1)
    return listing_id


class ParseError(Exception): pass


# returns (flat?, house, street)
# and this is a hideous hack but it works on 90% of the listings!
def parse_address(elem):
    address_text = elem.cssselect('a.dotted')[0].text_content().upper()
    m = re.search('''(?x)
        ^
        (?:(?:UNIT|APT|APARTMENT)\s)?                     # strip off some common prefixes
        (?:([0-9A-Z]+)/)?                                   # optional flat number
        (\d+(?:-\d+)?[A-Z]*)                                  # house number(s)
        \s+
        ([^.,]+)                                            # street name
    ''', address_text)
    if not m:
        raise ParseError('Cannot parse address: {!r}'.format(address_text))
    flat = m.group(1)
    house = m.group(2)
    street = m.group(3)
    return flat, house, street


def extract_listings(html):
    listings = {}
    import lxml.html
    doc = lxml.html.fromstring(html)
    #data = extract_json(html)
    for li in doc.cssselect('li.listingCard'):
        try:
            link = li.cssselect('a.dotted')[0]
            subtitle = li.cssselect('div.property-card-subtitle')[0].text_content()
            price = parse_price(li.cssselect('div.list-view-card-price')[0].text)
            available = parse_avail(li.cssselect('span.list-view-card-available')[0].text)
            thumbnail = li.cssselect('img.list-view-photo')[0].get('src')
            if 'placeholder' in thumbnail:
                thumbnail = None
            listing_id = parse_listing_id(li)
            unit, house, street = parse_address(li)
            listings[listing_id] = {
                'listing_id':   listing_id,
                'listed':       parse_listing_date(li),
                'unit':         unit,
                'house':        house,
                'street':       street,
                'suburb':       subtitle.split(',')[0].strip(),
                'city':         subtitle.split(',')[1].strip(),
                'price':        price,
                'available':    available,
                'bedrooms':     parse_bedrooms(li.cssselect('div.property-card-bedrooms')[0].text_content()),
                'bathrooms':    parse_bathrooms(li),
                'href':         'http://www.trademe.co.nz' + link.get('href'),
                'photo':        thumbnail,
            }
        except ParseError as err:
            print('warning, parse error: {}'.format(err), file=sys.stderr)
            continue
    return listings


def to_csv(value):
    if value is None:
        return ''
    vstr = str(value)
    if ',' in vstr:
        assert '"' not in vstr
        vstr = '"{}"'.format(value)
    return vstr


def dump_csv(records, f):
    keys = ['listing_id', 'listed', 'available',
            'unit', 'house', 'street', 'suburb', 'city',
            'price', 'bedrooms', 'bathrooms',
            'href', 'photo']
    f.write(','.join(keys) + '\n')
    for item in records.values():
        values = [to_csv(item.get(k)) for k in keys]
        if any(',' in v for v in values):
            print(values)
            assert False
        f.write(','.join(values) + '\n')


if __name__ == '__main__':
    import sys
    html = open(sys.argv[1]).read()
    listings = extract_listings(html)
    with open('output.csv', 'w') as f:
        dump_csv(listings, sys.stdout)
