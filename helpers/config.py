import configparser, os, sys
from pathlib import Path

_DEFAULT_CONFIG = "/etc/kattis/submit/kattisrc"

def configLocations():
    return [
        _DEFAULT_CONFIG,
        os.path.join(str(Path.home()), ".kattisrc"),
        os.path.join(os.path.dirname(sys.argv[0]), ".kattisrc"),
        os.path.join(os.getcwd(), ".kattisrc")
    ]

def findConfig(config = None):
    locations = configLocations()

    found = []
    for location in locations:
        if os.path.exists(location):
            if config:
                config.read(location)
            found.append(location)
    return found

_CONFIG_NOT_FOUND_MSG = """\
I failed to read in a config file from your home directory or from the
same directory as this script. Please go to your Kattis installation
to download a .kattisrc file.

The file should look something like this:
[user]
username: yourusername
token: *********

[kattis]
loginurl: https://<kattis>/login
submissionurl: https://<kattis>/submit"""

class Config:
    """The config singleton, use getConfig to access."""
    __instance = None
    __location = None
    @staticmethod
    def getInstance(shouldReturnLocation = False):
        if Config.__instance == None:
            Config()
        if shouldReturnLocation:
            return Config.__instance, Config.__location
        return Config.__instance
    @staticmethod
    def save():
        if Config.__instance == None:
            Config()
        with open(Config.__location, "w") as configFile:
            Config.__instance.write(configFile)
    def __init__(self):
        if Config.__instance != None:
            raise Exception("Config was tried initialized outside static scope.")
        else:
            _config = configparser.ConfigParser(converters={"array": strToArr, "command": toCommandArray})

            found = findConfig(_config)

            if not found:
                print("Config locations searched:", configLocations(), "\n")
                print(_CONFIG_NOT_FOUND_MSG)
                sys.exit()

            self = preconfigure(_config, found[-1])
            Config.__instance = self
            Config.__location = found[-1]

def getConfig(shouldReturnLocation = False):
    return Config.getInstance(shouldReturnLocation)

def saveConfig():
    Config.save()

def getConfigUrl(option, default):
    cfg = getConfig()
    if cfg.has_option("kattis", option):
        return cfg.get("kattis", option)
    else:
        return formatUrl(cfg.get("kattis", "hostname"), default)

def formatUrl(hostname, path):
    return "https://%s/%s" % (hostname, path)

def preconfigure(cfg, location):
    defaults = {
        "kat": {
            "language": "python",
            "openFileCommand": "",
            "workCommand": "",
        },
        "File associations": {
            ".c": "C",
            ".c#": "C#",
            ".c++": "C++",
            ".cc": "C++",
            ".cpp": "C++",
            ".cs": "C#",
            ".cxx": "C++",
            ".go": "Go",
            ".h": "C++",
            ".hs": "Haskell",
            ".java": "Java",
            ".js": "JavaScript",
            ".m": "Objective-C",
            ".pas": "Pascal",
            ".php": "PHP",
            ".pl": "Prolog",
            ".py": "Python",
            ".rb": "Ruby",
            ".fs": "F#",
            ".fsx": "F#",
            ".fsscript": "F#",
        },
        "Initialize commands": {
            "F#": "dotnet new console -lang F#",
            "C#": "dotnet new console",
        },
        "Run commands": {
            "Python": "python @f",
            "PHP": "php @f",
            "Java": "java @c",
            "C#": "dotnet run",
            "F#": "dotnet run",
            "C++": "@d/@d",
            "Haskell": "./@p",
            # TODO: Support rest of the languages that kattis supports
        },
        "Compile commands": {
            "Java": "javac @f",
            "C++" : "g++ @f -o @d",
            "Haskell": "ghc -ferror-spans -threaded -rtsopts @f -o @p",
        },
        "Naming": {
            "Java": "Pascal",
        },
    }

    for (section, settings) in defaults.items():
        if section not in cfg.sections():
            cfg.add_section(section)
        for (key, value) in settings.items():
            _set(cfg[section], key, value)

    with open(location, "w") as configFile:
        cfg.write(configFile)
    return cfg

def _set(cfgForSection, key, value):
    if not cfgForSection.get(key, False):
        cfgForSection[key] = value

def strToArr(string):
    string = string.replace("[","").replace("]","")
    string = string.replace("'","").replace('"',"")
    return string.split(", ")

def toCommandArray(string: str):
    splitString = string.split(" ")
    return commandConvert(splitString)

def commandConvert(array: list):
    result = []
    cumulator = None
    for item in array:
        if item[0] == '"' or item[0] == "'":
            cumulator = item
        elif cumulator:
            cumulator += " " + item
            if cumulator[-1] == cumulator[0]:
                result.append(cumulator)
                cumulator = None
        else:
            result.append(item)
    return result
