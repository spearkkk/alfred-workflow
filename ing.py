import sys

from workflow import web, Workflow

log = None


def search_keyword(keyword):
    url = 'https://en.dict.naver.com/api3/enko/search'
    params = dict(m="pc",
                  shouldSearchVlive="true",
                  lang="ko",
                  range="word",
                  query=keyword
                  )

    response = web.get(url, params)
    response.raise_for_status()
    return response.json()


def main(wf):
    keyword = wf.args[0]

    # to set next step when 'enter' is clicked
    wf.add_item(title='NAVER Endic.: \'%s\'' % keyword,
                subtitle="search in web page.",
                autocomplete=keyword,
                arg=keyword,
                valid=True)

    def search():
        return search_keyword(keyword)

    results = wf.cached_data('naver_endic_%s' % keyword, search, max_age=3600)
    anothers = results['searchResultMap']['searchResultListMap']['RECOMMENDENTRY']['items']

    for another in anothers:
        if 'entryExpose' in another and 'meanExpose' in another:
            another_keyword = another['entryExpose']
            another_meaning = another['meanExpose']
            wf.add_item(title=u"%s:     %s" % (another_keyword, another_meaning),
                        autocomplete=another_keyword,
                        arg=another_keyword,
                        valid=True)

    if 'searchResultMap' in results and 'searchResultListMap' in results['searchResultMap']:
        if 'WORD' in results['searchResultMap']['searchResultListMap']:
            parent = results['searchResultMap']['searchResultListMap']['WORD']
            searched_keyword = parent.get('query', keyword)

            if 'items' in parent and len(parent['items']) > 0 and 'meansCollector' in parent['items'][0] and len(
                    parent['items'][0]['meansCollector']) > 0 and 'means' in parent['items'][0]['meansCollector'][0]:
                words = parent['items'][0]['meansCollector'][0]['means']
                for word in words:
                    meaning = word['value']
                    wf.add_item(title=u"%s:     %s" % (searched_keyword, meaning),
                                autocomplete=searched_keyword,
                                arg=searched_keyword,
                                valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow()
    log = workflow.logger
    sys.exit(workflow.run(main))
