(function(){
  const mountId = "rapsodo-lesson-widget";
  const el = document.getElementById(mountId);
  if (!el) return;

  const css = `
    .rl-card{border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:8px 0;background:#fff}
    .rl-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
    @media (max-width:720px){.rl-grid{grid-template-columns:1fr}}
    .rl-input,.rl-select{width:100%;padding:8px;margin:6px 0;border:1px solid #d1d5db;border-radius:8px}
    .rl-btn{padding:10px 14px;border:1px solid #9ca3af;border-radius:10px;background:#f9fafb;cursor:pointer}
    pre{background:#f3f4f6;padding:12px;border-radius:8px;overflow:auto}
    h2,h3{margin:0 0 8px 0}
  `;
  const style = document.createElement("style"); style.textContent = css; document.head.appendChild(style);

  el.innerHTML = `
    <div class="rl-card">
      <h2>Build Your Personalized Lesson</h2>
      <label>Mode</label>
      <select id="rl-mode" class="rl-select">
        <option value="hitting">Hitting</option>
        <option value="pitching">Pitching</option>
      </select>
      <div class="rl-grid">
        <div>
          <label>Level</label>
          <select id="rl-level" class="rl-select">
            <option value="youth">Youth</option>
            <option value="hs" selected>HS</option>
            <option value="college">College</option>
            <option value="pro">Pro</option>
          </select>
        </div>
        <div>
          <label>Handedness</label>
          <select id="rl-handedness" class="rl-select">
            <option value="R" selected>Right</option>
            <option value="L">Left</option>
          </select>
        </div>
      </div>

      <div id="rl-hit" class="rl-card">
        <h3>Hitting Metrics</h3>
        <div class="rl-grid">
          <div><label>Samples</label><input id="rl-samples" class="rl-input" type="number" value="25"></div>
          <div><label>Avg EV (mph)</label><input id="rl-avg_ev" class="rl-input" type="number" value="82"></div>
          <div><label>Max EV (mph)</label><input id="rl-max_ev" class="rl-input" type="number" value="94"></div>
          <div><label>Avg Launch Angle (°)</label><input id="rl-avg_la" class="rl-input" type="number" value="10"></div>
          <div><label>Hard-Hit Rate (0-1)</label><input id="rl-hard_hit_rate" class="rl-input" type="number" step="0.01" value="0.35"></div>
          <div><label>Ground-Ball Rate (0-1)</label><input id="rl-gb_rate" class="rl-input" type="number" step="0.01" value="0.48"></div>
          <div><label>Airball Rate (0-1)</label><input id="rl-airball_rate" class="rl-input" type="number" step="0.01" value="0.30"></div>
          <div><label>Pull % (0-1)</label><input id="rl-pull_rate" class="rl-input" type="number" step="0.01" value="0.55"></div>
          <div><label>Oppo % (0-1)</label><input id="rl-oppo_rate" class="rl-input" type="number" step="0.01" value="0.20"></div>
          <div><label>Sweet Spot % (0-1)</label><input id="rl-sweet_spot_rate" class="rl-input" type="number" step="0.01" value="0.27"></div>
        </div>
      </div>

      <div id="rl-pitch" class="rl-card" style="display:none">
        <h3>Pitching Metrics</h3>
        <div class="rl-grid">
          <div><label>Pitch Type</label>
            <select id="rl-pitch_type" class="rl-select">
              <option value="FF" selected>FF</option>
              <option value="SI">SI</option>
              <option value="SL">SL</option>
              <option value="CT">CT</option>
              <option value="CB">CB</option>
              <option value="CH">CH</option>
              <option value="SPL">SPL</option>
              <option value="SP">SP</option>
            </select>
          </div>
          <div><label>Avg Velo (mph)</label><input id="rl-avg_velo" class="rl-input" type="number" value="84"></div>
          <div><label>Spin Rate (rpm)</label><input id="rl-spin_rate" class="rl-input" type="number" value="2200"></div>
          <div><label>Spin Efficiency (0-1)</label><input id="rl-spin_efficiency" class="rl-input" type="number" step="0.01" value="0.86"></div>
          <div><label>IVB (in)</label><input id="rl-ivb" class="rl-input" type="number" value="13"></div>
          <div><label>HB (in)</label><input id="rl-hb" class="rl-input" type="number" value="5"></div>
          <div><label>Release Height (ft)</label><input id="rl-release_height" class="rl-input" type="number" value="5.7"></div>
          <div><label>Release Side (ft)</label><input id="rl-release_side" class="rl-input" type="number" value="2.2"></div>
          <div><label>Extension (ft)</label><input id="rl-extension" class="rl-input" type="number" value="5.7"></div>
          <div><label>Zone Rate (0-1)</label><input id="rl-zone_rate" class="rl-input" type="number" step="0.01" value="0.45"></div>
          <div><label>Whiff Rate (0-1)</label><input id="rl-whiff_rate" class="rl-input" type="number" step="0.01" value="0.25"></div>
        </div>
      </div>

      <button id="rl-go" class="rl-btn">Generate Lesson</button>
    </div>

    <div id="rl-out" class="rl-card" style="display:none">
      <h3>Your Lesson</h3>
      <pre id="rl-json"></pre>
    </div>
  `;

  const $ = (id)=>document.getElementById(id);
  const modeSel = $("rl-mode"), hitBox = $("rl-hit"), pitchBox = $("rl-pitch");
  modeSel.addEventListener("change", ()=> {
    const v = modeSel.value;
    hitBox.style.display = v==="hitting" ? "block" : "none";
    pitchBox.style.display = v==="pitching" ? "block" : "none";
  });

  const API_BASE = window.API_BASE || "http://127.0.0.1:8000";

  $("rl-go").addEventListener("click", async ()=>{
    const common = { level:$("rl-level").value, handedness:$("rl-handedness").value };
    const mode = $("rl-mode").value;
    const payload = (mode==="hitting") ? {
      ...common,
      samples:+$("rl-samples").value, avg_ev:+$("rl-avg_ev").value, max_ev:+$("rl-max_ev").value, avg_la:+$("rl-avg_la").value,
      hard_hit_rate:+$("rl-hard_hit_rate").value, gb_rate:+$("rl-gb_rate").value, airball_rate:+$("rl-airball_rate").value,
      pull_rate:+$("rl-pull_rate").value, oppo_rate:+$("rl-oppo_rate").value, sweet_spot_rate:+$("rl-sweet_spot_rate").value
    } : {
      ...common,
      pitch_type:$("rl-pitch_type").value, avg_velo:+$("rl-avg_velo").value, spin_rate:+$("rl-spin_rate").value,
      spin_efficiency:+$("rl-spin_efficiency").value, ivb:+$("rl-ivb").value, hb:+$("rl-hb").value,
      release_height:+$("rl-release_height").value, release_side:+$("rl-release_side").value, extension:+$("rl-extension").value,
      zone_rate:+$("rl-zone_rate").value, whiff_rate:+$("rl-whiff_rate").value
    };
    const url = API_BASE + (mode==="hitting") ? "/analyze/hitting" : "/analyze/pitching";

    const out = document.getElementById("rl-json"), box = document.getElementById("rl-out");
    try {
      const r = await fetch(API_BASE + (mode==="hitting" ? "/analyze/hitting" : "/analyze/pitching"), {
        method:"POST", headers:{ "Content-Type":"application/json" }, body:JSON.stringify(payload)
      });
      if (!r.ok) { out.textContent = "Error: "+r.status+" "+(await r.text()); box.style.display="block"; return; }
      const data = await r.json();
      out.textContent = JSON.stringify(data, null, 2);
      box.style.display = "block";
    } catch (e) {
      out.textContent = "Network error: " + e.message + "\nCheck API_BASE and CORS.";
      box.style.display = "block";
    }
  });
})();
