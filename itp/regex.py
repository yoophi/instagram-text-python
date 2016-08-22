from __future__ import unicode_literals
import re
import sys

__all__ = [
    'emoji_regex',
    'username_regex',
    'reply_regex',
    'hashtag_regex',
    'url_regex',
]


# A partial regex from Instagram, from the following blog post
# http://instagram-engineering.tumblr.com/post/118304328152/emojineering-part-2-implementing-hashtag-emoji
# Their regex was to match emojis in hashtags, while we just want to match the emojis themselves
EMOJI_EXP = ur'((?:[\xa9\xae\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9\u21aa\u231a\u231b\u2328\u2388\u23cf\u23e9-\u23f3\u23f8-\u23fa\u24c2\u25aa\u25ab\u25b6\u25c0\u25fb-\u25fe\u2600-\u2604\u260e\u2611\u2614\u2615\u2618\u261d\u2620\u2622\u2623\u2626\u262a\u262e\u262f\u2638-\u263a\u2648-\u2653\u2660\u2663\u2665\u2666\u2668\u267b\u267f\u2692-\u2694\u2696\u2697\u2699\u269b\u269c\u26a0\u26a1\u26aa\u26ab\u26b0\u26b1\u26bd\u26be\u26c4\u26c5\u26c8\u26ce\u26cf\u26d1\u26d3\u26d4\u26e9\u26ea\u26f0-\u26f5\u26f7-\u26fa\u26fd\u2702\u2705\u2708-\u270d\u270f\u2712\u2714\u2716\u271d\u2721\u2728\u2733\u2734\u2744\u2747\u274c\u274e\u2753-\u2755\u2757\u2763\u2764\u2795-\u2797\u27a1\u27b0\u27bf\u2934\u2935\u2b05-\u2b07\u2b1b\u2b1c\u2b50\u2b55\u3030\u303d\u3297\u3299]|\ud83c[\udc04\udccf\udd70\udd71\udd7e\udd7f\udd8e\udd91-\udd9a\ude01\ude02\ude1a\ude2f\ude32-\ude3a\ude50\ude51\udf00-\udf21\udf24-\udf93\udf96\udf97\udf99-\udf9b\udf9e-\udff0\udff3-\udff5\udff7-\udfff]|\ud83d[\udc00-\udcfd\udcff-\udd3d\udd49-\udd4e\udd50-\udd67\udd6f\udd70\udd73-\udd79\udd87\udd8a-\udd8d\udd90\udd95\udd96\udda5\udda8\uddb1\uddb2\uddbc\uddc2-\uddc4\uddd1-\uddd3\udddc-\uddde\udde1\udde3\uddef\uddf3\uddfa-\ude4f\ude80-\udec5\udecb-\uded0\udee0-\udee5\udee9\udeeb\udeec\udef0\udef3]|\ud83e[\udd10-\udd18\udd80-\udd84\uddc0]|(?:0\u20e3|1\u20e3|2\u20e3|3\u20e3|4\u20e3|5\u20e3|6\u20e3|7\u20e3|8\u20e3|9\u20e3|#\u20e3|\*\u20e3|\ud83c(?:\udde6\ud83c(?:\uddeb|\uddfd|\uddf1|\uddf8|\udde9|\uddf4|\uddee|\uddf6|\uddec|\uddf7|\uddf2|\uddfc|\udde8|\uddfa|\uddf9|\uddff|\uddea)|\udde7\ud83c(?:\uddf8|\udded|\udde9|\udde7|\uddfe|\uddea|\uddff|\uddef|\uddf2|\uddf9|\uddf4|\udde6|\uddfc|\uddfb|\uddf7|\uddf3|\uddec|\uddeb|\uddee|\uddf6|\uddf1)|\udde8\ud83c(?:\uddf2|\udde6|\uddfb|\uddeb|\uddf1|\uddf3|\uddfd|\uddf5|\udde8|\uddf4|\uddec|\udde9|\uddf0|\uddf7|\uddee|\uddfa|\uddfc|\uddfe|\uddff|\udded)|\udde9\ud83c(?:\uddff|\uddf0|\uddec|\uddef|\uddf2|\uddf4|\uddea)|\uddea\ud83c(?:\udde6|\udde8|\uddec|\uddf7|\uddea|\uddf9|\uddfa|\uddf8|\udded)|\uddeb\ud83c(?:\uddf0|\uddf4|\uddef|\uddee|\uddf7|\uddf2)|\uddec\ud83c(?:\uddf6|\uddeb|\udde6|\uddf2|\uddea|\udded|\uddee|\uddf7|\uddf1|\udde9|\uddf5|\uddfa|\uddf9|\uddec|\uddf3|\uddfc|\uddfe|\uddf8|\udde7)|\udded\ud83c(?:\uddf7|\uddf9|\uddf2|\uddf3|\uddf0|\uddfa)|\uddee\ud83c(?:\uddf4|\udde8|\uddf8|\uddf3|\udde9|\uddf7|\uddf6|\uddea|\uddf2|\uddf1|\uddf9)|\uddef\ud83c(?:\uddf2|\uddf5|\uddea|\uddf4)|\uddf0\ud83c(?:\udded|\uddfe|\uddf2|\uddff|\uddea|\uddee|\uddfc|\uddec|\uddf5|\uddf7|\uddf3)|\uddf1\ud83c(?:\udde6|\uddfb|\udde7|\uddf8|\uddf7|\uddfe|\uddee|\uddf9|\uddfa|\uddf0|\udde8)|\uddf2\ud83c(?:\uddf4|\uddf0|\uddec|\uddfc|\uddfe|\uddfb|\uddf1|\uddf9|\udded|\uddf6|\uddf7|\uddfa|\uddfd|\udde9|\udde8|\uddf3|\uddea|\uddf8|\udde6|\uddff|\uddf2|\uddf5|\uddeb)|\uddf3\ud83c(?:\udde6|\uddf7|\uddf5|\uddf1|\udde8|\uddff|\uddee|\uddea|\uddec|\uddfa|\uddeb|\uddf4)|\uddf4\U0001f1f2|\uddf5\ud83c(?:\uddeb|\uddf0|\uddfc|\uddf8|\udde6|\uddec|\uddfe|\uddea|\udded|\uddf3|\uddf1|\uddf9|\uddf7|\uddf2)|\uddf6\U0001f1e6|\uddf7\ud83c(?:\uddea|\uddf4|\uddfa|\uddfc|\uddf8)|\uddf8\ud83c(?:\uddfb|\uddf2|\uddf9|\udde6|\uddf3|\udde8|\uddf1|\uddec|\uddfd|\uddf0|\uddee|\udde7|\uddf4|\uddf8|\udded|\udde9|\uddf7|\uddef|\uddff|\uddea|\uddfe)|\uddf9\ud83c(?:\udde9|\uddeb|\uddfc|\uddef|\uddff|\udded|\uddf1|\uddec|\uddf0|\uddf4|\uddf9|\udde6|\uddf3|\uddf7|\uddf2|\udde8|\uddfb)|\uddfa\ud83c(?:\uddec|\udde6|\uddf8|\uddfe|\uddf2|\uddff)|\uddfb\ud83c(?:\uddec|\udde8|\uddee|\uddfa|\udde6|\uddea|\uddf3)|\uddfc\ud83c(?:\uddf8|\uddeb)|\uddfd\U0001f1f0|\uddfe\ud83c(?:\uddf9|\uddea)|\uddff\ud83c(?:\udde6|\uddf2|\uddfc))))[\ufe00-\ufe0f\u200d]?)'  # noqa
emoji_regex = re.compile(EMOJI_EXP)

