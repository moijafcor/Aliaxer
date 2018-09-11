#!/usr/bin/python
import sys
import argparse
from aliaxer import aliaxer as ax

def controller(root_path=None):
    """ Application for the Terminal """
    
    helpdescription = """Basic Manager for Terminal Aliases and Functions.
    
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
    """
    parser = argparse.ArgumentParser(prog='aliaxer',
        description=helpdescription,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-a', dest='appender', default=None,
        type=str, nargs=2,
        help='Appends submitted command as a new alias'
        ' onto the Default alias file.'
        ' Usage: aliaxer -a < alias > < command >.')
    parser.add_argument('--append', action="store_true", 
        help='Summons a wizard to append an alias to an aliases file.')
    parser.add_argument('--compile', action="store_true", 
        help='Compiles the sourcing file for the Terminal.')
    parser.add_argument('--configure', action="store_true", 
        help='Opens up the config.ini file for editing.')
    parser.add_argument('--edit', action="store_true", 
        help='Brings up a wizard to select a file to be edited'\
        ' with system default editor.')
    parser.add_argument('-f', dest='find', default=None, type=str, nargs=1,
        help='Searchs in the aliases files for the requested term. '
        'Usage aliaxer -f < string-to-lookup >')
    parser.add_argument('--list', action="store_true", 
        help='Lists all aliases files.')
    parser.add_argument('--new', action="store_true", 
        help='Creates a new aliases file and adds in a new'\
        ' alias using a wizard.')
    parser.add_argument('--setup', action="store_true", 
        help='Configure Aliaxer for the first time or reset configuration.')
    parser.add_argument('-t', dest='pickup', default=None, type=str, 
        nargs='?', help='Makes an alias with a command'
        ' piped up from Terminal\'s stdout using the'
        ' provided name. Usage: '
        '< your-terminal-stdout > | aliaxer -t < alias-name >')

    try:
        args = parser.parse_args()
        if args.setup or args.configure:
            pass
        else:
            ax._check_config()
        # --append
        if args.append :
            ax._append_alias()
            ax._sourcer(root_path)
            sys.exit(0)
        # -a
        elif args.appender is not None :
            ax._appender_alias(args.appender)
            ax._sourcer(root_path)
            sys.exit(0)
        # --compile
        elif args.compile :
            ax._sourcer(root_path)
            sys.exit(0)
        # --configure
        elif args.configure :
            ax._configure()
            sys.exit(0)
        # --edit
        elif args.edit :
            ax._edit_file()
            sys.exit(0)
        # -f
        elif args.find is not None :
            out = ax._finder(args.find)
            s = len(out)
            if s > 1:
                print(out)
                sys.exit(0)
            elif s == 1:
                sys.exit(out[0])                
            else:
                print("'%s' not found" %args.find[0])
                sys.exit(1)
        # --list
        elif args.list :
            ax._list_aliases()
            sys.exit(0)
        # --new
        elif args.new :
            nf = ax._new_aliases_file()
            ax._append_alias(nf)
            ax._sourcer(root_path)
            sys.exit(0)
        # -t
        elif args.pickup is not None :
            ax._pickup(args.pickup)
            ax._sourcer(root_path)
            sys.exit(0)
        # --setup
        elif args.setup :
            ax._setup()
            ax._configure()
            sys.exit(0)
        else:
            ax._quickstart()
            print('Lib V. ' + ax._version('library'))
            print('CLI V. ' + ax._version('cli'))
            sys.exit(0)
    except Exception as e:
        template = "{0:s} Aborting.".format(str(e))
        ax._logger( template )
        sys.exit(1)
