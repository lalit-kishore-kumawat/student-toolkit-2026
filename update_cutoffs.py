import re

with open('final_colleges.js', 'r') as f:
    js_data = f.read().strip()

with open('cutoffs.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Branch Filter
branch_html_target = """<option value="ALL">All Branches</option>
                    <option value="CSE">CSE</option>
                    <option value="AIML">AI/ML</option>
                    <option value="ISE">ISE</option>
                    <option value="DS">Data Science</option>
                    <option value="ECE">ECE</option>
                    <option value="EEE">EEE</option>"""

branch_html_replacement = """<option value="ALL">All Branches</option>
                    <option value="CSE">Computer Science (CSE)</option>
                    <option value="AIML">AI & Machine Learning (AIML)</option>
                    <option value="ISE">Information Science (ISE)</option>
                    <option value="DS">Data Science (DS)</option>
                    <option value="ECE">Electronics & Communication (ECE)</option>
                    <option value="EEE">Electrical & Electronics (EEE)</option>
                    <option value="ME">Mechanical Engineering (ME)</option>
                    <option value="CV">Civil Engineering (CV)</option>
                    <option value="Chemical">Chemical Engineering</option>
                    <option value="Biotech">Biotechnology</option>"""
html = html.replace(branch_html_target, branch_html_replacement)

# Update Category Filter
cat_html_target = """<select id="categoryFilter" class="filter-select" onchange="filterData()">
                    <option value="GM">General (GM)</option>
                    <option value="2AG">Category 2A</option>
                    <option value="SCG">SC Category</option>
                </select>"""
cat_html_replacement = """<select id="categoryFilter" class="filter-select" onchange="filterData()">
                    <option value="GM">GM</option>
                    <option value="2A">2A</option>
                    <option value="2B">2B</option>
                    <option value="3A">3A</option>
                    <option value="3B">3B</option>
                    <option value="SC">SC</option>
                    <option value="ST">ST</option>
                </select>"""
html = html.replace(cat_html_target, cat_html_replacement)


# Replace Data block
new_data_code = js_data.replace('const collegeData', 'const cutoffDatabase') + "\\n"

start_idx = html.find('const cutoffDatabase = [')
end_idx = html.find('const categoryMap = {')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_data_code + "\\n        " + html[end_idx:]
else:
    print("Could not find cutoffDatabase pattern!")

# Replace categoryMap
cat_map_target = """const categoryMap = {
            'GM': 'gm',
            '2AG': 'cat2a',
            'SCG': 'scg'
        };"""
cat_map_replacement = """const categoryMap = {
            'GM': 'cutoff',
            '2A': '2A',
            '2B': '2B',
            '3A': '3A',
            '3B': '3B',
            'SC': 'SC',
            'ST': 'ST'
        };"""
html = html.replace(cat_map_target, cat_map_replacement)

# Add code replacement for college code
html = html.replace("${item.code}", "KEA") # We didn't parse KEA codes in the merged script.

with open('cutoffs.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated cutoffs.html")
