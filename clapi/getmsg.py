# -*- coding: utf-8 -*-

import urllib2, base64, zlib, clapi

cfg = open('config.cfg').read().splitlines()

def getf(l):
    print 'fetch %s' % l
    from StringIO import StringIO
    import gzip
    request = urllib2.Request(l)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        f = gzip.GzipFile(fileobj=StringIO( response.read()))
    else:
        f = response
    return f.read()

def get_echoarea(name):
    try: return open('echo/%s' % name).read().splitlines()
    except: return []

def sep(l,step=20):
    for x in range(0,len(l),step):
        yield l[x:x+step]

def unp(s):
    return clapi.b64d(s)

def debundle(ea,s):
    for n in s.splitlines():
        mid,kod = n.split(':',1)
        open('msg/%s' % mid,'w').write(unp(kod))
        open('echo/%s' % ea, 'a').write(mid + '\n')
        open('.newmsg','a').write(mid + '\n') # for newmsg

def walk_el(out):
    ea = ''; el = {}
    for n in out.splitlines():
        if '.' in n:
            ea = n
            el[ea] = []
        elif ea:
            el[ea].append(n)
    return el

def fetch(el,url):
    out = getf('%se/%s' % (url, '/'.join(el)))
    el = walk_el(out)
    for ea in cfg[2:]:
        myel = set(get_echoarea(ea))
        dllist = [x for x in el[ea] if x not in myel]
        for dl in sep(dllist,40):
            s = getf('%sm/%s' % (cfg[1], '/'.join(dl)))
            debundle(ea,s)
