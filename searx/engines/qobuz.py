# SPDX-License-Identifier: AGPL-3.0-or-later
"""
 Qobuz (Music)
"""

from lxml import html
from searx.engines.xpath import extract_text
from searx.utils import eval_xpath_getindex
from urllib.parse import quote

# about
about = {
    "website": 'https://www.qobuz.com',
    "wikidata_id": 'Q3412507',
    "use_official_api": False,
    "results": 'HTML',
}

categories = ['music']
paging = True

# Set base_url in settings.yml in order to
# have the desired local TLD.
base_url ='https://www.qobuz.com'
search_url = base_url + '/us-en/search?q={query}&page={pageno}'

results_xpath = '//div[@class="search-results"]/div'


def request(query, params):
    params['url'] = search_url.format(query=quote(query), pageno=params['pageno'])
    return params


def response(resp):
    results = []

    dom = html.fromstring(resp.text)
    results_dom = dom.xpath(results_xpath)
    if not results_dom:
        return []

    for result_dom in results_dom:
        url = base_url + eval_xpath_getindex(result_dom, './/a', 0).attrib['href']
        artist = extract_text(result_dom.xpath('.//h3'))
        album = extract_text(result_dom.xpath('.//h4'))
        title = f"{artist}: {album}"

        content = extract_text(eval_xpath_getindex(result_dom, './/p[contains(@class, "data")]', 0))
        image = eval_xpath_getindex(result_dom, './/img', 0).attrib['src']
        results.append(
            {
                'url': url,
                'title': title,
                'content': content,
                'img_src': image,
            }
        )

    return results
