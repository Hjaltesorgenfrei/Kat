from argparse import ArgumentParser
from helpers.config import getConfig, commandConvert

def configCommand(data):
    if 'section' not in data:
        print("Adding/updating configuration to your .kattisrc...")
        if not getConfig():
            print("""\
Something went wrong in locating the configuration file
for kattis. Have you fetched the .kattisrc? Consult the 
README.md for more details.""")
        else:
            print("Successfully added default configuration to your .kattisrc!")

    elif "value" in data:
        cfg, location = getConfig(shouldReturnLocation=True)
        section = data["section"]
        option = data["option"]
        value = data["value"]
        if not cfg:
            print("""\
Something went wrong in locating the configuration file
for kattis. Have you fetched the .kattisrc? Consult the 
README.md for more details.""")
        elif cfg.has_section(section):
            if not cfg.has_option(section, option) and section.lower() in ["kat", "kattis", "user"]:
                print("Setting", option, "was not recognized for section [" + section + "]")
            else:
                cfg.set(section, option, value)
                with open(location, "w") as configFile:
                    cfg.write(configFile)
                print("The setting", option, "from section [" + section + "]", "was set to", value)
        else:
            print("Section [" + section + "]", "was not found.")

    else:
        print("""\
Invalid number of arguments, expected 
'config <section> <option> <value>'. 
Remember to put arguments with spaces in quotes.""")

def configParser(parsers: ArgumentParser):
    helpText = 'Modify a configuration line.'
    parser = parsers.add_parser('config', description=helpText, help=helpText)
    parser.add_argument('section', help='The section of the config to access')
    parser.add_argument('option', help='The option to change')
    parser.add_argument('value', help='The updated value')
