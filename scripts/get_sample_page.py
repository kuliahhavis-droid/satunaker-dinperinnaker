import urllib.request
import ssl
import re
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://dinperinnaker.purbalinggakab.go.id/sample-page/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

# Find entry-content
idx_start = html.find('entry-content')
idx_end = html.find('</div><!-- .entry-content -->')
content = html[idx_start:idx_end]

img_urls = re.findall(r'src="([^"]+)"', content)
print("Found images:", len(img_urls))
for i, url in enumerate(img_urls):
    print(f"Image {i+1}: {url}")
    # Download images to inspect
    fn = f"sample_page_img_{i+1}.png"
    urllib.request.urlretrieve(url, fn)
    print(f"Saved to {fn}")
