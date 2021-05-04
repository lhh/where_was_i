Usage: python3 where_was_i.py [file1..fileN]

Parse semantic Google's semantic location data (in JSON format) into human readable form.  This reads in all the JSON files specified, aggregates location information, and prints out each date and locations visited on that date.

Older versions parsed the files individually.  Google semantic data, however, tend to be gathered for year at a time, and Google sends it to users in one-file-per-month format.  Given that people tend to visit locations more than once per year, I found that the location data would sometimes be incomplete for a given month for a given year, but other months have the missing information for a given location.

Even so, there are some times when Google location data do not have any address whatsoever for a location, so we can add those to known_locations.py to make the output readable.

Notes:
 - there are issues with non-US addresses.
 - Although Google location data is organized by year, location visits sometimes cross over from one to the next. This is expected.
