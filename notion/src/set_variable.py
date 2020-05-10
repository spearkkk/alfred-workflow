import sys

from workflow import Workflow3

log = None


def main(wf):
    log.info(wf.args)

    if len(wf.args) == 2:
        log.info("0th: %s" % wf.args[0])
        log.info("1th: %s" % wf.args[1])
        if wf.args[0] == "token":
            wf.save_password(wf.args[0], wf.args[1])
            wf.add_item("Please enter your %s" % wf.args[0],
                        "Your %s is '%s'" % (wf.args[0], wf.args[1]),
                        arg="Your %s is saved." % wf.args[0], valid=True)
            wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow3()
    log = workflow.logger
    sys.exit(workflow.run(main))
