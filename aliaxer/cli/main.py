#!/usr/bin/python
import sys
import argparse
import logging
from aliaxer import aliaxer as ax

def controller(root_path=None):
    """ Application for the Terminal """
    
    helpdescription = """Basic Terminal Alias File Importer and Aliases Manager.
    
    Discovers and sources in the Terminal all files inside the configured directory and remote hosts via curl.
    
    It features options for appending new commands:
    - Using a wizard
    - Command line stdin
    - Inline

    In addition, provides the features of file editing (using the OS default editor) and finding an alias for editing.
    """
    parser = argparse.ArgumentParser(description=helpdescription, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-a', dest='appender', default=None, type=str, nargs=2,
                    help='Appends submitted command as a new alias in the Default alias file. Usage: aliaxer.py -a < alias > < command >.')
    parser.add_argument('--append', action="store_true", 
                    help='Summon a wizard to append an alias.')
    parser.add_argument('--compile', action="store_true", 
                    help='Compiles the sourcing file for the Terminal.')
    parser.add_argument('--edit', action="store_true", 
                    help='Brings a wizard to select a file to be edited with system default editor. You must --source aliaxer manually.')
    parser.add_argument('-f', dest='find', default=None, type=str, nargs=1,
                    help='Search in the files for the requested term.')
    parser.add_argument('--list', action="store_true", help='Lists all alias files.')
    parser.add_argument('--new', action="store_true", help='Add a new alias and creates a new aliases file using a wizard.')
    parser.add_argument('-t', dest='pickup', default=None, type=str, nargs='?',
                    help='Makes an alias with command _read from stdin using the provided name.')

    args = parser.parse_args()

    try:
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
            ax._new_aliases_file()
            ax._sourcer(root_path)
            sys.exit(0)
        # -t
        elif args.pickup is not None :
            ax._pickup(args.pickup)
            ax._sourcer(root_path)
            sys.exit(0)
        else:
            ax._quickstart()
            sys.exit(0)
    except Exception as exc:
        template = "{0:s} Aborting.".format(str(exc))
        logging.warning( template )
        sys.exit(1)
