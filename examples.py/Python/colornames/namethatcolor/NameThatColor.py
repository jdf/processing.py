#!/usr/bin/env python
"""
name_that_color.py -- find names for hex colors
Copyright (c) 2010, Jeremiah Dodds <jeremiah.dodds@gmail.com>

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the conditions in LICENSE.txt are met
"""
from collections import namedtuple

ColorInfo = namedtuple('ColorInfo',
                       ' '.join(['hex_value', 'name', 'red', 'green', 'blue',
                                 'hue', 'saturation', 'lightness']))
Match = namedtuple('Match', ' '.join(['hex_value', 'name', 'exact',
                                      'original']))
RGB = namedtuple('RGB', ' '.join(['red', 'green', 'blue']))
HSL = namedtuple('HSL', ' '.join(['hue', 'saturation', 'lightness']))


class NameThatColor(object):
    """Utility for finding the closest "human readable" name for a hex color
    """
    def __init__(self, color_file):
        import csv
        self.color_info = []

        reader = csv.reader(open(color_file))

        for hex_val, name in reader:
            red, green, blue = self.rgb(hex_val.strip())
            hue, saturation, lightness = self.hsl(hex_val.strip())
            self.color_info.append(ColorInfo(hex_val.strip(), name.strip(),
                                             red, green, blue,
                                             hue, saturation, lightness))

    def name(self, color):
        """Return the closest human readable name given a color
        """
        color = color.upper()

        if not 3 < len(color) < 8:
            return Match("#000000", "Invalid Color", False, color)
        elif len(color) % 3 == 0:
            color = "#" + color
        elif len(color) == 4:
            color = ''.join(['#',
                             color[1], color[1],
                             color[2], color[2],
                             color[3], color[3]])

        red, green, blue = self.rgb(color)
        hue, saturation, lightness = self.hsl(color)

        ndf1 = 0
        ndf2 = 0
        ndf = 0
        the_color = Match(None, None, None, None)
        df = -1

        for info in self.color_info:
            if color == info.hex_value:
                return Match(info.hex_value, info.name, True, color)

            ndf1 = (((red - info.red) ** 2) +
                    ((green - info.green) ** 2) +
                    ((blue - info.blue) ** 2))
            ndf2 = (((hue - info.hue) ** 2) +
                    ((saturation - info.saturation) ** 2) +
                    ((lightness - info.lightness) ** 2))
            ndf = ndf1 + ndf2 * 2

            if not 0 < df < ndf:
                df = ndf
                the_color = info

        if not the_color.name:
            return Match("#000000", "Invalid Color", False, color)
        else:
            return Match(the_color.hex_value,
                         the_color.name,
                         False,
                         color)

    def rgb(self, color):
        """Given a hex string representing a color, return an object with
        values representing red, green, and blue.
        """
        return RGB(int(color[1:3], 16),
                   int(color[3:5], 16),
                   int(color[5:7], 16))

    def hsl(self, color):
        """Given a hex string representing a color, return an object with
        attributes representing hue, lightness, and saturation.
        """

        red, green, blue = self.rgb(color)

        red /= 255.0
        green /= 255.0
        blue /= 255.0

        min_color = min(red, min(green, blue))
        max_color = max(red, max(green, blue))
        delta = max_color - min_color
        lightness = (min_color + max_color) / 2

        saturation = 0
        sat_mod = ((2 * lightness) if lightness < 0.5 else (2 - 2 * lightness))

        if 0 < lightness < 1:
            saturation = (delta / sat_mod)

        hue = 0

        if delta > 0:
            if max_color == red and max_color != green:
                hue += (green - blue) / delta
            if max_color == green and max_color != blue:
                hue += (2 + (blue - red) / delta)
            if max_color == blue and max_color != red:
                hue += (4 + (red - green) / delta)
            hue /= 6

        return HSL(int(hue * 255),
                   int(saturation * 255),
                   int(lightness * 255))

def main():
    """Entry point for NameThatColor.py.
    Parse options, and find that color.
    """

    import json
    import argparse

    output_choices = {
        'match_hex': lambda m: m.hex_value,
        'match_name': lambda m: m.name,
        'is_exact': lambda m: m.exact,
        'original_hex': lambda m: m.original
    }

    format_choices = {
        'json': lambda r: json.dumps(r),
        'raw' : lambda r: r
    }

    color_set_choices = {
        'resene': 'resene.csv',
        'html4': 'html4.csv',
        'css3': 'css3.csv'
    }
    
    parser = argparse.ArgumentParser(
        description="Find the closest known color name for a hex value")

    color_set_sources = parser.add_mutually_exclusive_group(required=True)

    color_set_sources.add_argument('-s', '--color-set', dest="color_set",
                                  choices=color_set_choices.keys(),
                                  help="the set of color names to match to.")

    color_set_sources.add_argument('-c', '--colors', dest='colors_file',
                                   help="a csv file colors and their hex value")

    parser.add_argument('-o', '--output',
                        dest="output",
                        nargs='*',
                        choices=output_choices.keys(),
                        default=['match_hex', 'match_name'],
                        help="what information about the color match to output")

    parser.add_argument('--format',
                        dest="format",
                        choices=format_choices.keys(),
                        default="json",
                        help="what format to return data in")

    parser.add_argument('target',
                        help="hex value of the color to search for")

    args = parser.parse_args()

    colors_file = args.colors_file

    if not colors_file:
        from pkg_resources import Requirement, resource_filename
        colors_file = resource_filename(
            Requirement.parse('namethatcolor'),
            'namethatcolor/data/%s' % color_set_choices[args.color_set]
        )
        
    Namer = NameThatColor(colors_file)
    match = Namer.name(args.target)
    result = {}
    for choice in args.output:
        result[choice] = output_choices[choice](match)
    print format_choices[args.format](result)

if __name__ == '__main__':
    main()
