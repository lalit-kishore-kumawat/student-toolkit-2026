const fs = require('fs');
const content = fs.readFileSync('final_colleges.js', 'utf8');
const m = content.match(/"branch":\s*"(.*?)"/g);
if (m) {
  const s = new Set(m.map(x => x.split('"')[3]));
  console.log(Array.from(s));
}
