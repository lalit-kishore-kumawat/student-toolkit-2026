import pdfplumber
import json
import re

pdfs = ['r1.pdf', 'r2.pdf', 'cutoff.pdf']
merged_data = {}

def parse_pdf(pdf_path):
    print(f"Parsing {pdf_path}...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            current_college_name = None
            for page in pdf.pages:
                text = page.extract_text()
                if not text: continue
                
                lines = text.split('\n')
                for line in lines:
                    if "College:" in line:
                        match = re.search(r'College:\s*(E\d{3})\s*(.+)', line)
                        if match:
                            current_college_name = match.group(2).strip()
                            continue
                    
                    parts = line.split()
                    if len(parts) > 20:
                        ranks = parts[-28:]
                        if len(ranks) == 28:
                            course_name = " ".join(parts[:-28])
                            if course_name == "": continue
                            
                            def parse_rank(val):
                                if val == '--': return 0
                                try: return int(float(val))
                                except: return 0
                            
                            gm = parse_rank(ranks[15])
                            cat_2a = parse_rank(ranks[3])
                            cat_2b = parse_rank(ranks[6])
                            cat_3a = parse_rank(ranks[9])
                            cat_3b = parse_rank(ranks[12])
                            sc = parse_rank(ranks[21])
                            st = parse_rank(ranks[24])
                            
                            if current_college_name:
                                key = f"{current_college_name}|{course_name}"
                                if key not in merged_data:
                                    merged_data[key] = {
                                        "name": current_college_name,
                                        "branch_raw": course_name,
                                        "GM": gm,
                                        "2A": cat_2a,
                                        "2B": cat_2b,
                                        "3A": cat_3a,
                                        "3B": cat_3b,
                                        "SC": sc,
                                        "ST": st
                                    }
                                else:
                                    # Merge by taking the mathematically highest rank (most relaxed cutoff)
                                    d = merged_data[key]
                                    d["GM"] = max(d["GM"], gm)
                                    d["2A"] = max(d["2A"], cat_2a)
                                    d["2B"] = max(d["2B"], cat_2b)
                                    d["3A"] = max(d["3A"], cat_3a)
                                    d["3B"] = max(d["3B"], cat_3b)
                                    d["SC"] = max(d["SC"], sc)
                                    d["ST"] = max(d["ST"], st)
    except Exception as e:
        print(f"Error parsing {pdf_path}: {e}")

for pdf in pdfs:
    parse_pdf(pdf)

print(f"Extracted {len(merged_data)} unique courses across all rounds.")
with open('merged_raw.json', 'w') as f:
    json.dump(list(merged_data.values()), f, indent=2)

