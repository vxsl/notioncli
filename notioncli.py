import os

from termcolor import cprint

from notion.client import NotionClient
from notion.block import TodoBlock

from contextlib import contextmanager


@contextmanager
def captureStdOut(output):
    stdout = sys.stdout
    sys.stdout = output
    try:
        yield
    finally:
        sys.stdout = stdout


try:
    client = NotionClient(token_v2=os.environ["NOTION_TOKEN"], monitor=False)
except:
    cprint(
        "NOTION_TOKEN / NOTION_PAGE environment variables not set or token expired.\n",
        "red",
    )
try:
    page = client.get_block(os.environ["NOTION_PAGE"])
except:
    cprint("NOTION_PAGE environment variables not set.\n", "red")


def parse_task(string):
    taskn = string
    if isinstance(string, int):
        taskn = str(taskn)
    else:
        if "," in string:
            taskn = string.split(",")
    value = taskn
    return value


def checkEnv():
    try:
        os.environ["NOTION_TOKEN"]
        os.environ["NOTION_PAGE"]
    except KeyError:
        cprint("Environment variables not set", "white")
        exit


def list():
    checkEnv()
    n = 0
    cprint("\n\n{}\n".format(page.title), "white", attrs=["bold"])
    cprint("  # Status Description", "white", attrs=["underline"])
    for child in page.children:
        if child.type == "sub_header":
            cprint("[{}]".format(child.title), "green")
        elif child.type == "to_do":
            n += 1
            if child.checked:
                check = "[*]"
            else:
                check = "[ ]"
            cprint("  {}  {}  {}.".format(n, check, child.title), "green")
        else:
            pass

    cprint("\n{} total tasks".format(n), "white", attrs=["bold"])


def check(taskn):
    n = 0
    for child in page.children:
        if child.type == "to_do":
            n += 1
            for task in taskn:
                if n == int(task):
                    child.checked = True
        else:
            pass  # not a task
    cprint("{} marked as completed".format(taskn), "white", attrs=["bold"])


def uncheck(taskn):
    if isinstance(taskn, int):
        taskn = str(taskn)
    else:
        if "," in taskn:
            taskn = taskn.split(",")
    n = 0
    for child in page.children:
        n += 1
        try:
            for task in taskn:
                if n == int(task):
                    child.checked = False
        except:
            pass  # not a task
    cprint("{} marked as incomplete".format(taskn), "white", attrs=["bold"])


def add(task):
    newchild = page.children.add_new(TodoBlock, title=task)
    newchild.checked = False
    cprint("{} added as a new task".format(task))


def remove(taskn):
    if isinstance(taskn, int):
        taskn = str(taskn)
    else:
        if "," in taskn:
            taskn = taskn.split(",")
    n = 0
    for child in page.children:
        if child.type == "to_do":
            n += 1
            for task in taskn:
                if n == int(task):
                    child.remove()
        else:
            pass  # not a task
    cprint("{} removed.".format(taskn), "white", attrs=["bold"])
