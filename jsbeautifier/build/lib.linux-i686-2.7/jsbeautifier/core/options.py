# The MIT License (MIT)
#
# Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy
import re
from collections import namedtuple

class Options:
    def __init__(self, options=None, merge_child_field=None):
        self.css = None
        self.js = None
        self.html = None

        options = _mergeOpts(options, merge_child_field)
        self.raw_options = _normalizeOpts(options)

        # Support passing the source text back with no change
        self.disabled = self._get_boolean('disabled')

        self.eol = self._get_characters('eol', 'auto')
        self.end_with_newline = self._get_boolean('end_with_newline')
        self.indent_size = self._get_number('indent_size', 4)
        self.indent_char = self._get_characters('indent_char', ' ')
        self.indent_level = self._get_number('indent_level')

        self.preserve_newlines = self._get_boolean('preserve_newlines', True)
        # TODO: fix difference in js and python
        self.max_preserve_newlines = self.max_preserve_newlines = self._get_number('max_preserve_newlines', 10)
        if not self.preserve_newlines:
            self.max_preserve_newlines = 0

        self.indent_with_tabs = self._get_boolean('indent_with_tabs')
        if self.indent_with_tabs:
            self.indent_char = '\t'
            self.indent_size = 1

        # Backwards compat with 1.3.x
        self.wrap_line_length = self._get_number('wrap_line_length', self._get_number('max_char'))

    def _get_array(self, name, default_value=[]):
        option_value = getattr(self.raw_options, name, default_value)
        result = []
        if isinstance(option_value, list):
            result = copy.copy(option_value)
        elif isinstance(option_value, str):
            result = re.compile(r"[^a-zA-Z0-9_/\-]+").split(option_value)

        return result

    def _get_boolean(self, name, default_value=False):
        option_value = getattr(self.raw_options, name, default_value)
        result = False
        try:
            result = bool(option_value)
        except ValueError:
            pass

        return result

    def _get_characters(self, name, default_value=''):
        option_value = getattr(self.raw_options, name, default_value)
        result = ''
        if isinstance(option_value, str):
            result = option_value.replace('\\r', '\r').replace('\\n', '\n').replace('\\t', '\t')

        return result

    def _get_number(self, name, default_value=0):
        option_value = getattr(self.raw_options, name, default_value)
        result = 0
        try:
            result = int(option_value)
        except ValueError:
            pass

        return result

    def _get_selection(self, name, selection_list, default_value=None):
        result = self._get_selection_list(name, selection_list, default_value)
        if len(result) != 1:
            raise ValueError(
                "Invalid Option Value: The option '" + name + "' can only be one of the following values:\n" +
                str(selection_list) +
                "\nYou passed in: '" +
                str(getattr(self.raw_options, name, None)) +
                "'")

        return result[0]


    def _get_selection_list(self, name, selection_list, default_value=None):
        if not selection_list:
            raise ValueError("Selection list cannot be empty.")

        default_value = default_value or [selection_list[0]]

        if not self._is_valid_selection(default_value, selection_list):
            raise ValueError("Invalid Default Value!")

        result = self._get_array(name, default_value)
        if not self._is_valid_selection(result, selection_list):
            raise ValueError(
                "Invalid Option Value: The option '" + name + "' can contain only the following values:\n" +
                str(selection_list) +
                "\nYou passed in: '" +
                str(getattr(self.raw_options, name, None)) +
                "'")

        return result

    def _is_valid_selection(self, result, selection_list):
        if len(result) == 0 or len(selection_list) == 0:
            return False

        for item in result:
            if item not in selection_list:
                return False

        return True


# merges child options up with the parent options object
# Example: obj = {a: 1, b: {a: 2}}
#          mergeOpts(obj, 'b')
#
#          Returns: {a: 2, b: {a: 2}}


def _mergeOpts(options, childFieldName):
    if options is None:
        options = {}

    if isinstance(options, tuple):
        options = dict(options)

    if isinstance(options, dict):
        options = _normalizeOpts(options)
        options = namedtuple("CustomOptions", options.keys())(*options.values())

    finalOpts = copy.copy(options)

    local = getattr(finalOpts, childFieldName, None)
    if local:
        delattr(finalOpts, childFieldName)
        for key in local:
            setattr(finalOpts, key, local[key])

    return finalOpts

def _normalizeOpts(options):
    convertedOpts = copy.copy(options)
    if isinstance(convertedOpts, dict):
        option_keys = list(convertedOpts.keys())
        for key in option_keys:
            if '-' in key:
                del convertedOpts[key]
                convertedOpts[key.replace('-', '_')] = options[key]
    else:
        option_keys = list(getattr(convertedOpts, '__dict__', {}))
        for key in option_keys:
            if '-' in key:
                delattr(convertedOpts, key)
                setattr(convertedOpts, key.replace('-', '_'), getattr(options, key, None))

    return convertedOpts
