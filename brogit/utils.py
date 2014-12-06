# coding: utf-8
"""
GIT utility functions without dependencies on sublime API
"""

__all__ = [
    'clean_output',
    'get_git_path',
    'get_head_info',
    'get_module_path',
    'get_remote_repo',
]

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
