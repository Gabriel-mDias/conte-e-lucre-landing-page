import re
import json

with open(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\.system_generated\steps\28\content.md', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search for bio links
bio_links = re.findall(r'https?://[^\s"\'<>]+(?:linktr\.ee|wa\.me|api\.whatsapp|bit\.ly|forms|drive)[^\s"\'<>]*', text)
print('Bio links:', set(bio_links))

ext_urls = re.findall(r'"external_url"\s*:\s*"([^"]+)"', text)
print('External URLs:', ext_urls)

bios = re.findall(r'"biography"\s*:\s*"([^"]+)"', text)
print('Biography:', bios)

full_names = re.findall(r'"full_name"\s*:\s*"([^"]+)"', text)
print('Full names:', set(full_names))

profile_pic = re.findall(r'"profile_pic_url_hd"\s*:\s*"([^"]+)"', text)
if not profile_pic:
    profile_pic = re.findall(r'"profile_pic_url"\s*:\s*"([^"]+)"', text)
print('Profile pic:', profile_pic)

# Look for posts / edge_owner_to_timeline_media or similar
posts_data = re.findall(r'"node"\s*:\s*(\{[^{}]*"display_url"[^{}]*\})', text)
print(f'Found {len(posts_data)} posts nodes')

all_jpgs = list(set(re.findall(r'https://[^"\'\s<>\\]+cdninstagram\.com/[^"\'\s<>\\]+\.jpg[^"\'\s<>\\]*', text)))
print(f'Found {len(all_jpgs)} cdninstagram jpg links')
for j in all_jpgs[:10]:
    print('JPG:', j.replace('\\u0026', '&'))

all_mp4s = list(set(re.findall(r'https://[^"\'\s<>\\]+cdninstagram\.com/[^"\'\s<>\\]+\.mp4[^"\'\s<>\\]*', text)))
print(f'Found {len(all_mp4s)} cdninstagram mp4 links')

# Search for any post text/captions
captions = re.findall(r'"caption"\s*:\s*\{"text"\s*:\s*"([^"]+)"\}', text)
if not captions:
    captions = re.findall(r'"text"\s*:\s*"([^"]{30,400})"', text)
print(f'Found {len(captions)} caption candidates:')
for c in captions[:10]:
    print('-', c.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore')[:120])
