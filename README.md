# Aliaxer

![Python 2.7](https://img.shields.io/badge/Python%202.7--brightgreen.svg)
![Python 3+](https://img.shields.io/badge/Python%203%2B--brightgreen.svg)

Basic Manager for Terminal Aliases.
    
A very small app written in Python to help you with keeping command aliases organized in files located in any directory in your host. 

By storing all your aliases files independent from your Terminal's *rc, ~/.profile or ~/.aliases files you can use version control and/or sync them among hosts.

This app helps you create, manipulate and find aliases, sourcing only the files containing the aliases that you want available in that particular hosts. 

You can also ignore files based on name or extension that you specify in the config.ini.

You can also source aliases files located in remote hosts or in the Internet, ideal for system administration of a large number of hosts, Docker's containers deployments, technical support, etc.

You can add aliases by:
- Using a wizard
- Piping up the stdout from other commands or the Terminal history
- Inline

In addition, you can search and edit aliases using your default editor.

### Usage
```
aliaxer [-h] [-a APPENDER APPENDER] [--append] [--compile] [--edit]
        [-f FIND] [--list] [--new] [-t [PICKUP]]
```

### Optional Arguments

  -h, --help            show this help message and exit
  -a APPENDER APPENDER  Appends submitted command as a new alias onto the
                        Default alias file. Usage: aliaxer -a < alias > <
                        command >.
  --append              Summons a wizard to append an alias to an aliases
                        file.
  --compile             Compiles the sourcing file for the Terminal.
  --edit                Brings up a wizard to select a file to be edited with
                        system default editor.
  -f FIND               Searchs in the aliases files for the requested term.
                        Usage aliaxer -f < string-to-lookup >
  --list                Lists all aliases files.
  --new                 Creates a new aliases file and adds in a new alias
                        using a wizard.
  -t [PICKUP]           Makes an alias with a command piped up from Terminal's
                        stdout using the provided name. Usage: < your-
                        terminal-stdout > | aliaxer -t < alias-name >

If you need a single host but more robust tool there are alternatives out there such as [Bash-it](https://github.com/Bash-it/bash-it) and others.

# Dependencies
## Python < 2.7
If your host is running a Python version older than 2.7 you will need to
install *arparse*.

- arparse: https://pypi.python.org/pypi/argparse

# See

- Using Terminal Aliases: https://www.tldp.org/LDP/abs/html/aliases.htmlusage