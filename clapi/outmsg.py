# -*- coding: utf-8 -*-

import zlib, base64, os, urllib

def getf(l):
    return urllib.urlopen(l).read()

def ff(lst,e):
    return set([int(x[:-len(e)]) for x in lst if x.endswith(e)])

def lsout():
    ls = os.listdir('out')
    tossl = ff(ls,'.toss')
    outl = ff(ls,'.out')
    top = max(outl) + 1 if outl else 1
    return tossl,outl,top

def mktoss(f,tx):
    open('out/%s.out' % f,'w').write(tx)
    ctx = base64.urlsafe_b64encode( zlib.compress(tx,9) )
    open('out/%s.toss' % f,'w').write(ctx)

def zpush(f,url,auth):
    txt = open('out/%s.toss' % f).read()
    out = getf('%sz/push/%s/%s' % (url, auth, txt))
    os.remove('out/%s.toss' % f)

def getout(f):
    return open('out/%s.out' % f).read()

def mkmsg(ea,subj,msgto,msg,repto):
    rp = '@repto:%s\n' % repto if repto else ''
    return ea + '\n' + msgto + '\n' + subj + '\n\n' + rp + msg.replace('\r\n','\n')

def om(ea,subj,msgto,msg,repto=''):
    tx = mkmsg(ea,subj,msgto,msg,repto).encode('utf-8')
    t,o,top = lsout()
    mktoss(top,tx)

def outmsgs():
    out = []
    tossl ,outl, top = lsout()
    for x in outl:
        out.append( (0 if x in tossl else 1,getout(x).decode('utf-8')) )
    return out

def pushall(url,authstr):
    t,o,top = lsout()
    for x in t:
        zpush(x,url,authstr)

#om('ii.2014','suubj!','All',u'Привет всем всем всем всееееееем!')
#om('ii.2014',u'suubjик!','All',u'Привет всем всем всем всееееееем!\nВсем всем!')

#zpush(1,'http://51t.ru/','_')

#print outmsgs()
