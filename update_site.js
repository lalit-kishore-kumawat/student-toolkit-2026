const fs = require('fs');

// 1. Update sitemap.xml
let sitemap = fs.readFileSync('sitemap.xml', 'utf8');
sitemap = sitemap.replace(/<lastmod>.*<\/lastmod>/g, '<lastmod>2026-04-29</lastmod>');
fs.writeFileSync('sitemap.xml', sitemap);

// 2. Add 'About' to bottom nav in all html files
const htmlFiles = ['index.html', 'predictor.html', 'cutoffs.html', 'marks-to-rank.html', 'kcet-cutoff-2025.html', 'about.html'];

for (const file of htmlFiles) {
  let content = fs.readFileSync(file, 'utf8');
  
  // check if 'about.html' is already in bottom nav
  if (content.includes('about.html') && content.match(/<a href="about\.html" class="nav-item.*">/)) {
    // it exists? Let's check specifically in bottom nav context.
    const navMatch = content.match(/<nav class="bottom-nav">[\s\S]*?<\/nav>/);
    if (navMatch && !navMatch[0].includes('about.html')) {
      const activeClass = file === 'about.html' ? 'nav-item active' : 'nav-item';
      const insertStr = `\n    <a href="about.html" class="${activeClass}">\n      <span class="nav-icon">ℹ️</span>About\n    </a>\n  </nav>`;
      content = content.replace('  </nav>', insertStr);
      fs.writeFileSync(file, content);
      console.log('Updated ' + file);
    }
  } else {
      const navMatch = content.match(/<nav class="bottom-nav">[\s\S]*?<\/nav>/);
      if (navMatch && !navMatch[0].includes('about.html')) {
        const activeClass = file === 'about.html' ? 'nav-item active' : 'nav-item';
        const insertStr = `\n    <a href="about.html" class="${activeClass}">\n      <span class="nav-icon">ℹ️</span>About\n    </a>\n  </nav>`;
        content = content.replace('  </nav>', insertStr);
        fs.writeFileSync(file, content);
        console.log('Updated ' + file);
      }
  }
}
