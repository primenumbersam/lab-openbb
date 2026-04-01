# OpenBB Data Integration 가이드 (Multi-Backend)

OpenBB Workspace에서 공식 OpenBB Platform API와 사용자가 정의한 Custom Backend를 동시에 활용하는 방법입니다.

---

## 공통 환경 설정 (인증 통합)

OpenBB의 모든 도구(`openbb-api`, Python SDK, Custom Backend)에서 공통으로 사용할 API Key를 정석적인 방법으로 등록합니다.

### 🔐 로컬 설정 파일 활용 (표준)
`~/.openbb_platform/user_settings.json` 경로에 파일을 생성하거나 수정합니다.

```json
{
  "credentials": {
    "fred_api_key": "YOUR_FRED_API_KEY",
    "kosis_api_key": "YOUR_KOSIS_API_KEY"
  }
}
```
*이렇게 설정하면 모든 OpenBB 서비스에서 별도의 인증 로직 없이 FRED/KOSIS 데이터를 사용할 수 있습니다.*

---

## 1. 공식 OpenBB Platform API (Port 6901)

OpenBB에서 제공하는 수천 개의 표준 금융 데이터를 API 형태로 서비스합니다.

```bash
# 패키지 설치
pip install "openbb[all]"

# API 서버 실행 (기본 6900 포트가 사용 중이면 6901로 자동 할당됨)
openbb-api
```
* **Endpoint**: `http://127.0.0.1:6901`
* **특징**: 주식 데이터, 경제 지표 등 OpenBB의 생태계에서 제공하는 방대한 데이터 활용.

---

## 2. Custom Data Integration (Port 7779)

사용자만의 고유한 로직이나 특수 데이터를 OpenBB Workspace에 위젯 형태로 추가하기 위한 백엔드입니다.

### 📂 프로젝트 구조
```text
├── main.py        # FastAPI 서버 로직
├── widgets.json   # 위젯 메타데이터 정의
├── apps.json      # 대시보드 레이아웃 정의
└── .env           # 로컬 환경 변수
```

### 🚀 실행 방법
```bash
# 가상환경 활성화 후 실행
uvicorn main:app --reload --host 0.0.0.0 --port 7779
```
* **Endpoint**: `http://127.0.0.1:7779`
* **특징**: `widgets.json`을 통해 내가 만든 Python 함수를 OpenBB 차트나 테이블로 시각화 가능.

---

## OpenBB Workspace 연동

[OpenBB Workspace](https://pro.openbb.co)에 접속하여 각 백엔드를 연결합니다.

1. **Backend 설정**: `Settings` -> `Connected Backends`로 이동.
2. **Preset Backend 추가**: `http://127.0.0.1:6901` 입력.
3. **Custom Backend 추가**: `http://127.0.0.1:7779` 입력.
4. **확인**: Widgets 섹션에서 내가 정의한 `Custom Backend` 카테고리가 나타나는지 확인합니다.

---

## 🔗 관련 문서
* [OpenBB Data Integration 공식 문서](https://docs.openbb.co/workspace/developers/data-integration)
* [API Key 설정 가이드](https://docs.openbb.co/odp/python/settings/user_settings/api_keys)