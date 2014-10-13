import os
import re
import sys
import logging
from itertools import imap, product
import plyplus, plyplus.grammars
from django.conf import settings
from dashboard.models import Environment, Role, Host

__all__ = ("InventoryLex", "InventoryYacc")

parser = plyplus.Grammar(plyplus.grammars.open(os.path.join(settings.BASE_DIR, 'dashboard', 'inventory', 'inventory.g')), debug=False)

def section_parse(text):
    text = text.strip("[]")
    envname, groupname = text.split(":", 1)
    return envname, groupname

RE_tuple = re.compile(r"\[([^\]]+)\]")
SIGN_EXCLUDE = "!"
SIGN_CONTINUE = ":"
def _ranger(start, end, formater):
    return imap(formater.format, xrange(int(start), int(end)+1))

def _parse_tuple_item(sub_text, pad=0):
    number_formater = "{{:0{pad}d}}".format(pad=pad)
    for el in sub_text.split(","):
        if not el:
            continue
        if SIGN_CONTINUE in el:
            start, end = el.split(":", 1)
            for i in _ranger(start, end, number_formater):
                yield i
        else:
            yield number_formater.format(int(el))

def _host_tuple_item(text):
    if SIGN_EXCLUDE in text:
        include, exclude = text.split("!", 1)
    else:
        include, exclude = text, ""

    def find_max_pad(text):
        el_list = text.split(",")
        len_list = imap(
            lambda x: max(map(len, x.split(":", 1))) if SIGN_CONTINUE in x else
            len(x), el_list
        )
        return max(len_list)
    pad = max(find_max_pad(include), find_max_pad(exclude))
    exclude_list = set(_parse_tuple_item(exclude, pad))
    for i in _parse_tuple_item(include, pad):
        if i not in exclude_list:
            yield i

def host_parse(text):
    """ Host entity parser
    """
    last_pos = 0
    parts = []
    for matcher in RE_tuple.finditer(text):
        parts.append((text[last_pos:matcher.start()], ))
        parts.append(_host_tuple_item(matcher.group(1)))
        last_pos = matcher.end()
    if last_pos < len(text):
        parts.append((text[last_pos:],))
    return list(imap(lambda x: "".join(x), (product(*parts))))

def serialize(envs):
    pass

def deserialize(text):
    for token in parser.lex(text):
        if token.type == "NEWLINE":
            continue
        elif token.type == "SECTION":
            yield "SECTION", section_parse(token.value)
        elif token.type == "HOST":
            yield "HOST", host_parse(token.value)

def store(entities):
    for tp, args in entities:
        if tp == "SECTION":
            envname, groupname = args
            env, _ = Environment.objects.get_or_create(name=envname)
            role, _ = Role.objects.get_or_create(name=groupname, env__name=env)