AT_SIGNS = r'[@\uff20]'
UTF_CHARS = r'a-z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'
SPACES = r'[\u0020\u00A0\u1680\u180E\u2002-\u202F\u205F\u2060\u3000]'

# Users
if sys.version_info >= (3, 0):
    username_flags = re.ASCII | re.IGNORECASE
else:
    username_flags = re.IGNORECASE

# The username regex will match invalid usernames that start on dots, end on
# dots and include repeated dots. Those usernames are parsed without regex
# in the actual parser in `Parser._parse_username()`
USERNAME_CHARS = r'([a-z0-9_.]{1,30})(/[a-z][a-z0-9\x80-\xFF-]{0,79})?'

username_regex = re.compile(r'\B' + AT_SIGNS + USERNAME_CHARS, username_flags)
reply_regex = re.compile(r'^(?:' + SPACES + r')*' + AT_SIGNS
                         + r'([a-z0-9_]{1,20}).*', re.IGNORECASE)

reply = r'^(?:' + SPACES + r')*' + AT_SIGNS + r'([a-z0-9_]{1,20}).*'

# Hashtags
HASHTAG_EXP = r'(#|\uff03)([0-9A-Z_]+[%s]*)' % UTF_CHARS
hashtag_regex = re.compile(HASHTAG_EXP, re.IGNORECASE)

# URLs
PRE_CHARS = r'(?:[^/"\':!=]|^|\:)'
DOMAIN_CHARS = r'([\.-]|[^\s_\!\.\/])+\.[a-z]{2,}(?::[0-9]+)?'
PATH_CHARS = r'(?:[\.,]?[%s!\*\'\(\);:=\+\$/%s#\[\]\-_,~@])' % (UTF_CHARS, '%')
QUERY_CHARS = r'[a-z0-9!\*\'\(\);:&=\+\$/%#\[\]\-_\.,~]'

# Valid end-of-path chracters (so /foo. does not gobble the period).
# 1. Allow ) for Wikipedia URLs.
# 2. Allow =&# for empty URL parameters and other URL-join artifacts
PATH_ENDING_CHARS = r'[%s\)=#/]' % UTF_CHARS
QUERY_ENDING_CHARS = '[a-z0-9_&=#]'

url_regex = re.compile('((%s)((https?://|www\\.)(%s)(\/(%s*%s)?)?(\?%s*%s)?))'
                       % (PRE_CHARS, DOMAIN_CHARS, PATH_CHARS,
                          PATH_ENDING_CHARS, QUERY_CHARS, QUERY_ENDING_CHARS),
                       re.IGNORECASE)
