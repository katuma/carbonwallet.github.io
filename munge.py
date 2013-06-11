#!/usr/bin/python
# not using regex here is intentional for clear readability
from sys import stdout
import re
import base64

out = open("index.html", "w")
for l in open('index.src.html'):
    if 'script src=' in l or 'rel="stylesheet"' in l:
        fpath = l.split('"')[1]
        if fpath.endswith('.js'):
            out.write("<script>\n// inlined from %s\n%s\n// end of inline from %s\n</script>\n" % (fpath, open(fpath).read(), fpath))
        elif fpath.endswith('.css'):
            data = open(fpath).read()
            def convert_url(x):
              f = x.group(1).split("?")[0].replace("'","")
              ext = f.split('.')[-1]
              fmt = 'image/'
              if ext not in ('png','jpg','gif'):
                fmt = 'application/x-font-'
              res = base64.b64encode(open("css/"+f,"rb").read()).decode('ascii')
              return "url(data:%s%s;base64,%s)"%(fmt,ext,res)
            data = re.sub(r"url\('([^']*)'\)", convert_url, data)
#            print(data)
#            lambda x: 'data:image/%s;base64,%s'%(x[-4:-1], base64.b64encode(open("css/"+x.replace("'","")).read())), data)
            out.write("<style>\n/* inlined from %s */\n%s\n/* end of inline from %s */\n</style>\n" % (fpath, data, fpath))
        else:
            print("unknown file " + fpath)
            exit(1)
    else:
        out.write(l)
