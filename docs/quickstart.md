usage: aliaxer [-h] [-a APPENDER APPENDER] [--append] [--compile] [--edit]
               [-f FIND] [--list] [--new] [-t [PICKUP]]

Basic Manager for Terminal Aliases.
    
    Keep aliases in separate files grouped by some organizational criteria 
    in any accessible directory in your host allowing you to version control
    or sync them among hosts.
    
    This app helps you create and manipulate aliases sourcing those files 
    that you want available in the hosts. You can also ignore files based 
    on name or extension that you specify in the config.ini.
    
    You can also source aliases files located in remote hosts or the Internet.
    
    You can add aliases by:
    - Using a wizard
    - Piping up the stdout
    - Inline

    In addition, you can search and edit aliases using your default 
    editor.
    

optional arguments:
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
