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


# These should only be added when repeated Google data sets reference
# the location but fail to add an address.
__known_locations = {
    'ChIJzWWtpGPe5okR4ubPXaO0SlQ': '2231 Northampton St.\nHolyoke, MA 01040\nUSA',
    'ChIJvXrDpLShs0wR0PlQXgmfw6w': '40 Old West Side Rd.\nConway, NH 03860\nUSA',
    'ChIJcRfJJW6344kRl1_GjFm3YRg': '127 Shore Dr\nNashua\nNH 03062\nUSA',
    'ChIJXf_56Tu344kR8RWBfWXgCfc': '36 Riverside St\nNashua, NH 03062\nUSA',  # School itself
    'ChIJd0qIXTy344kRAAAAAAAAAAA': '36 Riverside St\nNashua, NH 03062\nUSA',  # Mine Falls Park entrance
    'ChIJr9MG1eu244kRaAi9cB2FR6o': '352 Amherst St\nNashua, NH 03063\nUSA',
    'ChIJE8K9pHtZ34cRigKix9wvo1g': '610 Wesley Dr.\nWood River, IL 62095\nUSA',
    'ChIJ3VMlLwWUEkcRiEOim7E_5ks': 'Purkyňova\n612 00 Brno-Královo Pole\nCzechia',
    'ChIJPZco_5Jq4okRukKhp4-9oI8': 'Concord, NH 03301\nUSA',
    'ChIJ3SCHxeRP4okR4lJZ6I1-8Ho': '58-76 Depot Rd\nAuburn, NH 03032\nUSA',  # FOMBA
    'ChIJLwKZAoG344kRkLOsrnSDmYE': 'Nashua, NH 03062\nUSA',  # Horrigan Pk. Conservation Land
    'ChIJk5eTJuLD44kRAAAAAAAAAAA': '153 Wallace Hill Rd\nTownsend, MA 01469\nUSA',  # Settlement Farm
    'ChIJlXFAOhG444kR3ZJpN9SyQ2E': '105-141 Rideout Rd\nHollis, NH 03049\nUSA'  # Rideout rd trailhead, Hollis, NH
}


def locations():
    ret = {}
    for k in __known_locations:
        ret[k] = {'placeId': k, 'location': {'address': __known_locations[k]}, 'dates': []}
    return ret
