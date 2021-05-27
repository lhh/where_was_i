Usage: where-was-i [-h] [args] [file1..fileN]

Parse Google's semantic location data (in JSON format) into human readable form.  This reads in all the JSON files specified, aggregates location information, and prints out each date and locations visited on that date, optionally entries by regular expression.

Older versions parsed the files individually.  Google semantic data, however, tend to be gathered for year at a time, and Google sends it to users in one-file-per-month format.  Given that people tend to visit locations more than once per year, I found that the location data would sometimes be incomplete for a given month for a given year, but other months have the missing information for a given location.

Even so, there are some times when Google location data do not have any address whatsoever for a location, so we can add those to known_locations.py to make the output readable.

There is a preliminary container build setup using Makefiles if one does not desire to use 'pip' to install things; it utilizes Red Hat's Universal Base Image, but could work with minimal changes on other base container images. Note that the container build only works with one file at a time.

Examples:
 - where-was-i 2020/\*

        ...
        +------------+
        | 2020-11-08 |
        +------------+
        Nashua, NH 03062
        Northfield, NH 03276
        Merrimack, NH 03054
        ...

 - where-was-i -s 2020/\*

        ...
        2020-11-08 Nashua, NH 03062
        2020-11-08 Northfield, NH 03276
        2020-11-08 Merrimack, NH 03054
        ...

 - where-was-i --address -p 'Northfield' 2020/\*

        ...
        +------------+
        | 2020-11-08 |
        +------------+
        75 Ski Hill Dr, Northfield, NH 03276, USA
        ...

 - where-was-i -s -p 'Northfield' 2020/\*

        ...
        2020-11-06 Northfield, NH 03276
        2020-11-08 Northfield, NH 03276

 - where-was-i -s -c -p 'Northfield' 2020/\*

        ...
        2020-11-06 Northfield, NH 03276
        2020-11-08 Northfield, NH 03276
        6 records

 - where-was-i --csv -a -p 'Northfield' 2020.\*

        Date,Location
        ...
        2020-11-06,"75 Ski Hill Dr, Northfield, NH 03276, USA"
        2020-11-08,"75 Ski Hill Dr, Northfield, NH 03276, USA"

Notes:
 - there may be issues with non-US addresses.
 - Although Google location data is organized by year, location visits sometimes cross over from one to the next. For example, one might see the Dec. 31 of the prior year or Jan. 1 of the next year at the beginning or end of the output. This is expected.
