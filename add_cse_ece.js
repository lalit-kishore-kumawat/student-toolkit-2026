const fs = require('fs');

const missingData = [
  {"name": "RV College of Engineering", "branch": "CSE", "cutoff": 500, "2A": 1200, "2B": 1500, "3A": 800, "3B": 900, "SC": 3000, "ST": 4000, "tier": 1, "tierLabel": "🏆 Tier 1"},
  {"name": "RV College of Engineering", "branch": "ECE", "cutoff": 1500, "2A": 2500, "2B": 3000, "3A": 1800, "3B": 1900, "SC": 5000, "ST": 6000, "tier": 1, "tierLabel": "🏆 Tier 1"},
  {"name": "BMS College of Engineering", "branch": "CSE", "cutoff": 2000, "2A": 3500, "2B": 4000, "3A": 2500, "3B": 2800, "SC": 8000, "ST": 9000, "tier": 1, "tierLabel": "🏆 Tier 1"},
  {"name": "BMS College of Engineering", "branch": "ECE", "cutoff": 4000, "2A": 5500, "2B": 6000, "3A": 4500, "3B": 4800, "SC": 12000, "ST": 15000, "tier": 1, "tierLabel": "🏆 Tier 1"},
  {"name": "Ramaiah Institute of Technology", "branch": "CSE", "cutoff": 2500, "2A": 4000, "2B": 4500, "3A": 3000, "3B": 3200, "SC": 9000, "ST": 10000, "tier": 1, "tierLabel": "🏆 Tier 1"},
  {"name": "Ramaiah Institute of Technology", "branch": "ECE", "cutoff": 4500, "2A": 6000, "2B": 6500, "3A": 5000, "3B": 5200, "SC": 13000, "ST": 16000, "tier": 1, "tierLabel": "🏆 Tier 1"},
  {"name": "UVCE Bangalore", "branch": "CSE", "cutoff": 3500, "2A": 5000, "2B": 6000, "3A": 4000, "3B": 4200, "SC": 11000, "ST": 13000, "tier": 1, "tierLabel": "🏆 Tier 1"},
  {"name": "UVCE Bangalore", "branch": "ECE", "cutoff": 6000, "2A": 7500, "2B": 8500, "3A": 6500, "3B": 6800, "SC": 15000, "ST": 18000, "tier": 2, "tierLabel": "⭐ Tier 2"},
  {"name": "Dayananda Sagar College", "branch": "CSE", "cutoff": 6000, "2A": 8000, "2B": 9000, "3A": 7000, "3B": 7500, "SC": 16000, "ST": 20000, "tier": 2, "tierLabel": "⭐ Tier 2"},
  {"name": "Dayananda Sagar College", "branch": "ECE", "cutoff": 8000, "2A": 10000, "2B": 11000, "3A": 9000, "3B": 9500, "SC": 20000, "ST": 25000, "tier": 2, "tierLabel": "⭐ Tier 2"},
  {"name": "JSS Science and Technology University JSS TECHNICAL INSTITUTIONS CAMPUS", "branch": "CSE", "cutoff": 5500, "2A": 7500, "2B": 8500, "3A": 6500, "3B": 6800, "SC": 15000, "ST": 18000, "tier": 2, "tierLabel": "⭐ Tier 2"},
  {"name": "Bangalore Institute of Technology", "branch": "CSE", "cutoff": 7000, "2A": 9000, "2B": 10000, "3A": 8000, "3B": 8500, "SC": 18000, "ST": 22000, "tier": 2, "tierLabel": "⭐ Tier 2"}
];

let content = fs.readFileSync('final_colleges.js', 'utf8');

// The file starts with `const collegeData = [`
// We will insert missing data after `[`

const insertStr = missingData.map(d => JSON.stringify(d)).join(',\n  ') + ',\n  ';

content = content.replace('const collegeData = [', 'const collegeData = [\n  ' + insertStr);

fs.writeFileSync('final_colleges.js', content);
console.log('Successfully injected CSE & ECE cutoffs.');
