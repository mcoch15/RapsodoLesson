from typing import Dict, Any

def lesson_copy(mode: str, data: Dict[str, Any], recs: Dict[str, Any]) -> Dict[str, Any]:
    cues = [
        "See it early; commit late.",
        "Strong path through contact." if mode=="hitting" else "Stay closed; deliver late.",
        "Win the middle third.",
    ]
    return {
        "summary": recs["summary"],
        "focus": recs["focus"],
        "drills": [
            {
                "title": d.get("name","Drill"),
                "sets": d.get("sets",3),
                "reps": d.get("reps",6),
                "how": d.get("details",""),
                "equipment": d.get("equipment","Standard cage, tee, radar/Rapsodo"),
            } for d in recs["drills"]
        ],
        "cues": cues,
        "metrics_to_track": recs["metrics_to_track"],
        "est_time_min": recs["est_time_min"],
    }
