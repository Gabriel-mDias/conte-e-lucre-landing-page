import json
import re

found_urls = set()
with open(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        urls = re.findall(r'https?://[^\s"\'<>\\]+', line)
        for u in urls:
            if any(k in u for k in ['scontent', 'linktree', 'ugc', 'cdninstagram', 'wa.me']):
                found_urls.add(u)

for u in sorted(found_urls):
    print(u)
