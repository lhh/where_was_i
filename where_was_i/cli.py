#!/usr/bin/env python
#
# Copyright 2020, 2021 Lon Hohberger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import datetime
import json
import re
import sys
from collections import OrderedDict

from where_was_i import known_locations


def box(whatever):
    print('+-' + '-' * len(whatever) + '-+')
    print(f'| {whatever} |')
    print('+-' + '-' * len(whatever) + '-+')


def normalize_usa_addr(addr):
    naddr = addr.replace(', ', '\n')
    lines = naddr.split('\n')

    if len(lines) < 2:
        return addr

    country = lines.pop()
    if country not in ('USA', 'United States of America', 'United States'):
        return addr

    zipcode = lines.pop()
    # 5 or 5+4
    if not re.search(r'[0-9][0-9][0-9][0-9][0-9](\-[0-9][0-9][0-9][0-9])?$', zipcode):
        return addr

    # handle unincorporated areas: "Merrimack County, NH 11111, USA"
    county = None
    city = None
    while len(lines) > 0:
        city = lines.pop()
        if 'County' in city:
            county = city
            city = None
            continue
        break

    if county and city:
        city = f'{city}, {county}'
    elif not city:
        city = county

    if len(lines):
        header = '\n'.join(lines)
        return f'{header}\n{city}, {zipcode}\nUSA'
    return f'{city}, {zipcode}\nUSA'


def usa_town_zip(addr):
    lines = addr.split('\n')
    if len(lines) < 2:
        return None
    if lines[len(lines) - 1] != 'USA':
        return None
    return lines[len(lines) - 2]


def print_locations_by_date(lbd, location_pattern=None, full_address=False, simple=False, count=False, csv=False):
    total = 0
    # Don't print the same zip code twice for the same day; it's pointless

    if csv and not simple:
        print('Date,Location')

    for date in lbd:
        been_here = []
        date_shown = False
        for item in lbd[date]:
            us_location = printable_location(item, full_address)
            if location_pattern and not re.search(location_pattern, us_location):
                continue
            if not date_shown:
                if not simple and not csv:
                    box(date)
                    date_shown = True
            if us_location and us_location not in been_here:
                been_here.append(us_location)
                if simple and not csv:
                    print(date, us_location)
                elif csv:
                    print(f'{date},\"{us_location}\"')
                else:
                    print(us_location)
                total = total + 1
        if date_shown:
            print()

    if count:
        if not csv:
            print(total, 'records')
        else:
            print(f'{total},records')


def lcat(left, right):
    ret = False
    for item in right:
        if item not in left:
            left.append(item)
            ret = True
    return ret


# Return an inversed list of all locations by date
def locations_by_date(locations):
    ret = OrderedDict()
    all_dates = []

    # pass 1: determine all our dates
    for key in locations:
        lcat(all_dates, locations[key]['dates'])

    all_dates.sort()

    # pass 2: Determine locations by date
    for date in all_dates:
        if date not in ret:
            ret[date] = []
        for key in locations:
            if date in locations[key]['dates']:
                ret[date].append(locations[key])
    return ret


def duration_to_dates(dur):
    start = datetime.datetime.fromtimestamp(int(dur['startTimestampMs']) / 1000)
    end = datetime.datetime.fromtimestamp(int(dur['endTimestampMs']) / 1000)

    ret = []
    delta = end - start
    for day in range(delta.days + 1):
        d_date = start + datetime.timedelta(days=day)
        pdate = d_date.strftime('%Y-%m-%d')
        if pdate not in ret:
            ret.append(pdate)
    # Just in case it's a short time between next-to-last prior day
    # but still crosses a date line
    pdate = end.strftime('%Y-%m-%d')
    if pdate not in ret:
        ret.append(pdate)

    return ret


def printable_location(location, full_address=False):
    loc = location['location']
    # If there's no street address or zip code (ex: in BLM land,
    # National Parks, private areas, etc.), just give the lat/lon
    # coordinates. (USA only)

    while 'address' in loc:
        naddr = normalize_usa_addr(loc['address'])
        lines = naddr.split('\n')
        if len(lines) < 2:
            break
        if lines[len(lines) - 1] not in ('USA', 'United States', 'United States of America'):
            return loc['address'].replace('\n', ', ')
        if not full_address:
            return lines[len(lines) - 2].replace('\n', ', ')
        return ', '.join(lines).replace('\n', ', ')
        # NOTREACHED

    try:
        lat = float(loc['latitudeE7']) / 10000000
        lon = float(loc['longitudeE7']) / 10000000
    except KeyError:
        info = location['placeId']
        return f'No location information for: {info}'

    place = location['placeId']
    if 'name' in loc:
        name = loc['name']
        return f'Zip code/Address missing: {name} @ {lat},{lon} - {place}'
    return f'Zip code/Address missing: {lat},{lon} - {place}'


# Sometimes, entries do not have location data (coordinates or address),
# but they still have the unique place ID.  Merge a location into our set
# of locations, adding missing entries for address/latitude/longitude/name
# as needed.
#
# locations = {'placeId': 'address', 'latitudeE7', 'longitudeE7', 'name' }
def update_locations(locations, location):
    loc = location['location']
    pid = loc['placeId']

    if pid not in locations:
        locations[pid] = {'placeId': pid, 'location': {}, 'dates': []}

    ret = False
    for k in ('address', 'name', 'latitudeE7', 'longitudeE7'):
        if k not in locations[pid]['location'] and k in loc:
            locations[pid]['location'][k] = loc[k]
            ret = True

    if lcat(locations[pid]['dates'], duration_to_dates(location['duration'])):
        ret = True
    return ret


def parse_locations(blob):
    locations = {}
    for loc in blob:
        update_locations(locations, loc)
    return locations


def load_json(filename):
    ret = None
    with open(filename) as input_file:
        ret = json.load(input_file)
    return ret


def decode_json(buffer):
    return json.loads(buffer)


# discard the outer shell and activitySegments, because irrelevant
def load_visits(jdata):
    ret = []
    for item in jdata['timelineObjects']:
        key = list(item.keys())[0]
        if key != 'placeVisit':
            continue
        ret.append(item[key])
    return ret


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pattern', '-p', help='Display locations visited matching this regular expression')
    parser.add_argument('--address', '-a', action='store_true', default=False, help='Include address instead of just city/state/zip')
    parser.add_argument('--simple', '-s', action='store_true', default=False, help='Show output in simple format (date - location)')
    parser.add_argument('--count', '-c', action='store_true', default=False, help='Show final summary/count')
    parser.add_argument('--csv', action='store_true', default=False, help='Output in CSV format')
    parser.add_argument('file', help='File(s) to analyze', nargs='*')
    return parser.parse_args()


def main():
    args = parse_options()
    all_locations = known_locations.locations()
    if args.file:
        for filename in args.file:
            jdata = load_json(filename)
            locations = load_visits(jdata)
            for k in locations:
                update_locations(all_locations, k)
    else:
        data = sys.stdin.read()
        jdata = decode_json(data)
        locations = load_visits(jdata)
        for k in locations:
            update_locations(all_locations, k)

    cal = locations_by_date(all_locations)
    print_locations_by_date(cal, args.pattern, args.address, args.simple, args.count, args.csv)

    return 0


if __name__ == "__main__":
    sys.exit(main())
