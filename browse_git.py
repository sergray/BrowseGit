# coding: utf-8
"""
Sublime Text Plugin opening GIT source code in a browser.

Supports Bitbucket and GitHub
"""

__all__ = ['BrowseGitCommand']

import sys

import sublime, sublime_plugin, webbrowser

from .brogit.utils import (
    clean_output, get_git_path, get_head_info, get_remote_repo,
)


# pylint: disable=line-too-long
GIT_HOSTINGS = {
    'bitbucket.org': 'https://bitbucket.org/{owner}/{repository}/src/{commit}{path}?at={branch}#cl-{line}',
    'github.com': 'https://github.com/{owner}/{repository}/blob/{branch}{path}#L{line}',
}
# pylint: enable=line-too-long


class BrowseGitCommand(sublime_plugin.ApplicationCommand):

    def run(self, *args):
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
        sys.stdout.write("Open URL {} in browser".format(url))
        webbrowser.open_new(url)
        # show Python module path in status bar
        # view.set_status('', '@' + get_module_path(file_path))
