import json
import re

with open('final_colleges.js', 'r') as f:
    js_data = f.read().strip()

# Let's fix tiers correctly
match = re.search(r'const collegeData = (\[.*?\]);', js_data, re.DOTALL)
if match:
    colleges = json.loads(match.group(1))
    tier_map = {}
    for c in colleges:
        if c['branch'] == 'CSE' and c['cutoff'] > 0:
            if c['name'] not in tier_map:
                tier_map[c['name']] = c['cutoff']
            else:
                tier_map[c['name']] = min(tier_map[c['name']], c['cutoff'])
    
    for c in colleges:
        cse_rank = tier_map.get(c['name'], 999999)
        if cse_rank < 5000:
            c['tier'] = 1
            c['tierLabel'] = "🏆 Tier 1"
        elif cse_rank < 15000:
            c['tier'] = 2
            c['tierLabel'] = "⭐ Tier 2"
        elif cse_rank < 30000:
            c['tier'] = 3
            c['tierLabel'] = "✅ Tier 3"
        elif cse_rank < 60000:
            c['tier'] = 4
            c['tierLabel'] = "📌 Tier 4"
        else:
            c['tier'] = 5
            c['tierLabel'] = "📍 Tier 5"
    
    new_js_data = 'const collegeData = [\n'
    for i, c in enumerate(colleges):
        new_js_data += f'  {json.dumps(c)}'
        if i < len(colleges) - 1:
            new_js_data += ',\n'
        else:
            new_js_data += '\n'
    new_js_data += '];'
    
    with open('final_colleges.js', 'w', encoding='utf-8') as f:
        f.write(new_js_data)
        
    # Re-inject into predictor.html
    with open('predictor.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace Data block
    start_idx = html.find('const collegeData = [')
    end_idx = html.find('const bookmarks = new Set();')
    
    if start_idx != -1 and end_idx != -1:
        html = html[:start_idx] + new_js_data + "\n\n    /* Track bookmarks (UI only, session state) */\n    " + html[end_idx:]
        with open('predictor.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated predictor.html size: {len(html)}")
    
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()
# Force write to touch file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print(f"Updated index.html size: {len(idx)}")
