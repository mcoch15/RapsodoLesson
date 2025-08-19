from typing import Dict, Any, List

def analyze_hitting(d: Dict[str, Any]) -> Dict[str, Any]:
    notes, focus, drills = [], [], []
    metrics = ["avg_ev","max_ev","avg_la","sweet_spot_rate","hard_hit_rate","gb_rate","airball_rate","pull_rate","oppo_rate"]

    ev_floor = {"youth":72, "hs":78, "college":85, "pro":90}[d["level"]]
    if d["avg_ev"] < ev_floor:
        focus.append("Increase bat speed / contact quality")
        notes.append("Average EV below target; train speed + centered contact.")
        drills.append({"name":"Over/Under Bats","sets":3,"reps":6,"details":"2 swings +10%, 2 game bat, 2 -10%. Track EV each swing."})
    if d["gb_rate"] > 0.5 and d["avg_la"] < 8:
        focus.append("Improve attack angle")
        notes.append("High ground balls w/ low LA; target 8–20° liners.")
        drills.append({"name":"Tee Ladder (Knee→Rib)","sets":4,"reps":5,"details":"Raise tee gradually; feel upward path."})
    if d["airball_rate"] > 0.45 and d["avg_la"] > 25:
        focus.append("Reduce excessive loft")
        notes.append("Too many high flies; work deeper contact & flatter path.")
        drills.append({"name":"Deep Contact Opposite-Field","sets":3,"reps":8,"details":"BP to oppo gap; cue 'barrel through, not under'."})
    if d["sweet_spot_rate"] < 0.28:
        focus.append("Consistent barrel control")
        notes.append("Low sweet-spot%; prioritize flush contact.")
        drills.append({"name":"Hard Line-Drive Challenge","sets":5,"reps":5,"details":"Score only 95+ EV (or +5 over avg) at 10–20°."})
    pull_bias = d["pull_rate"] - d["oppo_rate"]
    if pull_bias > 0.35:
        focus.append("Use full field")
        notes.append("Heavy pull bias; train oppo/middle liners.")
        drills.append({"name":"Gap-to-Gap Machine (Away)","sets":4,"reps":7,"details":"Machine away; score oppo/middle only."})

    return {
        "summary": "; ".join(notes) if notes else "Balanced profile—maintenance plan and compete.",
        "focus": list(dict.fromkeys(focus)),
        "drills": drills,
        "metrics_to_track": metrics,
        "est_time_min": 35 if drills else 20
    }

def analyze_pitching(d: Dict[str, Any]) -> Dict[str, Any]:
    notes, focus, drills = [], [], []
    metrics = ["avg_velo","spin_rate","spin_efficiency","ivb","hb","release_height","release_side","extension","zone_rate","whiff_rate"]

    if d["pitch_type"] == "FF":
        if d["spin_efficiency"] < 0.85 and d["ivb"] < 14:
            focus.append("Improve ride (axis/efficiency)")
            notes.append("Below-avg ride; tune axis window.")
            drills.append({"name":"Axis Mirror + Clean Fire","sets":3,"reps":8,"details":"Mirror 12:30–1:00; plyo into wall, stay behind ball."})
        if d["zone_rate"] < 0.5:
            focus.append("Strike consistency")
            notes.append("Zone% under target; simplify plan and raise in-zone intent.")
            drills.append({"name":"9-Box Command","sets":4,"reps":5,"details":"Hit 6/9 boxes before advancing; log misses."})
        if d["extension"] < 6.0:
            focus.append("Extension / timing")
            notes.append("Short extension; improve drift & late launch.")
            drills.append({"name":"Walk-Ins","sets":3,"reps":6,"details":"Controlled walk-in emphasizing hip lead & late launch."})
    if d["pitch_type"] in ["SL","CB"] and d["whiff_rate"] < 0.3:
        focus.append("Sharpen breaking ball separation")
        notes.append("Low whiff; increase separation vs FF.")
        drills.append({"name":"Tunnel Pairs","sets":3,"reps":10,"details":"FF/BRK from same release; finger pressure for late break."})

    return {
        "summary": "; ".join(notes) if notes else "Competitive profile—progress command targets and sequencing.",
        "focus": list(dict.fromkeys(focus)),
        "drills": drills,
        "metrics_to_track": metrics,
        "est_time_min": 30 if drills else 20
    }
