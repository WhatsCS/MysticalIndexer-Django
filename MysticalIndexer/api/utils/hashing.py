# Shamelessly stolen from @shello on github

import random
from itertools import accumulate
from bisect import bisect
from hashlib import blake2b
from datetime import datetime
from django.conf import settings


# Sauce: http://www.unicode.org/charts/PDF/U1F300.pdf
EMOJI_RANGES_UNICODE = {
    6: [
        ('\U0001F300', '\U0001F320'),
        ('\U0001F330', '\U0001F335'),
        ('\U0001F337', '\U0001F37C'),
        ('\U0001F380', '\U0001F393'),
        ('\U0001F3A0', '\U0001F3C4'),
        ('\U0001F3C6', '\U0001F3CA'),
        ('\U0001F3E0', '\U0001F3F0'),
        ('\U0001F400', '\U0001F43E'),
        ('\U0001F440', ),
        ('\U0001F442', '\U0001F4F7'),
        ('\U0001F4F9', '\U0001F4FC'),
        ('\U0001F500', '\U0001F53C'),
        ('\U0001F540', '\U0001F543'),
        ('\U0001F550', '\U0001F567'),
        ('\U0001F5FB', '\U0001F5FF')
    ],
    7: [
        ('\U0001F300', '\U0001F32C'),
        ('\U0001F330', '\U0001F37D'),
        ('\U0001F380', '\U0001F3CE'),
        ('\U0001F3D4', '\U0001F3F7'),
        ('\U0001F400', '\U0001F4FE'),
        ('\U0001F500', '\U0001F54A'),
        ('\U0001F550', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ],
    8: [
        ('\U0001F300', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ]
}

NO_NAME_ERROR = '(No name found for this codepoint)'


def random_emojis(unicode_version=7):
    if unicode_version in EMOJI_RANGES_UNICODE:
        emoji_ranges = EMOJI_RANGES_UNICODE[unicode_version]
    else:
        emoji_ranges = EMOJI_RANGES_UNICODE[-1]

    # Weighted distribution
    count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
    weight_distr = list(accumulate(count))
    emoji = ''
    for x in range(15):
        # Seed each time for maximum randomness
        random.seed()
        # Get one point in the multiple ranges
        point = random.randrange(weight_distr[-1])

        # Select the correct range
        emoji_range_idx = bisect(weight_distr, point)
        emoji_range = emoji_ranges[emoji_range_idx]

        # Calculate the index in the selected range
        point_in_range = point
        if emoji_range_idx is not 0:
            point_in_range = point - weight_distr[emoji_range_idx - 1]

        # Emoji 😄
        emoji += chr(ord(emoji_range[0]) + point_in_range)
        # emoji_name = unicode_name(emoji, NO_NAME_ERROR).capitalize()
        # emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())

    return emoji


def blake2b_hashing(name):
    # set the name with time (ensuring uniqueness
    name = name + datetime.now().strftime('%c.%f')
    # using blake2b hash the file and then set the name back
    hash = blake2b(str.encode(name), digest_size=10, salt=str.encode(settings.SECRET_KEY)[:16]).hexdigest()
    return hash
