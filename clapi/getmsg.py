# -*- coding: utf-8 -*-

import urllib

def getf(l):
    print 'fetch %s' % l
    return urllib.urlopen(l).read()

def get_echoarea(name):
    try:
        return open('echo/%s' % name).read().splitlines()
    except:
        return ''

def filter_urls(my,out,url):
    nmy = my[:]
    nmbuf = []
    for n in out:
        if not n in my:
            out = getf('%sm/%s' % (url, n))
            if out and not '<' in out:
                open('msg/%s' % n,'w').write(out)
                nmy.append(n)
                nmbuf.append ( (n,out) )
    return nmy, nmbuf


def fetch(el,url):
    newmsgs = []
    for ea in el:
        my = get_echoarea(ea) or []
        out = getf('%se/%s' % (url, ea))
        if not '<' in out:
            nmy, nmbuf = filter_urls(my,out.splitlines(),url)
            newmsgs += nmbuf
            buf = '\n'.join(nmy)
            open('echo/%s' % ea, 'w').write(buf)
    return newmsgs
