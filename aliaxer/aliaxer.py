try:
    import datetime
    import logging
    import logging.config
    import logging.handlers
    import os
    import re
    import select
    from shutil import copyfile
    import sys
    import webbrowser
    if sys.version_info[0] == 3:
        from configparser import ConfigParser
    else:
        from ConfigParser import ConfigParser
except ImportError as e:
    raise Exception(e)

def _append_alias(appendto=None):
    """ Appends an alias using a wizard to help out creating the alias. 

    Keyword arguments:
    appendto -- File path to append alias to

    User input fields:
    alias_name -- Name for the alias
    alias_command -- command
    alias_comment -- Optional comment for the alias (default None)
    """
    alias_name = None
    alias_command = None
    alias_comment = None
    template_comment = None
    template_alias = None

    if not appendto:
        f = _get_file_from_user_prompt()
    else:
        f = appendto

    is_remote = False
    if 'remotes' in f:
        is_remote = True

    if sys.version_info[0] == 3:
        if not is_remote:
            alias_name = str(input("Enter alias name: ")).strip()
            alias_command = str(input("Type in command: ")).strip()
            alias_comment = str(input("Type in comment (optional): ")).strip()
        else:
            alias_command = str(input("Type in command: ")).strip()
    else:
        if not is_remote:
            alias_name = raw_input("Enter alias name: ").strip()
            alias_command = raw_input("Type in command: ").strip()
            alias_comment = raw_input("Type in comment (optional): ").strip()
        else:
            alias_command = raw_input("Type in command: ").strip()
    if (not alias_name and not is_remote) or not alias_command:
        raise ValueError("Error x002: The alias must have a name"
                         " and/or a command.")
    if alias_comment:
        template_comment = "#{0:s}\n".format(alias_comment)
    if '\'' in alias_command:
        sqts = '"'
    else:
        sqts = "'"

    if is_remote:
        template_alias = "{0:s}\n".format(alias_command)
    else:
        template_alias = "alias {0:s}={2:s}{1:s}{2:s}\n".format(
            alias_name, alias_command, sqts)

    if template_comment:
        payload = template_comment + template_alias
    else:
        payload = template_alias

    return _writer(f, payload)


def _appender_alias(arguments):
    """ 
    Appends an alias from the command line into the default alias file. 
    Format: < alias > < command >. 

    Keyword arguments:
    arguments -- List with the arguments to build the string to be appended.
    """
    alias_name, alias_command = arguments
    if '\'' in alias_command:
        sqts = '"'
    else:
        sqts = "'"
    payload = "alias {0:s}={2:s}{1:s}{2:s}\n".format(
        alias_name, alias_command, sqts)
    return _writer(_get_path_default_file(), payload)


def _check_config():
    """ Verifies that settings and/or system dependencies are met """
    cf = _get_path_user() + 'config.ini'
    mm = 'Missing config.ini file at < %s >.' \
    ' Please run Aliaxer with --setup option.'
    mp = 'Required config.ini parameter < %s > missing.'
    if not os.path.exists(cf):
        raise Exception(mm % _get_path_user())
    config = ConfigParser()
    config.read(cf)
    req = ['sourced_aliases_path', 'aliases_dir']
    for r in req:
        if not config.get('filesystem', r):
            raise Exception(mp % r)
    return

def _configure():
    """ Opens up the config.ini file for editing. """
    home = _get_path_user()
    if not os.path.exists(home + 'config.ini'):
        er = 'You do not have a config.ini in < %s >.'\
        ' Please run Aliaxer with the --setup option instead.'
        raise Exception(er %home)
    return webbrowser.open(home + 'config.ini')

def _edit_file():
    """ Brings a wizard to select the file to be edited
     using system defaul editor. """
    fpath = _get_file_from_user_prompt()
    webbrowser.open(fpath)
    return True


def _finder(target):
    """ Searches for presence of target in the aliases files 

    Keyword arguments:
    target -- Search term
    """
    s = target[0]
    suspects = _scouer(_get_dir())
    result = []
    for suspect in suspects:
        f = open(suspect, "r")
        for line in f.readlines():
            line = line.strip()
            parts = line.split("=")
            for part in parts:
                if s in part:  # TODO: Print alias + command + comments
                    result.append(suspect.strip())
    return result


def _get_config(group, key, default=None):
    """ Retrieves configuration parameters from config.ini 

    Keyword arguments:
    group -- Parent group
    key -- Key to retrieve from group
    """
    v = None
    booleankeys = ['remotes', 'backup_sourced_before_save']
    config = ConfigParser()
    config.read(_get_path_user() + 'config.ini')
    try:
        if key in booleankeys:
            v = config.getboolean(group, key)
        else:
            v = config.get(group, key)
    except:
        if default:
            return default
        else:
            raise
    if not v and default:
        return default
    return v


