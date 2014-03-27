# -*- coding: utf-8 -*-

import clapi as api, clapi.sx as sx, clapi.flt as flt, clapi.getmsg as gm, clapi.outmsg as om
from clapi.bottle import *
echolist = []; url = ''; phash = '*'

def load_echo():
    global echolist, url, phash
    cfg = open('config.cfg').read().splitlines()
    url = cfg[1]; phash = cfg[0]
    echolist = [(x,api.echoarea_count(x)) for x in cfg[2:]]
load_echo()

def allstart():
    local.r = sx.mydict(fz=sx.mydict(request.forms),getl=sx.mydict(request.GET),echolist=echolist)

@route('/')
def dashboard():
    allstart()
    local.r.update(page_title='ii-client',ea='')
    return template('tpl/nedodash.html',r=local.r)

@route('/<echo>.<year:int>')
def index_list(echo,year):
    allstart()
    ea = '%s.%s' % (echo,year)
    if not flt.echo_flt(ea): return ea
    local.r.update(page_title = u'%s : ii-client' % ea,ea=ea,url=url)
    return template('tpl/start.html',r=local.r,j=api.get_echoarea(ea),ea=ea)

@route('/reply/<ea>/<repto>')
def index_list(ea,repto):
    allstart()
    if repto and repto != '-': 
        local.r.repto = repto
        local.r.rmsg = api.get_msg(repto)
    if not flt.echo_flt(ea): return ea
    local.r.page_title = u'message to ' + ea
    return template('tpl/form.html',r=local.r,ea=ea)

@route('/h/get')
def h_get():
    allstart()
    msgbuf = gm.fetch([x for x,y in echolist],url)
    load_echo(); local.r.echolist = echolist
    return template('tpl/newmsgs.html',msgbuf=msgbuf,r=local.r)

@route('/h/send')
def h_send():
    allstart()
    om.pushall(url,phash)
    return '<a href="/h/out"><h1>go back</h1></a>'


@route('/h/out')
def h_out():
    allstart()
    local.r.page_title=u'Исходящие сообщения'
    return template('tpl/outmsgs.html',outbuf = om.outmsgs(),r=local.r)

@post('/a/msg/<ea>')
def qmsg_post(ea):
    allstart()
    rq = request.forms
    if not flt.echo_flt(ea): return ea
    if not request.forms.msg or not request.forms.subj: return ''
    om.om(ea,rq.subj,'All',rq.msg,rq.repto)
    redirect ('/h/out')

@route('/s/<filename:path>')
def new_style(filename):
    return static_file(filename,root='./s')

#@route('/q/<msglst:path>')
#def msg_page(msglst):
#    return template('msg.html',lst=[api.get_msg(n) + {'msgid':n} for n in msglst.split('/')])

#webbrowser:

run(host='127.0.0.1',port=62222,debug=True)
