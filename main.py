import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openbb import obb
import pandas as pd

app = FastAPI(title="Custom OpenBB Backend", version="0.1.0")

# CORS 설정 (OpenBB Workspace와 연동을 위해 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 설정 파일 로드 함수 ---
def load_json(name):
    # name에 .json이 포함되어 있을 수 있으므로 처리 방식 변경
    path = Path(__file__).parent / name
    if not path.suffix:
        path = path.with_suffix(".json")
    return json.loads(path.read_text())

# --- 메타데이터 엔드포인트 ---
@app.get("/manifest.json")
def get_manifest():
    return {
        "name": "Custom Backend",
        "widgets_url": "/widgets.json",
        "apps_url": "/apps.json"
    }

@app.get("/widgets.json")
def get_widgets():
    return JSONResponse(content=load_json("widgets.json"))

@app.get("/apps.json")
def get_apps():
    return JSONResponse(content=load_json("apps.json"))

# --- 데이터 엔드포인트 (핵심 로직) ---
@app.get("/api/v1/us_cpi")
def get_us_cpi(start_date: str = "2020-01-01"):
    # 일일이 Key를 주입할 필요 없이 바로 호출 (로컬 설정 활용)
    res = obb.economy.fred_series(symbol="CPIAUCSL", transform="pc1", start_date=start_date)
    df = res.to_df().reset_index()
    
    # 데이터 가공 및 반환 (df.columns는 'date', 'value'로 가정)
    df.columns = ['date', 'value']
    df['indicator'] = 'US CPI YoY %'
    
    # NaN 값 0으로 치환 후 레코드 반환
    return df.fillna(0).to_dict(orient="records")

@app.get("/hello_world")
def hello_world(name: str = ""):
    return f"# Hello {name or 'OpenBB'}"

@app.get("/")
def health():
    return {"status": "running"}
