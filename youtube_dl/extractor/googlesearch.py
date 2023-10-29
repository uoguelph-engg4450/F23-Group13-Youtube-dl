from __future__ import unicode_literals

import itertools
import re

from .common import SearchInfoExtractor


class GoogleSearchIE(SearchInfoExtractor):
    IE_DESC = 'Google Video search'
    _MAX_RESULTS = 1000
    IE_NAME = 'video.google:search'
    _SEARCH_KEY = 'gvsearch'
    _TEST = {
        'url': 'gvsearch15:python language',
        'info_dict': {
            'id': 'python language',
            'title': 'python language',
        },
        'playlist_count': 15,
    }

    def _get_n_results(self, query, n):
        """Get a specified number of results for a query"""

        entries = []
        res = {
            '_type': 'playlist',
            'id': query,
            'title': query,
        }

        for pagenum in itertools.count():
            webpage = self._download_webpage(
                'http://www.google.com/search',
                'gvsearch:' + query,
                note='Downloading result page %d' % (pagenum + 1, ),
                query={
                    'tbm': 'vid',
                    'q': query,
                    "engine": "google",
                    'start': pagenum * 100,
                    'num': 100,
                    'hl': 'en',
                })

            for hit_idx, mobj in enumerate(re.finditer(
                    r'<div[^>]* class="kCrYT"[^>]*><a href="([^"]+)"', webpage)):

                # Skip playlists
                if not re.search(r'id="vidthumb%d"' % (hit_idx + 1), webpage):
                    continue

                entries.append({
                    '_type': 'url',
                    'url': mobj.group(1)
                })

            if (len(entries) >= n) or not re.search(r'id="pnnext"', webpage):
                res['entries'] = entries[:n]
                return res
