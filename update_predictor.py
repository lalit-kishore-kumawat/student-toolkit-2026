import re

with open('final_colleges.js', 'r') as f:
    js_data = f.read().strip()

with open('predictor.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Branch dropdown
branch_html_target = """<option value="EEE">Electrical & Electronics (EEE)</option>"""
branch_html_replacement = """<option value="EEE">Electrical & Electronics (EEE)</option>
          <option value="ME">Mechanical Engineering (ME)</option>
          <option value="CV">Civil Engineering (CV)</option>
          <option value="Chemical">Chemical Engineering</option>
          <option value="Biotech">Biotechnology</option>"""
if branch_html_target in html:
    html = html.replace(branch_html_target, branch_html_replacement)

# 2. Add Tier Badge CSS
if '.tier-badge' not in html:
    css_target = """    .cta-bottom a {"""
    css_replacement = """    .tier-badge {
      display: inline-block;
      font-size: 0.7rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      background: #f1f5f9;
      color: #475569;
      border: 1px solid #cbd5e1;
      margin-bottom: 8px;
      letter-spacing: 0.05em;
    }
    .cta-bottom a {"""
    html = html.replace(css_target, css_replacement)

# 3. Replace collegeData and masterColleges
# Find the start of const collegeData = [
start_idx = html.find('const collegeData = [')
# Find the start of const bookmarks = new Set();
end_idx = html.find('const bookmarks = new Set();')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + js_data + "\\n\\n    /* Track bookmarks (UI only, session state) */\\n    " + html[end_idx:]
else:
    print("Could not find collegeData block!")

# 4. Replace runPrediction function to include tierLabel
start_pred = html.find('function runPrediction() {')
end_pred = html.find('function toggleBookmark')

new_pred = """function runPrediction() {
      const rankInput = document.getElementById("rank");
      const branchChoice = document.getElementById("branch").value;
      const categoryChoice = document.getElementById("category").value;
      const container = document.getElementById("results-container");
      const legend = document.getElementById("legend");
      const btn = document.getElementById("predictBtn");

      const rank = parseInt(rankInput.value);

      /* Input validation */
      if (!rank || rank <= 0 || rank > 300000) {
        rankInput.classList.add("error");
        container.innerHTML = `<div class='no-results'>⚠️ Please enter a valid KCET rank (1 – 3,00,000).</div>`;
        legend.style.display = "none";
        return;
      }
      rankInput.classList.remove("error");

      /* Loading state */
      btn.disabled = true;
      btn.innerText = "Analyzing...";
      container.innerHTML = "";
      legend.style.display = "none";

      setTimeout(() => {
        /* Filter + score colleges */
        const results = collegeData
          .map(c => {
            const categoryCutoff = categoryChoice === "GM" ? c.cutoff : c[categoryChoice];
            const adjustedCutoff = categoryCutoff ? Math.floor(categoryCutoff * 1.1) : 0;
            return { ...c, categoryCutoff, adjustedCutoff };
          })
          .filter(c => {
            if (!c.adjustedCutoff || c.adjustedCutoff === 0) return false;
            const branchMatch = (branchChoice === "ALL" || c.branch === branchChoice);
            const withinRange = rank <= c.adjustedCutoff * 1.2;
            return branchMatch && withinRange;
          })
          .map(c => {
            const chance = calcProbability(rank, c.adjustedCutoff);
            const category = getCategory(chance);
            return { ...c, chance, ...category };
          })
          .filter(c => c.chance > 0)
          /* Sort: highest probability first */
          .sort((a, b) => b.chance - a.chance)
          .slice(0, 12);

        /* Render */
        if (results.length === 0) {
          container.innerHTML = `
        <div class='no-results'>
          😔 No matches found for rank <b>${rank.toLocaleString()}</b>.<br>
          <small>Try selecting "All Tech Branches" or check if your rank is in a valid range.</small>
        </div>`;
        } else {
          /* Rank range tip */
          const minCutoff = Math.min(...results.map(r => r.categoryCutoff));
          const maxCutoff = Math.max(...results.map(r => r.categoryCutoff));

          let html = `
        <div class="rank-range-tip">
          🎯 You can target colleges in the <b>${minCutoff.toLocaleString()} – ${maxCutoff.toLocaleString()}</b> cutoff range
        </div>
        <div class="results-header">
          <span>Showing top matches for rank <b>${rank.toLocaleString()}</b></span>
          <span style="color:var(--text-muted);">${branchChoice === "ALL" ? "All Branches" : branchChoice} • ${categoryChoice}</span>
        </div>`;

          results.forEach((item, i) => {
            const isBest = i === 0;
            const bestLabel = isBest ? `<div class="best-label">⭐ BEST MATCH</div>` : "";
            const cardClass = isBest ? "result-card best" : "result-card";
            const bookmarkIcon = bookmarks.has(item.name + item.branch) ? "🔖" : "🔖";
            const bookmarkSaved = bookmarks.has(item.name + item.branch) ? "saved" : "";

            html += `
          <div class="${cardClass}" id="card-${i}">
            <div class="college-info">
              ${bestLabel}
              <div class="tier-badge">${item.tierLabel || "📍 Tier 5"}</div>
              <h3>${item.name}</h3>
              <div class="meta">
                <span>${item.branch}</span>
                <span>Cutoff: ${item.categoryCutoff.toLocaleString()}</span>
              </div>
            </div>
            <button
              class="bookmark-btn ${bookmarkSaved}"
              onclick="toggleBookmark('${item.name}', '${item.branch}', this)"
              title="Save college">🔖</button>
            <div class="badge ${item.css}">
              ${item.label}
              <span class="pct">${item.chance}%</span>
            </div>
          </div>`;
          });

          html += `

        <div class="cta-bottom">
          📋 Want to explore all cutoffs by category?<br>
          <a href="cutoffs.html">Check the Cutoffs Tab →</a>
        </div>`;

          container.innerHTML = html;
          legend.style.display = "block";
        }

        /* Restore button */
        btn.disabled = false;
        btn.innerText = "Analyze My Chances →";

      }, 400);
    }

    /* ═══════════════════════════════════════════════
       BOOKMARK — UI only (session state)
       ═══════════════════════════════════════════════ */
    """

if start_pred != -1 and end_pred != -1:
    html = html[:start_pred] + new_pred + html[end_pred:]
else:
    print("Could not find runPrediction block!")

with open('predictor.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated predictor.html successfully!")
