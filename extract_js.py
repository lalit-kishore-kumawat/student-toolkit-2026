import re

with open('predictor.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove const collegeData = [...]; block
html = re.sub(r'const collegeData = \[\s*\{.*?\n\];', '', html, flags=re.DOTALL)

# Add the script tag right before the existing inline script
target = '<script>'
replacement = '<script src="final_colleges.js"></script>\n  <script>'
if '<script src="final_colleges.js"></script>' not in html:
    html = html.replace(target, replacement, 1)

with open('predictor.html', 'w', encoding='utf-8') as f:
    f.write(html)
