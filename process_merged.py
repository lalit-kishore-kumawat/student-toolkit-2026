import json

with open('merged_raw.json', 'r') as f:
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
    'ELECTRICAL': 'EEE',
    'MECHANICAL': 'ME',
    'MECH.': 'ME',
    'CIVIL': 'CV',
    'CHEMICAL': 'Chemical',
    'CHEM.': 'Chemical',
    'BIOTECH': 'Biotech'
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
    if 'MECHANICAL' in name_upper or 'MECH.' in name_upper: return 'ME'
    if 'CIVIL' in name_upper: return 'CV'
    if 'CHEMICAL' in name_upper or 'CHEM.' in name_upper: return 'Chemical'
    if 'BIOTECH' in name_upper: return 'Biotech'
    return None

# First pass: map branches and shorten names
processed = []
for c in colleges:
    branch_code = map_branch(c['branch_raw'])
    if branch_code:
        col_name = c['name']
        if 'Univesity' in col_name or 'University' in col_name:
            if 'Visvesvaraya' in col_name: col_name = 'UVCE Bangalore'
        elif 'R. V. College' in col_name or 'RV College' in col_name: col_name = 'RV College of Engineering'
        elif 'B M S College' in col_name: col_name = 'BMS College of Engineering'
        elif 'M S Ramaiah' in col_name: col_name = 'Ramaiah Institute of Technology'
        elif 'P E S University' in col_name: col_name = 'PES University'
        elif 'Dayananda Sagar' in col_name: col_name = 'Dayananda Sagar College'
        elif 'Bangalore Institute' in col_name: col_name = 'Bangalore Institute of Technology'
        
        col_name = col_name.split('(')[0].split(',')[0].strip()
        
        processed.append({
            "name": col_name,
            "branch": branch_code,
            "cutoff": c["GM"],
            "2A": c["2A"],
            "2B": c["2B"],
            "3A": c["3A"],
            "3B": c["3B"],
            "SC": c["SC"],
            "ST": c["ST"]
        })

# Unique colleges + branch (take max cutoff if multiple, since we want the most relaxed cutoff across any duplicates or specializations under the same code)
unique_map = {}
for p in processed:
    key = p["name"] + "|" + p["branch"]
    if key not in unique_map or p["cutoff"] > unique_map[key]["cutoff"]:
        # Only add if it has *some* non-zero cutoffs in any category
        if p["cutoff"] > 0 or p["2A"] > 0 or p["SC"] > 0:
            unique_map[key] = p

final_list = list(unique_map.values())

# Compute Tiers based on GM CSE rank
tier_map = {}
for c in final_list:
    if c['branch'] == 'CSE' and c['cutoff'] > 0:
        rank = c['cutoff']
        col_name = c['name']
        if col_name not in tier_map or rank > tier_map[col_name]: 
            # In case of multiple CSE variations, take the highest cutoff (most relaxed) or lowest? 
            # Let's take the lowest rank (most competitive) to define tier.
            pass

# Re-calculate with min rank for tier
for c in final_list:
    if c['branch'] == 'CSE' and c['cutoff'] > 0:
        col_name = c['name']
        if col_name not in tier_map:
            tier_map[col_name] = c['cutoff']
        else:
            tier_map[col_name] = min(tier_map[col_name], c['cutoff'])

# Assign tiers
for c in final_list:
    col_name = c['name']
    cse_rank = tier_map.get(col_name, 999999)
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

final_list.sort(key=lambda x: (x["tier"], x["cutoff"]))

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
