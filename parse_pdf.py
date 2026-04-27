import pdfplumber
import json
import re

pdf_path = 'cutoff.pdf'

colleges = []
current_college_name = None

def parse_pdf():
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text: continue
            
            lines = text.split('\n')
            for line in lines:
                # E001 Univesity of Visvesvaraya College...
                match_col = re.match(r'^(E\d{3})\s+(.+)', line)
                if match_col and "Course Name" not in line and "Seat Type" not in line and "College:" not in line:
                    # check if it actually looks like a college header
                    pass
                    
                if "College:" in line:
                    match = re.search(r'College:\s*(E\d{3})\s*(.+)', line)
                    if match:
                        current_college_name = match.group(2).strip()
                        # Shorten the name if needed, but keeping it is fine.
                        continue
                
                # Check for courses like "ARTIFICIAL 11952 -- -- 8509"
                # wait, the headers are: 1G 1K 1R 2AG 2AK 2AR 2BG 2BK 2BR 3AG 3AK 3AR 3BG 3BK 3BR GM GMK GMP GMR NRI OPN OTH SCG SCK SCR STG STK STR
                # Which is 28 columns after course name. Sometimes course names have multiple words.
                # Usually it ends with numbers and '--'.
                # Let's extract 1G, 2AG, 2BG, 3AG, 3BG, GM, SCG, STG
                # Their indices in the column list:
                # 1G: 0
                # 2AG: 3
                # 2BG: 6
                # 3AG: 9
                # 3BG: 12
                # GM: 15
                # SCG: 21
                # STG: 24
                
                parts = line.split()
                if len(parts) > 20:
                    # Ranks part starts from the end
                    ranks = parts[-28:]
                    if len(ranks) == 28:
                        course_name = " ".join(parts[:-28])
                        if course_name == "": continue
                        
                        def parse_rank(val):
                            if val == '--': return 0
                            # sometimes floats like 10643.5, taking int
                            try: return int(float(val))
                            except: return 0
                        
                        gm = parse_rank(ranks[15])
                        cat_2a = parse_rank(ranks[3])
                        cat_2b = parse_rank(ranks[6])
                        cat_3a = parse_rank(ranks[9])
                        cat_3b = parse_rank(ranks[12])
                        sc = parse_rank(ranks[21])
                        st = parse_rank(ranks[24])
                        
                        if gm > 0 and current_college_name:
                            colleges.append({
                                "name": current_college_name,
                                "branch": course_name,
                                "cutoff": gm,
                                "2A": cat_2a,
                                "2B": cat_2b,
                                "3A": cat_3a,
                                "3B": cat_3b,
                                "SC": sc,
                                "ST": st
                            })

parse_pdf()
print(f"Extracted {len(colleges)} courses.")
with open('extracted_data.json', 'w') as f:
    json.dump(colleges, f, indent=2)
