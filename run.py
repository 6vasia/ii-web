# -*- coding: utf-8 -*-

import clapi as api, clapi.sx as sx, clapi.flt as flt, clapi.getmsg as gm, clapi.outmsg as om
from clapi.bottle import *
echolist = []; url = ''; phash = '*'

II_PATH=os.path.dirname(__file__) or '.'
TEMPLATE_PATH.insert(0,II_PATH)

def load_echo():
    global echolist, url, phash
    cfg = open('config.cfg').read().splitlines()
    url = cfg[1]; phash = cfg[0]
    echolist = [(x,api.echoarea_count(x)) for x in cfg[2:]]
load_echo()

def newmsg_tags():
    try: return set(open('.newmsg').read().splitlines())
    except: return set()

def allstart():
    local.r = sx.mydict(fz=sx.mydict(request.forms),getl=sx.mydict(request.GET),echolist=echolist,newmsgs=newmsg_tags(),phash=phash)

def _msg(o,ml,mytitle=''):
    allstart()
    if o == 'msg':
        mo = api.get_msg(ml) + {'msgid':ml}
        local.r.page_title =  mo.subj + ' @ ' + mo.echoarea
        lst = [mo]
    elif o == 'lst' or o == 'lstall':
        lst=[api.get_msg(n) + {'msgid':n} for n in ml]
        local.r.page_title = mytitle or u'Список сообщений'
    return template('tpl/msg.html',lst=[mo] if o not in ('lst','lstall') else lst,r=local.r,mytitle=mytitle,lim=o)

@route('/')
def start_page():
    allstart()
    lst=[(e,api.get_echoarea(e)) for e,c in echolist]
    local.r.page_title = u'51t.ru : клуб хороших людей'
    return template('tpl/index.html',r=local.r,lst=lst)

@route('/reply/<ea>/<repto>')
def index_list(ea,repto):
    allstart()
    if repto and repto != '-': 
        local.r.repto = repto
        local.r.rmsg = api.get_msg(repto)
    if not flt.echo_flt(ea): return ea
    local.r.page_title = u'message to ' + ea
    return template('tpl/mform.html',r=local.r,ea=ea)

@route('/<echo>.<year:int>')
def index_list(echo,year):
    allstart()
    ea = '%s.%s' % (echo,year)
    if not flt.echo_flt(ea): return ea
    local.r.update(page_title=ea,echolist=echolist,ea=ea,url=url)
    return template('tpl/echoarea.html',r=local.r,j=api.get_echoarea(ea))

@route('/h/get')
def h_get():
    allstart()
    if request.query.a:
        newmsgs = open('.newmsg').read().splitlines()
        mpage = 'lstall'
    else:
        open('.newmsg','w').write('')
        gm.fetch([x for x,y in echolist],url)
        load_echo(); local.r.echolist = echolist
        newmsgs = open('.newmsg').read().splitlines()
        mpage = 'lst'
        newmsgs = newmsgs[-100:]
    return _msg(mpage, newmsgs,u'[%s] Новые сообщения' % len(newmsgs))

@route('/h/<act:re:send|out>')
def h_out(act):
    allstart()
    if act=='send': local.r.debugmsg = om.pushall(url,phash)
    local.r.page_title=u'Исходящие сообщения'
    return template('tpl/outmsgs.html',outbuf = om.outmsgs(),r=local.r)

@post('/a/msg/<ea>')
def qmsg_post(ea):
    allstart()
    rq = request.forms
    if not flt.echo_flt(ea): return ea
    if not request.forms.msg or not request.forms.subj: return ''
    us = False if url.endswith('/z/') else True
    om.om(ea,rq.subj,rq.msgto,rq.msg,rq.repto,us)
    redirect ('/h/out')

@route('/h/set')
def h_set():
    return 'У вас нет строки доступа. Вы не можете отправлять сообщения. О деталях подключения к 51t.ru смотрите на <a href="http://51t.ru">51t.ru</a>. Для других сетей - смотрите их официальные сайты.'

@route('/s/<filename:path>')
def new_style(filename):
    return static_file(filename,root='%s/s' % II_PATH)

@route('/q/<msglst:path>')
def msg_qpage(msglst):
    return _msg('lst',msglst.split('/'))

@route('/<msghash:re:[^/]{20}>')
def msg_page(msghash):
    return _msg('msg', msghash)

run(host='127.0.0.1',port=62222,debug=True)
