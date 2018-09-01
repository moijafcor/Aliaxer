#!/usr/bin/python
try:
    import os
    import datetime
    import logging
    import sys
    import logging.handlers
    import webbrowser
    import select
    from configparser import ConfigParser
except ImportError:
    # Python < 3.0
    from ConfigParser import ConfigParser

def _append_alias():
    """ Appends an alias using a wizard to help out creating the alias. 

    Keyword arguments:
    alias_name -- Name for the alias
    alias_command -- command
    alias_comment -- Optional comment for the alias (default None)
    """
    alias_name = None
    alias_command = None
    alias_comment = None
    template_comment = None
    template_alias = None

    f = _get_file_from_user_prompt()
    is_remote = False
    if 'remotes' in f:
        is_remote = True
        
    if sys.version_info[0] == 3 :
        if not is_remote :
            alias_name = str(input("Enter alias name: ")).strip()
            alias_command = str(input("Type in command: ")).strip()
            alias_comment = str(input("Type in comment (optional): ")).strip()
        else:
            alias_command = str(input("Type in command: ")).strip()
    else:
        if not is_remote :
            alias_name = raw_input("Enter alias name: ").strip()
            alias_command = raw_input("Type in command: ").strip()
            alias_comment = raw_input("Type in comment (optional): ").strip()
        else:
            alias_command = raw_input("Type in command: ").strip()

    if (not alias_name and not is_remote) or not alias_command :
       raise ValueError("Error x002: The alias must have a name and/or a command.")
    if alias_comment :
        template_comment = "#{0:s}\n".format(alias_comment)
    if '\'' in alias_command :
        sqts = '"'
    else:
        sqts = "'"

    if is_remote :
        template_alias = "{0:s}\n".format(alias_command)
    else :
        template_alias = "alias {0:s}={2:s}{1:s}{2:s}\n".format(alias_name, alias_command, sqts)
    
    if template_comment :
        payload = template_comment + template_alias
    else :
        payload = template_alias
        
    return _writer(f, payload)

def _appender_alias(arguments):
    """ 
    Appends an alias from the command line into the default alias file. Format: < alias > < command >. 

    Keyword arguments:
    arguments -- List with the arguments to build the string to be appended.
    """
    alias_name, alias_command = arguments
    if '\'' in alias_command :
        sqts = '"'
    else:
        sqts = "'"
    payload = "alias {0:s}={2:s}{1:s}{2:s}\n".format(alias_name, alias_command, sqts)
    return _writer(_get_path_default_file(), payload)

def _check_config():
    """ Verifies all mandatory settings and system dependencies are met """
    #TODO: 
    return

def _edit_file():
    """ Brings a wizard to select the file to be edited using system defaul editor. """
    fpath = _get_file_from_user_prompt()
    webbrowser.open(fpath)
    return

def _finder(target):
    """ Searches for presence of target in the aliases files 
    
    Keyword arguments:
    target -- Search term
    """
    s = target[0]
    suspects = _scouer(_get_dir())
    result = []
    for suspect in suspects :
        f = open(suspect, "r")
        for line in f.readlines():
            line = line.strip()
            parts = line.split("=")
            for part in parts:
                if s in part:
                    result.append(suspect.strip())
    return result

def _get_config(group, key):
    """ Retrieves configuration parameters from config.ini 
    
    Keyword arguments:
    group -- Parent group
    key -- Key to retrieve from group
    """
    v = None
    booleankeys = ['remotes', 'backup_sourced_before_save']
    config = ConfigParser()
    here = os.path.abspath(os.path.dirname(__file__))
    config.read(here + '/../config.ini')
    try :
        if key in booleankeys :
            v = config.getboolean(group, key)
        else :
            v = config.get(group, key)
    except :
        raise
    return v

