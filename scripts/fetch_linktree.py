import urllib.request
import re
import json

url = 'https://linktr.ee/vanessarezendepianzola'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        with open('scratch_linktree.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('Saved scratch_linktree.html, length:', len(html))

        # Look for images and next/data
        urls = re.findall(r'https://[^\s"\'<>\\]+', html)
        for u in set(urls):
            if any(k in u.lower() for k in ['ugc', 'avatar', 'profile', 'd3fd5j', 'cloudfront', 'image']):
                print('Candidate image:', u)
except Exception as e:
    print('Failed:', e)
