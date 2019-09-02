# Aliaxer

![Python 2.7](https://img.shields.io/badge/Python%202.7--brightgreen.svg)
![Python 3+](https://img.shields.io/badge/Python%203%2B--brightgreen.svg)

Basic Manager for Terminal Aliases and Shell Functions.
    
A very small app written in Python to help you with keeping command aliases and shell functions organized in files located in any directory in your host. 

By storing all your aliases files independent from your Terminal's ```*rc```, ```~/.profile``` or ```~/.aliases``` files you can use version control and/or sync them among hosts.

This app helps you create, manipulate and find aliases, sourcing only the files containing the aliases that you want available in that particular hosts. 

You can ignore files based on name or extension that you specify in the ```config.ini```.

You can also source aliases files located in remote hosts or in the Internet, ideal for system administration of a large number of hosts, Docker's containers deployments, technical support, etc.

You can add aliases by:

- Using a wizard
- Piping up the stdout from other commands or the Terminal history
- Inline

In addition, you can search and edit aliases using your default editor.

### Usage
```bash
usage: aliaxer [-h] [-a APPENDER APPENDER] [--append] [--compile]
               [--configure] [--edit] [-f FIND] [--list] [--new] [--setup]
               [-t [PICKUP]]
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
  --configure           Opens up the config.ini file for editing.
  --edit                Brings up a wizard to select a file to be edited with
                        system default editor.
  -f FIND               Searchs in the aliases files for the requested term.
                        Usage aliaxer -f < string-to-lookup >
  --list                Lists all aliases files.
  --new                 Creates a new aliases file and adds in a new alias
                        using a wizard.
  --setup               Configure Aliaxer for the first time or reset
                        configuration.
  -t [PICKUP]           Makes an alias with a command piped up from Terminal's
                        stdout using the provided name. Usage: < your-
                        terminal-stdout > | aliaxer -t < alias-name >

```

# Set Up

- Clone or fork/clone or download this repo as ZIP
- Create the directory to contain the aliases files and grab its path.
- Determine which file is used by your Terminal for sourcing aliases from. You can find that out in your Terminal configuration file: in Bash usually is ```~/.bashrc``` and ```~/.zshrc``` for Zsh. You may need to uncommend the lines with the import. For example, in Bash that file's path is ```~/.bash_aliases```
- Make ```run.py``` executable by the system: ```chmod u+x ./run.py```
- Run ```run.py``` script for the first time using the ```--setup``` switch: ```./run.py --setup```.
- Close and re-open your Terminal or re-source your ```*rc``` file from the previous step so you can use the app. For better results, closing the Terminal session to get a fresh one is better because re-sourcing does not perform unaliasing.
- The ```aliaxer``` command will then be available for you to summon Aliaxer. Check out its help ```aliaxer -h``` or just ```aliaxer``` to learn about all available options.
- Optionally, you can create a ```remotes``` file for sourcing aliases from remotes files. Please see the *Using Remotes section* for instructions.

### Using Remotes

You can use remotes files (either in your network or on the Internet) to source your aliases from. This is particularly useful when you have to administer a fleet of drone servers with quasi-identical setups or running same tools; also for operating Docker containers, IoT, Arduinos, etc.
 
In order to have your remotes sourced you need to:

- Create a file named ```remotes``` inside your aliases file directory.
- Paste the URL of your aliases onto the file. If you are sourcing more than one remote url add each one on its own line.

For example:

```txt
https://raw.githubusercontent.com/moijafcor/terminal-aliases/master/common
https://raw.githubusercontent.com/moijafcor/terminal-aliases/master/git-flow
```

There is a ancilliary [repository](https://github.com/moijafcor/terminal-aliases) of commonly used aliases that you can play with.

Please beware of the performance consequences on having 'too many' remotes sourced at once, because the lag added by ```curl``` can be noticeable on the loading time of your Terminals.

#### Security

*Avoid using* remote sources of aliases that you don't control yourself or are not properly vetted by you. 

You don't want any command running on your Terminal that you are not certain of what it does.

# Pro Tip

- If you need to see an alias syntax or to find out the appropriate one for a task, use the shell's build in alias listing tool:

```bash
alias | grep < keyword >
```

# Best Practices

When scripting your aliases first consider if a [shell function](https://www.gnu.org/software/bash/manual/bash.html#Shell-Functions) is better suited for your purposes instead of an alias because, as stated on the [Bash Manual](https://www.gnu.org/software/bash/manual/bash.html#Aliases), they are a much more powerful instrument:

> For almost every purpose, shell functions are preferred over aliases.

# Dependencies
## Python < 2.7
If your host is running a Python version older than 2.7 you will need to
install *arparse*.

- arparse: https://pypi.python.org/pypi/argparse

# Alternatives

## The "Classic" Way

Is not foreing practice to use a directory on _*rc_ file for sourcing all files from there, like this:

```bash
if [ -f ~/path/to/directory ]; then
    . ~/path/to/directory/*
fi
```
The problem with this set up is that is not scalable to dozens of boxes, Docker containers and IoT devices; the whole thing is a manual process in order to comment out or remove aliases collections discretionally in function of the box. 

For example, just consider the simple case where your Cloud vendor has re-built a VM in your fleet changing its public IP Address; you will have to propagate the change in a lot of places and -believe me- you will forget to update a bunch of them and stuff will start breaking silently.

In a fleet scenario you need a tool that allows you to source aliases discretionally per host from a single pool of aliases, create aliases on the fly (because a job done in one box surely will have to be done in another drone on your fleet -as hopefully you are deploying inside Availability Sets-) and, among other features, helps you with the offloading of your memory banks in your mind by finding the command that you may need in a given circunstance.

## Bash-it
A robust tool for a single host [Bash-it](https://github.com/Bash-it/bash-it).

# See

- Using Terminal Aliases: https://www.tldp.org/LDP/abs/html/aliases.htmlusage
- Bash Reference Manual, Aliases: https://www.gnu.org/software/bash/manual/bash.html#Aliases
- Bash Reference Manual, Shell Functions: https://www.gnu.org/software/bash/manual/bash.html#Shell-Functions
