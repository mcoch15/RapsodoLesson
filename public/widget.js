(function(){
  const mountId = "rapsodo-lesson-widget";
  const el = document.getElementById(mountId);
  if (!el) return;

  // Minimal styles
  const css = `
    .rl-card{border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:8px 0;background:#fff}
    .rl-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
    @media (max-width:720px){.rl-grid{grid-template-columns:1fr}}
    .rl-input,.rl-select{width:100%;padding:8px;margin:6px 0;border:1px solid #d1d5db;border-radius:8px}
    .rl-btn{padding:10px 14px;border:1px solid #9ca3af;border-radius:10px;background:#f9fafb;cursor:pointer}
    pre{background:#f3f4f6;padding:12px;border-radius:8px;overflow:auto}
    h2,h3{margin:0 0 8px 0}
  `;
  const style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  // UI with NEW metric fields
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

      <!-- Hitting (NEW fields) -->
      <div id="rl-hit" class="rl-card">
        <h3>Hitting Metrics</h3>
        <div class="rl-grid">
          <div><label>Exit Velocity (mph)</label><input id="rl-exit_velocity" class="rl-input" type="number" value="82"></div>
          <div><label>Launch Angle (°)</label><input id="rl-launch_angle" class="rl-input" type="number" value="15"></div>
          <div><label>Exit Direction (°)</label><input id="rl-exit_direction" class="rl-input" type="number" value="0"></div>
          <div><label>Distance (ft)</label><input id="rl-distance" class="rl-input" type="number" value="300"></div>
          <div><label>Spin Rate (rpm)</label><input id="rl-batted_spin" class="rl-input" type="number" value="1800"></div>
        </div>
      </div>

      <!-- Pitching (NEW fields) -->
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
          <div><label>Velocity (mph)</label><input id="rl-velocity" class="rl-input" type="number" value="88"></div>
          <div><label>Total Spin (rpm)</label><input id="rl-total_spin" class="rl-input" type="number" value="2200"></div>
          <div><label>Spin Direction (°)</label><input id="rl-spin_direction" class="rl-input" type="number" value="180"></div>
          <div><label>Gyro Degree (°)</label><input id="rl-gyro_degree" class="rl-input" type="number" value="15"></div>
          <div><label>Spin Efficiency (0–1)</label><input id="rl-spin_efficiency" class="rl-input" type="number" step="0.01" value="0.90"></div>
          <div><label>Release Height (ft)</label><input id="rl-release_height" class="rl-input" type="number" value="5.7"></div>
          <div><label>Vertical Break (in)</label><input id="rl-vertical_break" class="rl-input" type="number" value="14"></div>
          <div><label>Horizontal Break (in)</label><input id="rl-horizontal_break" class="rl-input" type="number" value="5"></div>
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

  // Toggle sections by mode
  $("rl-mode").addEventListener("change", ()=>{
    const v = $("rl-mode").value;
    $("rl-hit").style.display = v==="hitting" ? "block" : "none";
    $("rl-pitch").style.display = v==="pitching" ? "block" : "none";
  });

  // Click handler with NEW payloads
  $("rl-go").addEventListener("click", async ()=>{
    const mode = $("rl-mode").value;
    const common = { level:$("rl-level").value, handedness:$("rl-handedness").value };

    let payload;
    if (mode === "hitting") {
      payload = {
        ...common,
        exit_velocity: +$("rl-exit_velocity").value,
        launch_angle: +$("rl-launch_angle").value,
        exit_direction: +$("rl-exit_direction").value,
        distance: +$("rl-distance").value,
        spin_rate: +$("rl-batted_spin").value
      };
    } else {
      payload = {
        ...common,
        pitch_type: $("rl-pitch_type").value,
        velocity: +$("rl-velocity").value,
        total_spin: +$("rl-total_spin").value,
        spin_direction: +$("rl-spin_direction").value,
        gyro_degree: +$("rl-gyro_degree").value,
        spin_efficiency: +$("rl-spin_efficiency").value,
        release_height: +$("rl-release_height").value,
        vertical_break: +$("rl-vertical_break").value,
        horizontal_break: +$("rl-horizontal_break").value
      };
    }

    const base = (window.API_BASE) || window.location.origin || "http://127.0.0.1:8000";
    const path = mode === "hitting" ? "/analyze/hitting" : "/analyze/pitching";
    const url = base + path;

    const out = $("rl-json"), box = $("rl-out");
    try {
      const r = await fetch(url, { method:"POST", headers:{ "Content-Type":"application/json" }, body:JSON.stringify(payload) });
      if (!r.ok) { out.textContent = "Error: "+r.status+" "+(await r.text()); box.style.display="block"; return; }
      const data = await r.json();
      out.textContent = JSON.stringify(data, null, 2);
      box.style.display = "block";
    } catch (e) {
      out.textContent = "Network error: " + e.message + "\\nCheck API_BASE and CORS.";
      box.style.display = "block";
    }
  });
})();
