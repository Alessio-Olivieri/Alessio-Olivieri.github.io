"""Build static Italian pages and paired language links; stdlib only.

Edit the English HTML and locales/it.json, then run python3 tools/build_translations.py.
English remains the default. Choosing Italian follows matching /it/ pages without
browser-language detection, cookies, storage or JavaScript redirects.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit, urlunsplit
import json,re,posixpath

ROOT=Path(__file__).resolve().parents[1]
BASE='https://alessio-olivieri.github.io'
TRANSLATIONS=json.loads((ROOT/'locales/it.json').read_text())
PAGES=[Path('index.html'),Path('projects.html'),*sorted(p.relative_to(ROOT) for p in (ROOT/'projects').glob('*.html'))]
PAGE_SET={str(p) for p in PAGES}
missing=set()
def translate(value):
 core=value.strip()
 if not core:return value
 if core.startswith('Open figure at full size: '):
  result='Apri la figura a dimensione intera: '+translate(core[len('Open figure at full size: '):])
 else:result=TRANSLATIONS.get(core,core)
 return value[:len(value)-len(value.lstrip())]+result+value[len(value.rstrip()):]
def url(page,lang):
 route='' if str(page)=='index.html' else str(page)
 return BASE+('/it/' if lang=='it' else '/')+route

def controls(page,lang):
 label='Lingua' if lang=='it' else 'Language'
 return '<span class="language-switch" role="group" aria-label="'+label+'">'+''.join(
  '<a href="'+url(page,code).replace(BASE,'')+'" lang="'+code+'" hreflang="'+code+'" aria-label="'+name+'" title="'+name+'"'+(' aria-current="true"' if code==lang else '')+'>'+code.upper()+'</a>' for code,name in [('en','English'),('it','Italiano')])+'</span>'
def prepare(s,page,lang):
 s=re.sub(r'<span class="language-switch".*?</span>','',s,flags=re.S)
 s=re.sub(r'<link rel="alternate"[^>]*>\s*','',s)
 # Insert only in the primary navigation, never in section or breadcrumb menus.
 s=re.sub(r'(<nav class="navlinks".*?)(</nav>)',lambda m:m[1]+controls(page,lang)+m[2],s,count=1,flags=re.S)
 alternates='\n'.join('<link rel="alternate" hreflang="'+code+'" href="'+url(page,'en' if code=='x-default' else code)+'">' for code in ['en','it','x-default'])
 return s.replace('</head>',alternates+'\n</head>')

class Italian(HTMLParser):
 def __init__(self,page):super().__init__(convert_charrefs=True);self.page=page;self.output=[]
 def link(self,value):
  u=urlsplit(value)
  if u.scheme or u.netloc or not u.path or u.path.startswith('/'):return value
  target=posixpath.normpath(posixpath.join(str(self.page.parent),u.path))
  if target in PAGE_SET:target='it/'+target
  elif target.startswith('assets/projects/') and target.endswith('.svg'):
   target=target[:-4]+'.it.svg'
  return urlunsplit(('', '', '/'+target,u.query,u.fragment))
 def handle_decl(self,d):self.output.append('<!'+d+'>')
 def handle_comment(self,d):self.output.append('<!--'+d+'-->')
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':a['lang']='it'
  for key in ['alt','aria-label','title']:
   if key in a:a[key]=translate(a[key])
  if tag=='meta':
   if a.get('name')=='description' or a.get('property') in ['og:title','og:description']:a['content']=translate(a['content'])
   if a.get('property')=='og:url':a['content']=url(self.page,'it')
  if tag=='link' and a.get('rel')=='canonical':a['href']=url(self.page,'it')
  for key in ['href','src']:
   if key in a:a[key]=self.link(a[key])
  self.output.append('<'+tag+''.join(' '+key+('="'+escape(value,quote=True)+'"' if value is not None else '') for key,value in a.items())+'>')
 def handle_endtag(self,t):self.output.append('</'+t+'>')
 def handle_data(self,d):self.output.append(escape(translate(d),quote=False))
 def handle_startendtag(self,t,a):self.handle_starttag(t,a)

for page in PAGES:
 p=ROOT/page;s=p.read_text()
 english=prepare(s,page,'en');p.write_text(english)
 # Remove language controls before translating; add the explicit Italian pair after.
 clean=re.sub(r'<span class="language-switch".*?</span>','',english,flags=re.S)
 parser=Italian(page);parser.feed(clean)
 translated=prepare(''.join(parser.output),page,'it')
 dest=ROOT/'it'/page;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(translated)
print(f'Built {len(PAGES)} Italian pages and updated English language links.')

# Preserve the original presentation images; localize the purpose-built diagram.
from html import unescape
chart_translations=json.loads((ROOT/'locales/charts.it.json').read_text())
svg=(ROOT/'assets/projects/gear-integration.svg').read_text()
def svg_text(match):
 text=unescape(match.group(1))
 return '>'+escape(chart_translations.get(text,text),quote=False)+'<'
svg=re.sub(r'>([^<>]+)<',svg_text,svg)
(ROOT/'assets/projects/gear-integration.it.svg').write_text(svg)
