# Copyright (c) 2013 Alexander Schrijver <alex@flupzor.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from django.core import exceptions

from importlib import import_module

from django.conf import settings

# XXX: Code copied from: ./django/core/handlers/base.py

def load_parser(parser_path):
    # Load the parser class.
    try:
        parser_module, parser_classname = parser_path.rsplit('.', 1)
    except ValueError:
        raise exceptions.ImproperlyConfigured('%s isn\'t a parser module' % middleware_path)
    try:
        mod = import_module(parser_module)
    except ImportError as e:
        raise exceptions.ImproperlyConfigured('Error importing parser %s: "%s"' % (parser_module, e))
    try:
        parser_class = getattr(mod, parser_classname)
    except AttributeError:
        raise exceptions.ImproperlyConfigured('Parser module "%s" does not define a "%s" class' % (parser_module, parser_classname))

    return parser_class

def parser_by_path(path):
    if path in settings.NIEUWSVERSCHILLEN_PARSERS:
        return load_parser(path)

    return None