def _get_dir():
    """ Returns the path to alias file collection """
    try:
        conf_path = _get_config('filesystem', 'aliases_dir')
        relpath = os.path.sep + conf_path
        abpath = os.getcwd() + os.path.sep + conf_path
        scanned_dirs = '{0:s} or ../{1:s} nor {2:s}'.format(relpath, relpath, abpath)
        if not os.path.isabs(conf_path):
            here = os.path.abspath(os.path.dirname(__file__))
            if os.path.exists(conf_path):
                return conf_path
            elif os.path.exists(here + '/../' + conf_path):
                return here + '/../' + conf_path
            else:
                raise OSError("Error x001: %s do not exist or lack proper permissions." %scanned_dirs)
        else :
            if os.path.exists(conf_path):
                return conf_path
            else:
                raise OSError("Error IOx001: %s do not exist or lack proper permissions." %scanned_dirs)
    except OSError as e:
        logging.warning( e )
        raise

def _get_path_default_file():
    """ Returns the path to the configured Default file for new aliases """
    default = _get_config('filesystem', 'default_aliases_file')
    if not default :
        raise ValueError("No default file has been specified in config.ini.")
    path = _get_dir() + os.path.sep + default
    return path

def _get_file_from_user_prompt():
    """ Prints indexed list to select a file from, returning full path to file."""
    file_names = _scouer(_get_dir(), True)
    file_paths = _scouer(_get_dir())
    matrix_paths = dict(zip(range(len(file_paths)),file_paths))
    matrix_names = dict(zip(range(len(file_names)),file_names))
    for index, name in matrix_names.items():
        print("[ {0:d} ] {1:s}".format(index, name))
    print("[ q ] ### To Exit App ###")
    tries = 5
    for i in range(0,tries):
        while True:
            if sys.version_info[0] == 3 :
                selection = input("Please enter number to select file or 'q' to exit the app: ")
            else:
                selection = raw_input("Please enter number to select file or 'q' to exit the app: ")
            if selection == 'q':
                print('Good bye!')
                sys.exit(0)
            try:
                lc = len(file_paths)
                print('number of files: ', lc)
                s = int(selection)
                print('selected: ', s)
                print(type(lc))
                if s <= lc:
                    print('bingo!', matrix_paths[selection])
                    p = matrix_paths[selection]
                    return p
                else:
                    raise Exception("Selection (%s) is not a valid option." %selection)
                    i +=1
                    continue
            except Exception as e:
                print(e)
                t = tries - (i + 1)
                print('{0:1} more tries left'.format(t))
                break

def _get_remotes():
    """ Return a list of URLs from remote aliases file honoring config.ini setting. """
    r = []
    fs = _scouer(_get_dir(), quiet=True)
    for n in fs :
        if 'remotes' in n :
            with open(n, "r") as l :
                for s in l :
                    if '#' in s :
                        continue
                    r.append(s)
    return r

def _list_aliases():
    """ Print a list of aliases file in the scanned directory. """
    file_names = _scouer(_get_dir(), True)
    print("Sourcing files from directory:\n%s" %_get_dir())
    matrix_names = dict(zip(range(len(file_names)),file_names))
    for index, name in matrix_names.items():
        print("{0:d}) {1:s}".format(index + 1, name))

def _new_aliases_file():
    """ Using a wizard, add a new alias and creates a new aliases file insde <aliases_dir>. """
    #TODO:
    return

def _pickup(alias_name):
    """ Appends alias from stdin with the given name. 
    
    Keyword arguments:
    alias_name -- Name for the alias
    """
    if not select.select([sys.stdin,],[],[],0.0)[0] :
        raise ValueError("No piped data has been provided.")
    for line in sys.stdin :
        stin = line.strip('\n')
        # We are picking up only one argument
        break 
    return _appender_alias([alias_name, stin])

def _quickstart():
    """ How to use """
    here = os.path.abspath(os.path.dirname(__file__))
    print(_read(here + '/../docs/quickstart.md'))

