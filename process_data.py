import json

with open('extracted_data.json', 'r') as f:
    colleges = json.load(f)

branch_map = {
    'COMPUTER SCIENCE': 'CSE',
    'COMP. SC.': 'CSE',
    'ARTIFICIAL INTELLIGENCE': 'AIML',
    'ARTIFICIAL': 'AIML',
    'INFORMATION SCIENCE': 'ISE',
    'INFO.SCIENCE': 'ISE',
    'DATA SCIENCE': 'DS',
    'DATA SC.': 'DS',
    'ELECTRONICS': 'ECE',
    'ELECTRICAL': 'EEE'
}

def map_branch(name):
    name_upper = name.upper()
    if 'COMPUTER SCIENCE' in name_upper or 'COMP. SC.' in name_upper: return 'CSE'
    if 'ARTIFICIAL' in name_upper or 'AI' in name_upper or 'A.I.' in name_upper: return 'AIML'
    if 'INFORMATION' in name_upper or 'INFO' in name_upper: return 'ISE'
    if 'DATA' in name_upper: return 'DS'
    if 'ELECTRONICS' in name_upper and 'COMMUNICATION' in name_upper: return 'ECE'
    if 'ELECTRONICS' in name_upper and 'COMM' in name_upper: return 'ECE'
    if 'ELECTRICAL' in name_upper: return 'EEE'
    return None

processed = []
for c in colleges:
    branch_code = map_branch(c['branch'])
    if branch_code:
        # shorten college names
        col_name = c['name']
        if 'Univesity' in col_name or 'University' in col_name:
            if 'Visvesvaraya' in col_name: col_name = 'UVCE Bangalore'
        elif 'R. V. College' in col_name or 'RV College' in col_name: col_name = 'RV College of Engineering'
        elif 'B M S College' in col_name: col_name = 'BMS College of Engineering'
        elif 'M S Ramaiah' in col_name: col_name = 'Ramaiah Institute of Technology'
        elif 'P E S University' in col_name: col_name = 'PES University'
        elif 'Dayananda Sagar' in col_name: col_name = 'Dayananda Sagar College'
        elif 'Bangalore Institute' in col_name: col_name = 'Bangalore Institute of Technology'
        
        # limit name length for neatness
        col_name = col_name.split('(')[0].strip()
        
        processed.append({
            "name": col_name,
            "branch": branch_code,
            "cutoff": c["cutoff"],
            "2A": c["2A"],
            "2B": c["2B"],
            "3A": c["3A"],
            "3B": c["3B"],
            "SC": c["SC"],
            "ST": c["ST"]
        })

# Unique colleges + branch (take lowest cutoff if multiple)
unique_map = {}
for p in processed:
    key = p["name"] + "|" + p["branch"]
    if key not in unique_map or p["cutoff"] < unique_map[key]["cutoff"]:
        if p["cutoff"] > 0:
            unique_map[key] = p

final_list = list(unique_map.values())
final_list.sort(key=lambda x: x["cutoff"])

with open('final_colleges.js', 'w') as f:
    f.write('const collegeData = [\n')
    for idx, c in enumerate(final_list):
        f.write(f'  {json.dumps(c)}')
        if idx < len(final_list) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    f.write('];\n')
print(f"Total processed: {len(final_list)}")
