import os
import re
import logging
from operator import itemgetter
from itertools import imap, product, groupby
import plyplus, plyplus.grammars
from django.conf import settings
from dashboard.models import Environment, Role, Host

__all__ = ("InventoryLex", "InventoryYacc")

parser = plyplus.Grammar(
    plyplus.grammars.open(os.path.join(settings.BASE_DIR, 'dashboard', 'inventory', 'inventory.g')), debug=False)


def section_parse(text):
    text = text.strip("[]")
    env_name, group_name = text.split(":", 1)
    return env_name, group_name


RE_tuple = re.compile(r"\[([^\]]+)\]")
SIGN_EXCLUDE = "!"
SIGN_CONTINUE = ":"
NUMBER_FORMATTER = "{{:0{pad}d}}"


def _ranger(start, end, formatter):
    return imap(formatter.format, xrange(int(start), int(end) + 1))


def _parse_tuple_item(sub_text, pad=0):
    formatter = NUMBER_FORMATTER.format(pad=pad)
    for el in sub_text.split(","):
        if not el:
            continue
        if SIGN_CONTINUE in el:
            start, end = el.split(":", 1)
            for i in _ranger(start, end, formatter):
                yield i
        else:
            yield formatter.format(int(el))


def _host_tuple_item(text):
    """ 01:10!03:08 -> 01,02,04,09,10 """
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


def _tuple_format(first, last, formater):
    els = map(formater.format, (first, last))
    differ = last - first
    if differ < 1:
        return els[0]
    elif differ == 1:
        return ",".join(els)
    else:
        return ":".join(els)


def _cluster_tuple(items):
    """
    [u'01', u'02', u'03', u'04'] -> "[01:04]"
    [u'01', u'03', u'04'] -> "["01,02,03"]"
    [u'01', u'05', u'06', u'07', u'08', u'09', u'11'] -> "[01, 05:09, 11]"

    :type items: list
    :rtype : Generator
    """
    max_llen = max(map(len, items))
    items_int = sorted(map(int, items))
    mmax, mmin = items_int[0], items_int[-1]
    formater = NUMBER_FORMATTER.format(pad=max_llen)
    if mmax == mmin:
        yield formater.format(mmin)
        raise StopIteration

    # yield the discontinuous tuple
    i = start = prev = None
    for i in items_int:
        if prev is None:
            start = prev = i
            continue
        if i - prev > 1:
            yield _tuple_format(start, prev, formater)
            prev = start = i
            continue
        prev = i
    yield _tuple_format(start, prev, formater)
    raise StopIteration


def _cluster_one_pattern(data):
    assert len(data) > 0
    row_len = len(data[0])
    for n in xrange(row_len):
        items = map(itemgetter(n), data)
        items_formatted = list(_cluster_tuple(items))
        yield "[{0}]".format(",".join(items_formatted))
    raise StopIteration


RE_number_spliter = re.compile("([^0-9]+|\d+)")


def cluster_hostname(host_list):
    """
    [
        u'DB01.01domain', u'DB01.02domain', u'DB01.03domain',
        u'DB02.01domain', u'DB02.03domain', u'DB02.04domain',
        u'DB03.01domain', u'DB03.02domain', u'DB03.3domain',
        u'WEB01.domain', u'WEB02.domain', u'WEB03.domain'
    ]
    ->
   [
       "DB01:03.01:04domain",
       "WEB01:03.domain"
   ]

    :param host_list: Generator
    :rtype : Generator
    """
    patterns = []
    for hostname in host_list:
        tuples = RE_number_spliter.findall(hostname)
        data = []
        pattern = []
        for el in tuples:
            if el.isdigit():
                data.append(el)
                pattern.append(None)
            else:
                pattern.append(el)
        patterns.append((pattern, data))
    for pattern, els in groupby(patterns, key=itemgetter(0)):
        rows = map(itemgetter(1), els)
        c = _cluster_one_pattern(rows)
        yield "".join(i if i is not None else c.next() for i in pattern)
    raise StopIteration


def serialize():
    for env in Environment.objects.filter(is_enabled=True):
        hosts = env.hosts.filter(is_enabled=True).order_by("name")
        roles = Role.objects.filter(is_enabled=True, hosts__in=hosts).distinct()
        for role in roles:
            yield "[{0}:{1}]".format(env.name, role.name)
            yield "\n".join(cluster_hostname(i.name for i in hosts.filter(roles=role)))
            yield "\n"
    raise StopIteration


def deserialize(text):
    for token in parser.lex(text):
        if token.type == "NEWLINE":
            continue
        elif token.type == "SECTION":
            yield "SECTION", section_parse(token.value)
        elif token.type == "HOST":
            yield "HOST", host_parse(token.value)
    raise StopIteration


def store_from_parsed(entities):
    """
    Storing the entities
    also maintain the exists entities in the DB and disbale them (is_enabled=False)
    """
    opted_envs = set()
    opted_roles = set()
    opted_hosts = set()

    # Clean the role relationship
    Host.roles.through.objects.all().delete()

    for tp, args in entities:
        if tp == "SECTION":
            envname, groupname = args
            env, _ = Environment.objects.get_or_create(name=envname)
            opted_envs.add(env.name)
            role, _ = Role.objects.get_or_create(name=groupname)
            opted_roles.add(role.name)
        elif tp == "HOST":
            for hostname in args:
                host = Host.objects.filter(name=hostname).first()
                if host is None:
                    host = Host(name=hostname, env=env)
                host.env = env
                host.roles.add(role)
                host.is_enabled = True
                host.save()
                opted_hosts.add(host.name)

    Environment.objects.exclude(name__in=opted_envs).update(is_enabled=False)
    Role.objects.exclude(name__in=opted_roles).update(is_enabled=False)
    Host.objects.exclude(name__in=opted_hosts).update(is_enabled=False)

    Environment.objects.filter(name__in=opted_envs).update(is_enabled=True)
    Role.objects.filter(name__in=opted_roles).update(is_enabled=True)


def store(text):
    return store_from_parsed(deserialize(text))
