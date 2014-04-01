# -*- coding: utf-8 -*-

from bottle import *
import base64, zlib, os

def _rf(f): 
    if os.path.exists(f): return open(f).read()
    else: return ''

def _2nl(s):
    out = ''
    for x in s: out += s + '\n'
    return out

def raw_msg(h):
    return _rf('msg/%s' % h)

def get_echoarea(name):
    return _rf('echo/%s' % name).splitlines()

def mk_jt(mh,mb):
    return mh + ':' + base64.urlsafe_b64encode( zlib.compress(mb) )

def qua(ea,s):
    items =  get_echoarea(ea)
    if len(s) < 6 and s.isdigit():
        return items[-int(s):]
    else:
        if not s in items: return items
        return items[items.index(s)+1:]

def parse_echos(echos):
    pool = []
    for ea in echos:
        if ':' in ea:
            items = qua(*ea.split(':',1))
        else:
            items = get_echoarea(ea)
        for x in items:
            if not x in pool:
                pool.append(x)
    return pool


@route('/z/m/<h:path>')
def jt_outmsg(h):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return _2nl( [mk_jt(x,raw_msg(x)) for x in h.split('/') if len(x)==20] )

@route('/z/e/<names:path>')
def index_list(names):
    response.set_header ('content-type','text/plain; charset=utf-8')
    out = ''
    for ea in names.split('/'):
        out += ea + '\n'
        ge = get_echoarea(ea)
        if ge: out += '\n'.join(ge) + '\n'
    return out

@route('/z/get/<echos:path>')
def jt_echo(echos):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return _2nl( [mk_jt(x,raw_msg(x)) for x in parse_echos(echos.split('/'))] )

@route('/m/<msg:re:[A-Za-z0-9]{20}>')
def get_msg(msg):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return raw_msg(msg)

@route('/e/<echoarea>')
def get_echolist(echoarea):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return '\n'.join(  get_echoarea(echoarea) )

run(host='127.0.0.1',port=62220,debug=False)
