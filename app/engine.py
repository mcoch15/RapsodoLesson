from typing import Dict, Any, List

def analyze_hitting_engine(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inputs: exit_velocity, launch_angle, exit_direction, distance, spin_rate, level, handedness
    """
    notes: List[str] = []
    focus: List[str] = []
    drills: List[Dict[str, Any]] = []
    metrics = ["exit_velocity","launch_angle","exit_direction","distance","spin_rate"]

    # Simple EV targets by level (tune for your org)
    ev_floor = {"youth":72, "hs":78, "college":85, "pro":90}.get(d["level"], 78)
    if d["exit_velocity"] < ev_floor:
        focus.append("Increase bat speed / impact quality")
        notes.append(f"EV {d['exit_velocity']:.0f} < target {ev_floor}.")
        drills.append({
            "title":"Overload/Underload Bats",
            "sets":3, "reps":6,
            "how":"2 swings +10%, 2 game bat, 2 -10%. Track EV each swing."
        })

    # Launch angle heuristics (typical damage lane ≈10–25°)
    la = d["launch_angle"]
    if la < 8:
        focus.append("Raise attack angle / contact point")
        notes.append(f"Low LA {la:.0f}° → GB risk.")
        drills.append({"title":"Tee Ladder (Knee→Rib)","sets":4,"reps":5,
                       "how":"Progress tee height; maintain barrel through the zone."})
    elif la > 28:
        focus.append("Reduce excessive loft")
        notes.append(f"High LA {la:.0f}° → high flies.")
        drills.append({"title":"Deep Contact Opposite-Field","sets":3,"reps":8,
                       "how":"Let ball travel; cue 'barrel through, not under'."})

    # Direction bias: large pull/oppo angles
    if abs(d["exit_direction"]) > 30:
        side = "pull" if d["exit_direction"] < 0 else "opposite"
        focus.append("Use full field / direction control")
        notes.append(f"Heavy {side} tendency (dir {d['exit_direction']:.0f}°).")
        drills.append({"title":"Gap-to-Gap Machine","sets":4,"reps":7,
                       "how":"Aim liners to middle/oppo; score only middle/oppo."})

    # Distance sanity relative to EV & LA
    if d["distance"] < 180 and d["exit_velocity"] >= ev_floor - 4:
        focus.append("Optimize flight for carry")
        notes.append("Adequate EV but short distance — fine-tune LA & direction.")
    if d["distance"] > 360 and la > 30:
        focus.append("Flatten peak contact for consistency")
        notes.append("Very long/high — chase 10–25° for repeatable damage.")

    # Batted spin: high backspin + high LA → undercut tendency
    if d["spin_rate"] > 2500 and la > 25:
        focus.append("Reduce undercut / improve smash")
        notes.append(f"High spin {d['spin_rate']:.0f} rpm with loft; work through the ball.")
        drills.append({"title":"Top-Hand Line Drives","sets":3,"reps":8,
                       "how":"Palm-up/palm-down through; target 12–18°."})

    summary = "; ".join(notes) if notes else "Balanced hitting profile — maintain and compete."
    return {
        "mode": "hitting",
        "summary": summary,
        "focus": list(dict.fromkeys(focus)),
        "drills": drills,
        "cues": ["See it early; commit late.","Strong path through contact.","Win the middle third."],
        "metrics_to_track": metrics,
        "est_time_min": 30 if drills else 20
    }


def analyze_pitching_engine(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inputs: velocity, total_spin, spin_direction, gyro_degree, pitch_type,
            spin_efficiency, release_height, vertical_break, horizontal_break, level, handedness
    """
    notes: List[str] = []
    focus: List[str] = []
    drills: List[Dict[str, Any]] = []
    metrics = ["velocity","total_spin","spin_direction","gyro_degree","pitch_type",
               "spin_efficiency","release_height","vertical_break","horizontal_break"]

    # Fastball ride & efficiency heuristic
    if d["pitch_type"] == "FF":
        if d["spin_efficiency"] < 0.85 and d["vertical_break"] < 14:
            focus.append("Improve ride (axis/efficiency)")
            notes.append("Below-avg ride and efficiency; tighten axis window.")
            drills.append({"title":"Axis Mirror + Clean Fire","sets":3,"reps":8,
                           "how":"Mirror ~12:30–1:00 feel; clean-fire plyo staying behind ball."})
        # Simple command progression (no zone% in v2; still include a command drill)
        drills.append({"title":"9-Box Glove-Side Challenge","sets":3,"reps":6,
                       "how":"Hit 4/6 boxes glove-side; log misses & adjust plan."})
        if d["release_height"] < 5.5:
            focus.append("Posture / release height consistency")
            notes.append(f"Low release height {d['release_height']:.2f} ft — check posture & timing.")

    # Breaking ball sharpness: high gyro or low eff
    if d["pitch_type"] in ["SL","CB","SP"] and (d["gyro_degree"] > 45 or d["spin_efficiency"] < 0.6):
        focus.append("Sharpen breaking ball efficiency/tilt")
        notes.append(f"Gyro {d['gyro_degree']:.0f}° / eff {d['spin_efficiency']:.2f} — refine finger pressure.")
        drills.append({"title":"Tunnel Pairs (FF/BRK)","sets":3,"reps":10,
                       "how":"Match release; adjust pressure to shift tilt while keeping late break."})

    # Side movement shaping for SI/CH/CT if HB is small
    if abs(d["horizontal_break"]) < 3 and d["pitch_type"] in ["SI","CH","CT"]:
        focus.append("Add horizontal separation")
        notes.append("Limited HB — use pronation/supination cues for shape.")
        drills.append({"title":"One-Seam/Pronated Change Progression","sets":3,"reps":8,
                       "how":"One-seam feel; pronation through release to add arm-side run."})

    # Spin direction vs expected (rough example values; tune to org)
    expected = {
        "FF": 180.0, "SI": 165.0, "SL": 30.0, "CT": 210.0, "CB": 45.0, "CH": 150.0, "SPL": 155.0, "SP": 60.0
    }.get(d["pitch_type"], 180.0)
    if abs(d["spin_direction"] - expected) > 30:
        focus.append("Refine spin axis for intended shape")
        notes.append(f"Spin dir {d['spin_direction']:.0f}° deviates from ~{expected:.0f}° for {d['pitch_type']}.")

    summary = "; ".join(notes) if notes else "Competitive profile — progress command, shape, and sequencing."
    return {
        "mode": "pitching",
        "summary": summary,
        "focus": list(dict.fromkeys(focus)),
        "drills": drills,
        "cues": ["Stay closed; deliver late.","Own glove-side lanes.","Win neutral counts."],
        "metrics_to_track": metrics,
        "est_time_min": 30 if drills else 20
    }