def _get_dir():
    """ Returns the path to alias file collection """
    try:
        conf_path = _get_config('filesystem',
                                'aliases_dir').rstrip("/").strip() + os.path.sep
        relpath = os.path.sep + conf_path
        abpath = os.getcwd() + os.path.sep + conf_path
        scanned_dirs = '{0:s} or ../{1:s} nor {2:s}'.format(
            relpath, relpath, abpath)
        if not os.path.isabs(conf_path):
            #Maybe the user is using a directory inside Aliaxer's install
            here = os.path.abspath(os.path.dirname(__file__))
            if os.path.exists(conf_path):
                return conf_path
            elif os.path.exists(here + '/../' + conf_path):
                return here + '/../' + conf_path
            else:
                raise OSError("Error x001: %s do not exist or lack proper"
                              " permissions." % scanned_dirs)
        else:
            if os.path.exists(conf_path):
                return conf_path
            else:
                raise OSError("Error IOx001: %s do not exist or lack proper"
                              " permissions." % scanned_dirs)
    except OSError as e:
        _logger(e)
        raise


def _get_path_default_file():
    """ Returns the path to the configured Default file for new aliases.

    If the default file does not exist is then created.
    """
    default = _get_config('filesystem', 'default_aliases_file')
    if not default:
        raise ValueError("No default file has been specified in config.ini.")
    path = _get_dir() + default
    if not os.path.exists(path):
        with open(path, 'w'):
            os.utime(path, None)
    return path

def _get_path_user():
    """ Returns the path to directory for User local operational files.
    
    This directory holds configuration, logs and personalizations for the User.
    """
    return os.environ["HOME"] + os.path.sep + '.aliaxer' + os.path.sep


def _get_file_from_user_prompt():
    """ Prints indexed list to select a file from, returning full path to
     file."""
    file_names = _scouer(_get_dir(), True)
    file_paths = _scouer(_get_dir())
    matrix_paths = dict(zip(range(len(file_paths)), file_paths))
    matrix_names = dict(zip(range(len(file_names)), file_names))
    for index, name in matrix_names.items():
        print("[ {0:d} ] {1:s}".format(index, name))
    print("[ q ] ### To Exit App ###")
    tries = int(_get_config('preferences', 'number_tries', 5))
    for i in range(0, tries):
        while True:
            try:
                if sys.version_info[0] == 3:
                    selection = input("Please enter number to select file"
                                      " or 'q' to exit the app: ")
                else:
                    selection = raw_input("Please enter number to select file"
                                          " or 'q' to exit the app: ")
                if selection == 'q':
                    print('Good bye!')
                    sys.exit(0)
                s = int(selection)
                print('Selected: ', matrix_names[s])
                if len(file_paths) >= s:
                    return matrix_paths[s]
                else:
                    raise Exception("Selection (%s) is not"
                                    " a valid option." % selection)
            except Exception as e:
                t = tries - (i + 1)
                if t == 0:
                    raise Exception('You ran out of tries.')
                else:
                    print(e)
                    print('{0:1} more tries left'.format(t))
                    break


def _get_remotes():
    """ Return a list of URLs from remote aliases file."""
    r = []
    fs = _scouer(_get_dir(), quiet=True)
    for n in fs:
        if 'remotes' in n:
            with open(n, "r") as l:
                for s in l:
                    if '#' in s:
                        continue
                    r.append(s)
    return r


def _list_aliases():
    """ Print a list of aliases file in the scanned directory. """
    file_names = _scouer(_get_dir(), True)
    print("Sourcing files from directory:\n%s" % _get_dir())
    matrix_names = dict(zip(range(len(file_names)), file_names))
    for index, name in matrix_names.items():
        print("{0:d}) {1:s}".format(index + 1, name))

