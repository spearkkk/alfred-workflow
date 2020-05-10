import sys
import httplib
import json

from workflow import Workflow3, PasswordNotFound

log = None


def get_user_shared_pages(cookie):
    # set header
    headers = {"content-type": "application/json",
               "cookie": cookie}

    # set connection
    connection = httplib.HTTPSConnection("www.notion.so")
    connection.request("POST", "/api/v3/getUserSharedPages", json.dumps({'includeDeleted': False}), headers)
    response = connection.getresponse()

    data = response.read()

    # close connection
    connection.close()
    return data


def get_space_id(space):
    # If you want to get whole data, role value should be changed.
    for key, value in space.iteritems():
        if value['role'] == 'editor':
            return value['value']['id']


def get_parsed_data(user_shared_pages):
    parsed_json = json.loads(user_shared_pages)
    record_map = parsed_json['recordMap']
    space_id = get_space_id(record_map['space'])

    return {'space_id': space_id}


def main(wf):
    wf.clear_cache()
    try:
        token = wf.get_password('token')
        log.debug("token: %s" % token)

    except PasswordNotFound:
        log.warn("There is no `token`.")
        wf.add_item("Cannot find `token`", "Please set `token`...", arg="token", valid=True)
        wf.send_feedback()
        return 0

    # set cookie
    cookie = 'token_v2=%s;' % token

    user_shared_pages = get_user_shared_pages(cookie)
    got = get_parsed_data(user_shared_pages)
    space_id = got['space_id']

    wf.save_password("space_id", space_id)

    wf.add_item("Done")
    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow3()
    log = workflow.logger
    sys.exit(workflow.run(main))
