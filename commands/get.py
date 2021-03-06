from argparse import ArgumentParser

from commands.web import webCommand

from commands.unarchive import unarchive
from helpers.exceptions import InvalidProblemException
from helpers.fileutils import findProblemLocation
from helpers.webutils import fetchProblem


def getCommand(data):
    for problem in data['problem']:
        try:
            get(problem, data)
        except InvalidProblemException:
            print("")
            print(f"Error: Problem '{problem}' does not exist")
            print("")


def get(problemName: str, data: dict):
    message = ""
    folder = findProblemLocation(problemName)
    if folder is None:
        overrideLanguage = data['language']
        fetchProblem(problemName, overrideLanguage)
        message = "👍 Successfully initialized exercise " + problemName + "!"

    elif folder != "":
        unarchive(problemName)
        message = "👍 Successfully unarchived exercise " + problemName + "!"
    if message != "":
        print(message)
    if "open" in data and data['open']:
        webCommand(problemName)

def getParser(parsers: ArgumentParser):
    helpText = 'Get a problem and its tests from the Kattis instance.'
    parser = parsers.add_parser('get', help=helpText, description=helpText)
    parser.add_argument('problem', help='Name of problem to get', nargs='+')
    getFlags(parser)

def getFlags(parser):
    parser.add_argument('-o', '--open', action='store_true', help='Open the problem in your web-browser.')
    parser.add_argument('-l', '--language', type=str, help='Choose the language to initialize the problem in')
