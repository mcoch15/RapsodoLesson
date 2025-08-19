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
    samples: int = Field(ge=1)
    avg_ev: float
    max_ev: float
    avg_la: float
    hard_hit_rate: float = Field(..., ge=0, le=1)
    gb_rate: float = Field(..., ge=0, le=1)
    airball_rate: float = Field(..., ge=0, le=1)
    pull_rate: float = Field(..., ge=0, le=1)
    oppo_rate: float = Field(..., ge=0, le=1)
    sweet_spot_rate: float = Field(..., ge=0, le=1)

class PitchingInput(BaseModel):
    level: Literal["youth","hs","college","pro"] = "hs"
    handedness: Literal["R","L"] = "R"
    pitch_type: Literal["FF","SI","SL","CT","CB","CH","SPL","SP"] = "FF"
    avg_velo: float
    spin_rate: int
    spin_efficiency: float = Field(..., ge=0, le=1)
    ivb: float
    hb: float
    release_height: float
    release_side: float
    extension: float
    zone_rate: float = Field(..., ge=0, le=1)
    whiff_rate: float = Field(..., ge=0, le=1)

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
