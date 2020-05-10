import sys

from workflow import Workflow3, PasswordNotFound

log = None


def main(wf):
    try:
        token = wf.get_password('token')
        log.debug("token: %s" % token)

        wf.delete_password('token')
        wf.add_item("Token Removed", "Token should be updated.", valid=True)
        wf.send_feedback()
    except PasswordNotFound:
        wf.add_item("No Token", "Token is not found.", valid=True)
        wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow3()
    log = workflow.logger
    sys.exit(workflow.run(main))
