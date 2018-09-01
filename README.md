TODO
# aliaxer
https://img.shields.io/badge/Python%202.7--brightgreen.svg
https://img.shields.io/badge/Python%203%2B--brightgreen.svg

If you need a more robust tool there are alternatives out there such as [Bash-it](https://github.com/Bash-it/bash-it) and others.

usage: aliaxer.py [-h] [-a APPENDER APPENDER] [--append] [--edit] [-f FIND]
                  [--list] [-n NEW] [-r REMOTE] [-t [PICKUP]] [-u UNALIAS]
                  [-v EDITOR]

Basic Terminal Alias File Importer and Aliases Manager.
    
Discovers and sources in the Terminal all files inside the configured directory and remote hosts via curl.

It features options for appending new commands:
- Using a wizard
- Command line stdin
- Inline

In addition, provides the features of file editing (using the OS default editor) and finding an alias for editing.

optional arguments:
  -h, --help            show this help message and exit
  -a APPENDER APPENDER  Appends submitted command as a new alias in the
                        Default alias file. Usage: aliaxer.py -a < alias > <
                        command >.
  --append              Summon a wizard to append an alias.
  --edit                Brings a wizard to select a file to be edited with
                        system defaul editor.
  -f FIND               Search in the files for the requested term.
  --list                Lists all alias files.
  -n NEW                Create a new alias file.
  -r REMOTE             Import from remotes Y/N?
  -t [PICKUP]           Makes an alias with command from stdin and the
                        provided name.
  -u UNALIAS            Unalias the submitted alias for the duration of the
                        Terminal session.
  -v EDITOR             Supported editors: Vim, EMacs, Gedit, Visual Studio
                        Code as vsc.

# Dependencies
## Python < 2.7 
- arparse, https://pypi.python.org/pypi/argparse

# See
- https://www.tldp.org/LDP/abs/html/aliases.html