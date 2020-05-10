import re
import sys
import httplib
import json
import datetime

from workflow import Workflow3, MATCH_ATOM, MATCH_CAPITALS, MATCH_STARTSWITH, MATCH_SUBSTRING, PasswordNotFound

log = None


def get_key(item):
    return u'%s %s' % (item['title'], item['tags'])


def get_searched_item(loaded, result):
    if ('parent_id' and 'alive' and 'type' and 'id') in loaded and loaded['alive']:
        if loaded['type'] in ['bulleted_list', 'toggle', 'numbered_list', 'quote', 'code']:
            return None
        title = ''
        tags = ''
        if 'properties' in loaded and 'title' in loaded['properties']:
            properties = loaded['properties']
            title = ''.join([i if type(i) is unicode else '' for sublist in properties['title'] for i in sublist])
            for property_key, property_value in properties.iteritems():
                if property_key == 'title':
                    continue
                tags = ''.join([i if type(i) is unicode else '' for sublist in property_value for i in sublist])
        elif 'highlight' in result:
            title = result['highlight']['text'].replace("<gzkNfoUU>", "").replace("</gzkNfoUU>", "")

        if 'format' in loaded:
            value_format = loaded['format']
            if 'page_icon' in value_format:
                title = u"%s %s" % (value_format['page_icon'], title)

        item_id = loaded['id'].replace("-", "")
        if loaded['type'] not in ['page']:
            item_id = loaded['parent_id'].replace("-", "")

        created_time = ''
        if 'created_time' in loaded:
            created_time = datetime.datetime.fromtimestamp(float(str(loaded['created_time'])[0:-3]))

        return {'item_id': item_id, 'title': title, 'tags': tags, 'created_time': created_time}


def search_keyword(keyword, cookie, space_id):
    # set header
    headers = {"Content-type": "application/json",
               "Cookie": cookie}

    # set connection
    connection = httplib.HTTPSConnection("www.notion.so")
    connection.request("POST", "/api/v3/search",
                       get_query(keyword, space_id), headers)
    response = connection.getresponse()

    data = response.read()

    # close connection
    connection.close()

    parsed_json = json.loads(data)

    searched_items = []
    for result in parsed_json['results']:
        result_id = result['id']
        searched_item = get_searched_item(parsed_json['recordMap']['block'][result_id]['value'], result)
        if searched_item is None:
            continue
        searched_items.append(searched_item)
    return searched_items


def get_query(keyword, space_id):
    filters = {"isDeletedOnly": False, "excludeTemplates": False, "isNavigableOnly": False,
               "requireEditPermissions": False, "ancestors": [], "createdBy": [], "editedBy": [], "lastEditedTime": {},
               "createdTime": {}}

    query = {"type": "BlocksInSpace", "query": keyword, "spaceId": space_id, "limit": 100, "sort": "Relevance",
             "source": "quick_find", "filters": filters}

    return json.dumps(query)


def main(wf):
    # set link prefix
    prefix_link = 'notion://www.notion.so/'

    try:
        token = wf.get_password('token')
    except PasswordNotFound:
        log.warn("There is no `token`.")
        wf.add_item("Cannot find `token`", "Please initialize first...")
        wf.send_feedback()
        return 0

    # set cookie
    cookie = 'token_v2=%s;' % token
    space_id = workflow.get_password("space_id")

    searched_items = []

    keyword = None

    def search():
        return search_keyword(keyword, cookie, space_id)

    # keyword to search in Notion
    if len(wf.args):
        keyword = wf.args[0]
        cache_key = re.sub(r"\s+", "", keyword)
        searched_items = wf.cached_data('notion_search_%s' % cache_key, search, max_age=300)

    seen_id = set()
    deduplicated = []
    for elem in searched_items:
        if elem['item_id'] not in seen_id:
            seen_id.add(elem['item_id'])
            deduplicated.append(elem)

    items = wf.filter(keyword, deduplicated, get_key,
                      match_on=MATCH_STARTSWITH | MATCH_CAPITALS | MATCH_ATOM | MATCH_SUBSTRING)

    for elem in items:
        added_item = wf.add_item(title=elem['title'],
                                 arg=u"%s%s" % (prefix_link, elem['item_id']),
                                 valid=True,
                                 uid=elem['item_id'],
                                 copytext=elem['title'])
        added_item.add_modifier(key='cmd',
                                subtitle=elem['tags'],
                                valid=False)
        added_item.add_modifier(key='ctrl',
                                subtitle="created time: %s" % elem['created_time'],
                                valid=False)
        added_item.add_modifier(key='alt',
                                subtitle="redirect: www.notion.so/%s" % elem['title'],
                                arg=u"https://www.notion.so/%s" % elem['item_id'],
                                valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow3()
    log = workflow.logger
    sys.exit(workflow.run(main))
