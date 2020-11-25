#!/usr/bin/python
#
# Copyright 2020 Lon Hohberger
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

import datetime
import json
import sys
from collections import OrderedDict


def box(whatever):
    print('+-' + '-'*len(whatever) + '-+')
    print(f'| {whatever} |')
    print('+-' + '-'*len(whatever) + '-+')


def usa_town_zip(addr):
    lines = addr.split('\n')
    if len(lines) < 2:
        return None
    if lines[len(lines)-1] != 'USA':
        return None
    return lines[len(lines)-2]


def print_locations_by_date(lbd):
    # Don't print the same zip code twice; it's pointless
    for date in lbd:
        been_here = []
        box(date)
        for item in lbd[date]:
            us_location = usa_town_zip(item['address'])
            if us_location and us_location not in been_here:
                been_here.append(us_location)
                print(us_location)
        print()


def lcat(left, right):
    for item in right:
        if item not in left:
            left.append(item)


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
    start = datetime.datetime.fromtimestamp(int(dur['startTimestampMs'])/1000)
    end = datetime.datetime.fromtimestamp(int(dur['endTimestampMs'])/1000)

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


def parse_locations(blob):
    locations = {}
    for loc in blob:
        key = loc['location']['placeId']
        if key not in locations:
            locations[key] = {}
            locations[key]['address'] = loc['location']['address']
            locations[key]['dates'] = duration_to_dates(loc['duration'])
        else:
            lcat(locations[key]['dates'], duration_to_dates(loc['duration']))
    return locations


def load_json(filename):
    ret = None
    with open(filename) as input_file:
        ret = json.load(input_file)
    return ret


# discard the outer shell and activitySegments, because irrelevant
def load_visits(filename):
    jdata = load_json(filename)
    ret = []
    for item in jdata['timelineObjects']:
        key = list(item.keys())[0]
        if key != 'placeVisit':
            continue
        ret.append(item[key])
    return ret


def main(argv):
    if len(argv) < 2:
        print(f"usage: {argv[0]} file1..fileN")
        return 1

    argv.pop(0)
    while True:
        if len(argv) <= 0:
            break
        filename = argv.pop(0)
        locations = load_visits(filename)
        parsed_locs = parse_locations(locations)
        cal = locations_by_date(parsed_locs)
        print_locations_by_date(cal)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