def _read(*filenames, **kwargs):
    """ A file _reader taken from sowehere """
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with open(filename,'r') as f:
            buf.append(f.read())
    return sep.join(buf)

def _scouer(dir_path, name_only = False, quiet = False):
    """ Scans for files in the configured directory returning a sorted list, ignoring hidden files.

    Keyword arguments:
    dir_path -- Path to directory
    name_only -- Flag to retrieve file names with no paths (default False)
    quiet -- Do not log or print debug info (default False)
    """
    ignore_f_ext = _get_config('ignore', 'file_ext')
    ignore_file = _get_config('ignore', 'file')
    sourceable = []

    try:
        listing = os.listdir(dir_path)
    except Exception as exc:
        if not quiet :
            logging.warning(str(exc))
        raise

    for infile in listing:

        filename, file_extension = os.path.splitext(infile)

        if 'remotes' in filename :
            if _get_config('ignore', 'remotes') :
                if not quiet :
                    logging.warning('aliaxer ignoring file ' + filename)
                continue
        if filename.startswith("."):
            continue
        if file_extension in ignore_f_ext.split(","):
            if not name_only :
                if not quiet :
                    logging.warning('aliaxer ignoring file ' + filename + file_extension)
            continue
        if filename+file_extension in ignore_file.split(","):
            if not name_only :
                if not quiet :
                    logging.warning('aliaxer ignoring file ' + filename + file_extension)
            continue

        if name_only :
            source = filename + file_extension
        else:
            source = dir_path + os.path.sep + filename + file_extension

        sourceable.append(source)

    sourceable.sort()
    
    return sourceable

def _sourcer(root_path=None):
    """ Compiles and saves the aliases file's paths and remote URLs to be sourced by the Terminal.
    
    The <sourced_aliases_path> parameter on config.ini determines what file is used. 
    That file must be sourced by the Terminal, either on runtime (on user log in) for the length
    of the session or permanently using the terminal's rc file (.bashrc, .zshrc, etc.).

    If the ~.aliases file is used on <sourced_aliases_path> no sourcing is necessary as that file is
    automatically sourced on most distros, MacOS and Ubuntu on Windows.

    Before writing on the <sourced_aliases_path> a time-stamped backup is created using its base
    name and stored at the same location.
    """
    sfpath = _get_config('filesystem', 'sourced_aliases_path')
    flag_remotes = _get_config('ignore', 'remotes')
    afs = _scouer(_get_dir())
    afs.sort(reverse=True)
    try:
        if os.path.exists(sfpath):
            backup_flag = _get_config('preferences', 'backup_sourced_before_save')
            if backup_flag:
                last_ed = os.path.getmtime(sfpath)
                now = datetime.datetime.fromtimestamp(last_ed).strftime("%b%d%Y%H")
                os.rename(sfpath, sfpath + '-' + now)
            with open(sfpath, "w+") as fh:
                app_alias_template = "alias aliaxer='{0:s}/run.py'\n".format(root_path)
                fh.write(app_alias_template)
                for af in afs :
                    if 'remotes' in af :
                        if flag_remotes :
                            continue
                        else :
                            for r in _get_remotes() :
                                rtemplate = 'source <(curl -sS {0:s})\n'.format(r)
                                fh.write(rtemplate)
                                print(rtemplate)
                    else :
                        ftemplate = 'source {0:s}\n'.format(af)
                        fh.write(ftemplate)
                        print(ftemplate)
        return True
    except Exception as exc:
        logging.warning(str(exc))
        raise

def _writer(file_path, payload):
    """ Writes to a file preserving its old content. 
    
    Keyword arguments:
    file_path -- Full path to aliases file
    payload -- String to append to file
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, "r+") as f:
                dirty = f.read()
                f.seek(0)
                f.write(payload + dirty)
        return True
    except FileNotFoundError as exc:
        logging.warning(str(exc))
        return False
