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
    'ChIJPZco_5Jq4okRukKhp4-9oI8': 'Concord, NH 03301\nUSA'
}


def locations():
    ret = {}
    for k in __known_locations:
        ret[k] = {'placeId': k, 'location': {'address': __known_locations[k]}, 'dates': []}
    return ret
