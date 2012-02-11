#!/usr/bin/python
import os
import re
import operator
import UserList
import sublime
import sublime_plugin


class Symbol(sublime.Region):
    def __init__(self, view, a, b):
        sublime.Region.__init__(self, a, b)
        self.view = view
        self.file = self.get_file()
        self.filename = self.get_filename()
        self.line = self.get_line()
        self.name = self.get_name()

    def __str__(self):
        return "%s[:%s] %s" % (self.file, self.line, self.name)

    def db(self):
        print self

    def get_line(self):
        return self.view.rowcol(self.begin())[0] + 1

    def get_file(self):
        return self.view.file_name()

    def get_filename(self):
        file = self.get_file()
        if file:
            return file.split(os.path.sep)[-1]

    def get_name(self):
        name = self.view.substr(self)
        # alignement ??
        matches = re.compile('(.+)').findall(name)
        if matches:
            name = matches[0]
        return name


class SymbolList(UserList.UserList):
    def sort(self):
        self.sort(key=operator.attrgetter('name'))

    def find(self, symbol):
        results = []
        if symbol and symbol.name:
            for _symbol in self.data:
                if symbol.name in _symbol.name:
                    results.append(_symbol)
        return results

    def clear_view(self, view):
        file = view.file_name()
        entries = self.data
        if file and entries:
            self.data = []
            for entry in entries:
                if entry.file not in file:
                    self.append(entry)

    def append_view(self, view):
        self.clear_view(view)
        tmLanguage = view.settings().get('syntax').split('/')[1]
        rxs = view.settings().get('goto_symbol_regexp').get(tmLanguage)
        if rxs:
            for rx in rxs:
                for region in view.find_all(rx, sublime.IGNORECASE):
                    symbol = Symbol(view, region.a, region.b)
                    self.append(symbol)
                #self.sort()


class GotoSymbolListener(sublime_plugin.EventListener):
    def on_load(self, view):
        SYMBOL_LIST.append_view(view)

    def on_post_save(self, view):
        SYMBOL_LIST.append_view(view)

    def on_close(self, view):
        SYMBOL_LIST.clear_view(view)


class GotoSymbolCommand(sublime_plugin.TextCommand):

    def run(self, edit, action):
        method = getattr(self, action)
        if method:
            method()

    def list_all(self):
        self.symbols = SYMBOL_LIST
        symbols = [o.name for o in self.symbols]
        self.view.window().show_quick_panel(symbols, self.on_select_symbol)

    def list_carret_matches(self):
        region = self.view.sel()[-1]
        region = self.view.word(region)
        symbol = Symbol(self.view, region.a, region.b)
        self.symbols = SYMBOL_LIST.find(symbol)
        if not self.symbols:
            sublime.status_message(STATUS['empty_symbol'])
        elif len(self.symbols) == 1:
            self.on_select_symbol(0)
        else:
            symbols = [o.name for o in self.symbols]
            self.view.window().show_quick_panel(symbols, self.on_select_symbol)

    def on_select_symbol(self, index):
        if index >= 0:
            file = "%s:%d" % (self.symbols[index].file, self.symbols[index].line)
            if self.view.window():
                self.view.window().open_file(file, sublime.ENCODED_POSITION)


# Main ()
SYMBOL_LIST = SymbolList()
STATUS = {
    'empty_symbol': 'GotoSymbol: unfound matches'
}
