# Aliaxer

![Python 2.7](https://img.shields.io/badge/Python%202.7--brightgreen.svg)
![Python 3+](https://img.shields.io/badge/Python%203%2B--brightgreen.svg)

Basic Manager for Terminal Aliases.
    
A very small app written in Python to help you with keeping command aliases organized in files located in any directory in your host. 

By storing all your aliases files independent from your Terminal's _\*rc_, *~/.profile* or *~/.aliases* files you can use version control and/or sync them among hosts.

This app helps you create, manipulate and find aliases, sourcing only the files containing the aliases that you want available in that particular hosts. 

You can also ignore files based on name or extension that you specify in the *config.ini*.

You can also source aliases files located in remote hosts or in the Internet, ideal for system administration of a large number of hosts, Docker's containers deployments, technical support, etc.

You can add aliases by:

- Using a wizard
- Piping up the stdout from other commands or the Terminal history
- Inline

In addition, you can search and edit aliases using your default editor.

### Usage
```bash
aliaxer [-h] [-a APPENDER APPENDER] [--append] [--compile] [--edit]
        [-f FIND] [--list] [--new] [-t [PICKUP]]
```

### Optional Arguments
```bash
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
```
If you need a single host but more robust tool there are alternatives out there such as [Bash-it](https://github.com/Bash-it/bash-it) and others

# Set Up

- Clone or fork/clone or download this repo as ZIP
- Create the directory to contain the aliases files and grab its path. You can use the included 'aliases' directory but is not recommended because its ideal to have versioning for the aliases themselves.
- Determine which file is your terminal sourcing for aliases. In Bash usually is _~/.bashrc_, _~/.zshrc_ for Zsh where that file is sourced. You may need to uncommend the lines with the import.
- Fill in the _config.ini_ settings: *sourced_aliases_path* is the path to the file your terminal import aliases from as seen on previous step; *aliases_dir* is the path to the directory that will contain your aliases files. The rest of the settings IMHO are optional but please take a look at them.
- Run _run.py_ script for the first time using the *--append* switch, create your first alias and verify that every works.
- Optionally, you can create a _remotes_ file for sourcing aliases from remotes files. Please see the *Using Remotes section* for instructions.

### Using Remotes

You can use remotes files (either in your network or on the Internet) to source your aliases from. This is particularly useful when you have to administer a fleet of drone servers whit quasi-identical setups or running same tools; also for operating Docker containers, Arduinos, etc.
 
In to have your remotes sourced you need to:

- Create a file named ```remotes``` inside your aliases file directory.
- Paste the URL onto the file. If you are sourcing more than one remote url add each one on its own line.

For example:

```txt
https://raw.githubusercontent.com/moijafcor/terminal-aliases/master/common
https://raw.githubusercontent.com/moijafcor/terminal-aliases/master/git-flow
```

I maintain [here a repository](https://github.com/moijafcor/terminal-aliases) of commonly used aliases that you can play with.

Please beware of the performance consequences on having 'too many' remotes sourced at once because of the lag added by ```curl``` can be noticeable on the loading time of your terminals.

#### Security

*Avoid using* remote sources of aliases that you don't control yourself or are not properly vetted by you. 

You don't want any command running on your terminal that you are not certain of what it does.

# Dependencies
## Python < 2.7
If your host is running a Python version older than 2.7 you will need to
install *arparse*.

- arparse: https://pypi.python.org/pypi/argparse

# See

- Using Terminal Aliases: https://www.tldp.org/LDP/abs/html/aliases.htmlusage