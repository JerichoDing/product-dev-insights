import json,unittest
from pathlib import Path
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.hrefs=[];self.assets=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if 'href' in a:self.hrefs.append(a['href'])
  if tag in ('script','img') and 'src'in a:self.assets.append(a['src'])
class Tests(unittest.TestCase):
 def setUp(self):self.p=Parser();self.p.feed((R/'index.html').read_text())
 def test_unique_ids(self):self.assertEqual(len(self.p.ids),len(set(self.p.ids)))
 def test_local_targets(self):
  for h in self.p.hrefs+self.p.assets:
   if h.startswith('#') and len(h)>1:self.assertIn(h[1:],self.p.ids)
   elif not h.startswith(('https://','#')):self.assertTrue((R/h).is_file(),h)
 def test_sourcing(self):
  r=json.loads((R/'data/research.json').read_text());self.assertEqual(12,len(r["selected"]));self.assertEqual(10,len({x["author"] for x in r['selected']}))
  for x in r['selected']:self.assertNotIn('original_text',x);self.assertTrue(x['limits']);self.assertIn(x['url'],self.p.hrefs)
 def test_no_remote_assets(self):self.assertFalse(any(x.startswith('http') for x in self.p.assets))
 def test_no_long_reposts(self):self.assertNotIn('original_text',(R/'data/research.json').read_text())
