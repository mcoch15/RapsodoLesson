from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any
from .engine import analyze_hitting, analyze_pitching
from .lessons import lesson_copy

app = FastAPI(title="Rapsodo Interactive Lesson API", version="0.2.0")

app.mount("/static", StaticFiles(directory="public"), name="static")

ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "https://YOUR-STORE.myshopify.com",
    "https://shop.YOURDOMAIN.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class HittingInput(BaseModel):
    level: Literal["youth","hs","college","pro"] = "hs"
    handedness: Literal["R","L"] = "R"
    # new required data points
    exit_velocity: float          # mph
    launch_angle: float           # degrees
    exit_direction: float         # degrees (pull <0, oppo >0, or use -45..+45 convention)
    distance: float               # feet
    spin_rate: int                # rpm
class PitchingInput(BaseModel):
     level: Literal["youth","hs","college","pro"] = "hs"
    handedness: Literal["R","L"] = "R"
    pitch_type: Literal["FF","SI","SL","CT","CB","CH","SPL","SP"] = "FF"
    velocity: float               # mph
    total_spin: int               # rpm
    spin_direction: float         # clockface in degrees (e.g., 180 ~ 6:00 RHP FF)
    gyro_degree: float            # 0..90
    spin_efficiency: float        # 0..1
    release_height: float         # ft
    vertical_break: float         # in  (IVB)
    horizontal_break: float       # in  (HB)

class Lesson(BaseModel):
    summary: str
    focus: List[str]
    drills: List[Dict[str, Any]]
    cues: List[str]
    metrics_to_track: List[str]
    est_time_min: int

@app.post("/analyze/hitting", response_model=Lesson)
def analyze_h(d: HittingInput):
    recs = analyze_hitting(d.model_dump())
    return lesson_copy("hitting", d.model_dump(), recs)

@app.post("/analyze/pitching", response_model=Lesson)
def analyze_p(d: PitchingInput):
    recs = analyze_pitching(d.model_dump())
    return lesson_copy("pitching", d.model_dump(), recs)

@app.get("/health")
def health():
    return {"ok": True}
from fastapi.responses import RedirectResponse, HTMLResponse

@app.get("/", response_class=HTMLResponse)
def index():
    # Either redirect to the preview page...
    return RedirectResponse(url="/static/widget.html")
    # ...or render a tiny HTML index (uncomment below and remove the line above):
    # return """
    # <!doctype html><html><body style="font-family:system-ui">
    #   <h1>Rapsodo Interactive Lesson API</h1>
    #   <p>Try: <a href="/docs">/docs</a> or the <a href="/static/widget.html">widget preview</a>.</p>
    # </body></html>
    # """
