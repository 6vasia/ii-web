# -*- coding: utf-8 -*-

import time, bottle, re

class mydict(dict):
    def __getattr__(self, key):
        return self.get(key,'')
    def __setattr__(self, key, value):
        self[key] = value
    def __add__(self, data):
        return mydict(self.items() + data.items())
    def __sub__(self, key):
        return mydict((k,v) for (k,v) in self.items() if k != key)


def datef(d,f):
    return time.strftime(f, time.localtime(int(d)))

def dateg(d,f):
    return time.strftime(f, time.gmtime(int(d)))

def ts_get(d,f=None):
    return time.strptime(d, f or '%d.%m.%Y %H:%M')

def gts():
    return int(time.time())

def rend(txt):
    out = bottle.html_escape(txt)
    r1 = re.compile(r"(\b(http|https)://([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))")
    out = r1.sub(r'<a href="\1">\1</a>',out)
    r2 = re.compile(r"(\b(ii)://([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))")
    out = r2.sub(r'<strong><a href="\3">\3</a></strong>',out)
    return out.replace('\n', '<br />')
