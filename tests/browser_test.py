"""Isolated, nonpersistent browser only. Start local http.server first."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('/workspace/product-dev-research/site-test');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1000})
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8765/',wait_until='networkidle')
 assert page.locator('.case:visible').count()==9
 page.screenshot(path=str(out/'desktop.png'),full_page=True)
 page.locator('#search').fill('Mole');assert page.locator('.case:visible').count()==1
 page.locator('.case:visible summary').click();assert page.locator('.case:visible details').get_attribute('open') is not None
 page.locator('#search').fill('not-a-match-xyz');assert page.locator('#empty').is_visible()
 page.locator('#reset').click();assert page.locator('.case:visible').count()==9
 page.locator('#topic').select_option(label='工程验证');assert page.locator('.case:visible').count()==2
 page.locator('#author').select_option(label='@gefei55');assert page.locator('.case:visible').count()==0
 page.locator('#reset').click();page.locator('#stage').select_option(label='首次付费后 / 获客');assert page.locator('.case:visible').count()==1
 with page.expect_download() as d:page.locator('#export').click()
 data=json.load(open(d.value.path()));assert len(data['items'])==1
 page.locator('[data-task="0"]').check();page.reload();assert page.locator('[data-task="0"]').is_checked();assert '1 / 8' in page.locator('#progress').inner_text()
 for width in [360,390,768,1440]:
  page.set_viewport_size({'width':width,'height':900});page.goto('http://127.0.0.1:8765/');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  if width==390:page.screenshot(path=str(out/'mobile.png'),full_page=True)
 assert not errors,errors
 context.close();browser.close()
print('PASS: search, combined filters, reset, empty state, details, export, persisted checklist; no console errors; no overflow at 360/390/768/1440px')
