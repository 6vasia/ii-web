# -*- coding: utf-8 -*-

import zlib, base64, os, urllib, clapi

def postf(url,pauth,s):
    data = urllib.urlencode({'tmsg': s,'pauth': pauth})
    u = urllib.urlopen(url + 'point', data)
    return u.read()


def ff(lst,e):
    return set([int(x[:-len(e)]) for x in lst if x.endswith(e)])

def lsout():
    ls = os.listdir('out')
    tossl = ff(ls,'.toss')
    outl = ff(ls,'.out')
    top = max(outl) + 1 if outl else 1
    return tossl,outl,top

def mktoss(f,tx,us):
    open('out/%s.out' % f,'w').write(tx)
    ctx = clapi.b64c(tx)
    open('out/%s.toss' % f,'w').write(ctx)

def zpush(f,url,pauth):
    txt = open('out/%s.toss' % f).read()
    out = postf(url,pauth,txt)
    if out.startswith('msg ok'):
        os.remove('out/%s.toss' % f)
    else:
        return out

def getout(f):
    return open('out/%s.out' % f).read()

def mkmsg(ea,subj,msgto,msg,repto):
    rp = '@repto:%s\n' % repto if repto else ''
    return ea + '\n' + msgto + '\n' + subj + '\n\n' + rp + msg.replace('\r\n','\n')

def om(ea,subj,msgto,msg,repto='',us=True):
    tx = mkmsg(ea,subj,msgto,msg,repto).encode('utf-8')
    t,o,top = lsout()
    mktoss(top,tx,us)

def outmsgs():
    out = []
    tossl ,outl, top = lsout()
    for x in outl:
        out.append( (0 if x in tossl else 1,getout(x).decode('utf-8')) )
    return out

def pushall(url,pauth):
    t,o,top = lsout()
    for x in t:
        debugmsg = zpush(x,url,pauth)
        if debugmsg: return debugmsg