def _logger(msg, level='WARNING'):
    """ A very basic wrapper for the logging module.
    
    Writes to log file only on ERROR level logs.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Aliaxer")

    if level is 'INFO':
        logger.setLevel(logging.INFO)
        logger.info(msg)
    elif level is 'ERROR':
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(_get_path_user() + "error.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - '\
        '%(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.error(msg)
    else:
        logger.setLevel(logging.WARNING)
        logger.warning(msg)
    return


def _new_aliases_file():
    """ Using a wizard, add a new alias and creates a new aliases 
    file inside <aliases_dir>. """
    if sys.version_info[0] == 3:
        alias_filename = str(input("Enter new file name: ")).strip()
    else:
        alias_filename = str(raw_input("Enter new file name: ")).strip()
    nf = _get_dir() + _slugify(alias_filename) + _get_config('preferences',
                                                             'file_extension')
    if os.path.exists(nf):
        raise Exception('The file %s already exists.' % nf)
    with open(nf, 'w'):
        os.utime(nf, None)
    return nf


def _pickup(alias_name):
    """ Appends alias from stdin with the given name. 

    Keyword arguments:
    alias_name -- Name for the alias
    """
    if not select.select([sys.stdin, ], [], [], 0.0)[0]:
        raise ValueError("No piped data has been provided.")
    for line in sys.stdin:
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
        with open(filename, 'r') as f:
            buf.append(f.read())
    return sep.join(buf)


def _scouer(dir_path, name_only=False, quiet=False):
    """ Scans for files in the configured directory

    Returns a sorted list ignoring hidden files.

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
        if not quiet:
            _logger(str(exc))
        raise

    for infile in listing:
        filename, file_extension = os.path.splitext(infile)
        if 'remotes' in filename:
            if _get_config('ignore', 'remotes'):
                if not quiet:
                    _logger('Ignoring file ' + filename)
                continue
        if filename.startswith("."):
            continue
        if file_extension in ignore_f_ext.split(","):
            if not name_only:
                if not quiet:
                    _logger('Ignoring file '
                                    + filename + file_extension)
            continue
        if filename+file_extension in ignore_file.split(","):
            if not name_only:
                if not quiet:
                    _logger('Ignoring file '
                                    + filename + file_extension)
            continue

        if name_only:
            source = filename + file_extension
        else:
            source = dir_path + filename + file_extension

        sourceable.append(source)

    sourceable.sort()

    return sourceable


def _slugify(value):
    """
    Convert spaces to hyphens. Remove characters that aren't
    alphanumerics, underscores, or hyphens. Convert to lowercase. Also strip
    leading and trailing whitespace.

    Ideas taken with love from Django
    https://github.com/django/django/blob/master/django/template/defaultfilters.py
    """
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value


def _sourcer(root_path=None):
    """ Compiles and saves aliases file's paths and remote URLs to be sourced 
    by the Terminal.

    The <sourced_aliases_path> parameter on config.ini determines what file is
     used. That file must be sourced by the Terminal, either on runtime (on 
     user log in) for the length of the session or permanently using the 
     terminal's rc file (.bashrc, .zshrc, etc.).

    If the ~.aliases file is used on <sourced_aliases_path> no sourcing is 
    necessary as that file is automatically sourced on most distros, MacOS and 
    Ubuntu on Windows.

    Before writing on the <sourced_aliases_path> a time-stamped backup is 
    created using its base name and stored at the same location.
    """
    sfpath = _get_config('filesystem', 'sourced_aliases_path')
    flag_remotes = _get_config('ignore', 'remotes')
    afs = _scouer(_get_dir())
    afs.sort(reverse=True)
    try:
        if os.path.exists(sfpath):
            backup_flag = _get_config('preferences',
                                      'backup_sourced_before_save')
            if backup_flag:
                last_ed = os.path.getmtime(sfpath)
                now = datetime.datetime.fromtimestamp(last_ed).strftime(
                    "%b%d%Y%H")
                os.rename(sfpath, sfpath + '-' + now)
            with open(sfpath, "w+") as fh:
                app_alias_template = "alias aliaxer='{0:s}/run.py'\n".format(
                    root_path)
                fh.write(app_alias_template)
                for af in afs:
                    if 'remotes' in af:
                        if flag_remotes:
                            continue
                        else:
                            for r in _get_remotes():
                                rtemplate = 'source <(curl -sS {0:s})\n'.format(
                                    r.strip())
                                fh.write(rtemplate)
                                print(rtemplate)
                    else:
                        ftemplate = 'source {0:s}\n'.format(af)
                        fh.write(ftemplate)
                        print(ftemplate)
        return True
    except Exception as exc:
        _logger(str(exc))
        raise


def _setup():
    """ Installs the main application 

    Clients for the application must implement their own installation
    checks and deployment workflow.
    """
    home = _get_path_user()
    if os.path.exists(home + 'config.ini'):
        er = 'You already have a config.ini in < %s >.'\
        ' Please run Aliaxer with the --configure option instead.'
        raise Exception(er %home)
    try:
        if not os.path.exists(home):
            os.makedirs(home)
        here = os.path.abspath(os.path.dirname(__file__))
        cf = here + '/../template.config.ini'
        copyfile(cf, home + 'config.ini')
    except Exception as e:
        raise Exception(e)
    return True
    


def _version(app='library'):
    """ Returns version numbers """
    here = os.path.abspath(os.path.dirname(__file__))
    vf = here + '/version.ini'
    m = 'Missing version.ini file or parameter not provided.'
    if not os.path.exists(vf):
        raise Exception(m)
    config = ConfigParser()
    config.read(vf)
    return config.get('sc', app)


def _writer(file_path, payload):
    """ Writes to a file preserving its old content. 

    Keyword arguments:
    file_path -- Full path to aliases file
    payload -- String to append to file
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, "a") as f:
                f.write(payload)
        return True
    except FileNotFoundError as exc:
        _logger(str(exc))
        return False
