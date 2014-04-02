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
    return mh + ':' + base64.b64encode( mb.replace('-','+').replace('_','/') )

@route('/u/m/<h:path>')
def jt_outmsg(h):
    response.set_header ('content-type','text/plain; charset=iso-8859-1')
    return _2nl( [mk_jt(x,raw_msg(x)) for x in h.split('/') if len(x)==20] )

@route('/u/e/<names:path>')
def index_list(names):
    response.set_header ('content-type','text/plain; charset=iso-8859-1')
    out = ''
    for ea in names.split('/'):
        out += ea + '\n'
        ge = get_echoarea(ea)
        if ge: out += '\n'.join(ge) + '\n'
    return out


@route('/m/<msg:re:[A-Za-z0-9]{20}>')
def get_msg(msg):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return raw_msg(msg)

@route('/e/<echoarea>')
def get_echolist(echoarea):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return '\n'.join(  get_echoarea(echoarea) )

run(host='127.0.0.1',port=62220,debug=False)
