# coding: utf-8
"""
Sublime Text Plugin opening GIT source code in a browser.

Supports Bitbucket and GitHub
"""

# __all__ = ['BrowseGitCommand']

import sublime, sublime_plugin, webbrowser

# from .git_utils import *

import os

from subprocess import check_output, CalledProcessError


def clean_output(*args, **kwargs):
    "Return decoded and stripped output of check_output"
    return check_output(*args, **kwargs).decode().rstrip()


def get_remote_repo(name='origin'):
    "Return dictionary with parsed address of remote repository or None"
    try:
        data = clean_output(['git', 'remote', '-v']).split()
    except (OSError, CalledProcessError):
        return None
    # build dictionary of (remote_name, remote_addr)
    remotes = dict(tuple(data[i:i+2]) for i in range(0, len(data), 3))
    origin = remotes.get(name, '')
    try:
        url, path = origin.split(':')
        host = url.split('@')[-1]
        owner, repository = path.split('/', 2)
    except ValueError:
        return None
    else:
        return {
            'host': host,
            'owner': owner,
            'repository': repository[:-4],  # strip .git
        }


def get_git_path(file_path):
    "Return relative GIT path in repository for given file_path"
    from os.path import sep, isdir, join, dirname
    git_dir = dirname(file_path)
    # local repository name can differ from remote, so
    # traverse git_dir from bottom to top until it has .git
    while git_dir and git_dir != sep and not isdir(join(git_dir, '.git')):
        git_dir = dirname(git_dir)
    return file_path[len(git_dir):]


def get_head_info():
    "Return dictionary with the current GIT branch and commit"
    return dict(
        branch=clean_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']),
        commit=clean_output(['git', 'rev-parse', 'HEAD'])
    )


def get_module_path(file_path):
    "Return Python module path for given file_path"
    path = os.path.dirname(file_path)
    name = os.path.splitext(os.path.basename(file_path))[0]
    module_path = []
    init_path = os.path.join(path, '__init__.py')
    while os.path.isfile(init_path):
        module_path.append(name)
        name = os.path.basename(path)
        path = os.path.dirname(path)
        init_path = os.path.join(path, '__init__.py')
    module_path.append(name)
    return '.'.join(module_path[::-1])


# pylint: disable=line-too-long
GIT_HOSTINGS = {
    'bitbucket.org': 'https://bitbucket.org/{owner}/{repository}/src/{commit}{path}?at={branch}#cl-{line}',
    'github.com': 'https://github.com/{owner}/{repository}/blob/{branch}{path}#L{line}',
}
# pylint: enable=line-too-long


class BrowseGitCommand(sublime_plugin.ApplicationCommand):

    def run(self, *args):
        import sys
        window = sublime.active_window()
        view = window.active_view()
        row, col = view.rowcol(view.sel()[0].a)  # current position of cursor
        file_path = view.file_name()
        # sys.stdout.write(file_path+'\n')
        if not file_path:
            return
        url_info = get_remote_repo()
        # sys.stdout.write(repr(url_info)+'\n')
        if not url_info:
            return
        url_info.update(get_head_info())
        url_info['path'] = get_git_path(file_path)
        url_info['line'] = row + 1
        sys.stdout.write(repr(url_info) + '\n')
        try:
            url_tpl = GIT_HOSTINGS[url_info['host']]
            url = url_tpl.format(**url_info)
        except KeyError as exc:
            sys.stderr.write(repr(exc))
            return
        sys.stdout.write(url + '\n')
        webbrowser.open_new(url)
        # show Python module path in status bar
        # view.set_status('', '@' + get_module_path(file_path))
