# Violation Detection

違規檢舉與違規紀錄管理系統。專案包含 FastAPI 後端、PostgreSQL 資料庫、Vue 管理前台，以及 Flutter 行動端。行動端負責拍攝與辨識違規相關影像，前台提供使用者、車牌、檢舉紀錄、違規紀錄與申訴管理，後端負責 API、資料儲存與違規資料自動建立。

## 專案架構

```text
.
├── backend/              # FastAPI 後端服務
│   ├── app/api/          # API routes
│   ├── app/models/       # SQLAlchemy models
│   ├── app/repositories/ # 資料存取層
│   ├── app/schemas/      # Pydantic schemas
│   └── app/main.py       # FastAPI 入口
├── frontend/             # Vue 3 + Vite 前端
│   ├── src/views/        # Home, Login, Register, Profile, Records, Appeals, Report, Map
│   ├── src/components/   # UI 與版面元件
│   └── src/stores/       # Pinia 狀態管理
├── app/                  # Flutter 行動端
│   ├── lib/screens/      # 偵測、追蹤、照片列表等畫面
│   ├── lib/providers/    # App 狀態管理
│   ├── lib/utils/        # OCR、定位、截圖、權限等工具
│   └── android/app/src/main/assets/
│       └── *.tflite      # YOLO / 違規辨識模型
├── docker-compose.yml    # PostgreSQL + FastAPI
└── init.sql              # 初始資料表與 trigger
```

## 主要功能

- 使用者註冊、資料查詢與個人資料更新
- 車牌新增、查詢與刪除
- 違規檢舉上傳，支援圖片檔案或圖片 URL
- 檢舉資料查詢與圖片讀取
- 依車牌與檢舉資料自動建立違規紀錄
- 使用者違規紀錄查詢
- 申訴建立、查詢與狀態更新
- 員警註冊與申訴處理關聯
- 前端地圖、檢舉紀錄、申訴、個人資料等頁面
- Flutter 端相機偵測、YOLO 模型推論、OCR、GPS 定位與照片紀錄

## 技術棧

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Poetry
- Uvicorn

### Frontend

- Vue 3
- Vite
- TypeScript
- Vue Router
- Pinia
- Axios
- Leaflet
- Tailwind CSS

### Mobile App

- Flutter / Dart
- Provider
- Camera
- Ultralytics YOLO
- Google ML Kit Text Recognition
- Geolocator / Geocoding
- Permission Handler

## 環境需求

- Docker Desktop
- Python 3.11 或以上
- Poetry
- Node.js 20.19+ 或 22.12+
- Flutter SDK 3.9.2 對應的 Dart SDK
- Android Studio 或可用的 Android 裝置 / 模擬器

## 環境變數

根目錄需要 `.env`，供 FastAPI 連線 PostgreSQL 使用。

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/app_db
```

如果不使用 Docker，而是在本機直接啟動後端，資料庫 host 通常要改成 `localhost`：

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/app_db
```

## 使用 Docker 啟動後端與資料庫

在根目錄執行：

```bash
docker compose up --build
```

服務啟動後：

- FastAPI: http://localhost:8000
- API docs: http://localhost:8000/docs
- DB check: http://localhost:8000/db-check
- PostgreSQL: `localhost:5432`

`init.sql` 會建立資料表，並建立 `reports_after_insert_create_violation` trigger。當新增檢舉資料時，系統會依照車牌比對 `cars` 資料表，自動建立對應的 `violations` 紀錄。

## 本機啟動後端

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

本機啟動時，請確認 `.env` 的 `DATABASE_URL` 指向可連線的 PostgreSQL。

## 啟動前端

```bash
cd frontend
npm install
npm run dev
```

預設 Vite 開發伺服器：

```text
http://localhost:5173
```

後端 CORS 目前允許：

- `http://localhost:5173`
- `http://127.0.0.1:5173`

## 啟動 Flutter App

```bash
cd app
flutter pub get
flutter run
```

App 使用相機、定位、OCR 與 YOLO 模型推論。請確認 Android 裝置或模擬器已授權相機與定位權限，且模型檔案存在於：

```text
app/android/app/src/main/assets/
```

## 主要 API

### System

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | API 健康檢查 |
| GET | `/db-check` | 資料庫連線檢查 |

### Users

| Method | Path | Description |
| --- | --- | --- |
| POST | `/users/register` | 使用者註冊 |
| GET | `/users/by-email/{email}` | 透過 email 查詢使用者 |
| PUT | `/users/by-email/{email}` | 透過 email 更新使用者資料 |

### Police

| Method | Path | Description |
| --- | --- | --- |
| POST | `/police/register` | 員警註冊 |

### Cars

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/cars/{user_id}` | 查詢使用者車牌 |
| POST | `/api/cars/{user_id}` | 新增使用者車牌 |
| DELETE | `/api/cars/{user_id}/{car_id}` | 刪除使用者車牌 |

### Reports

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/reports/upload` | 上傳檢舉資料 |
| GET | `/api/reports/` | 查詢全部檢舉資料 |
| GET | `/api/reports/{report_id}/image` | 讀取檢舉圖片 |

### Violations

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/violations/` | 查詢全部違規紀錄 |
| GET | `/api/violations/user/{user_id}` | 查詢指定使用者違規紀錄 |
| GET | `/api/violations/{violation_id}` | 查詢單筆違規詳情 |

### Appeals

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/appeals/` | 建立申訴 |
| GET | `/api/appeals/` | 查詢全部申訴 |
| GET | `/api/appeals/police/{police_id}` | 查詢指定員警負責的申訴 |
| PATCH | `/api/appeals/{appeal_id}/status` | 更新申訴狀態 |

申訴狀態支援：

```text
pending
approved
rejected
```

## 資料流程

1. 使用者註冊並新增車牌。
2. Flutter App 或前端上傳檢舉資料，包含車牌、地點、座標與圖片。
3. 後端將檢舉寫入 `reports`。
4. PostgreSQL trigger 依照檢舉車牌比對 `cars`。
5. 若找到相符車牌，自動建立 `violations`。
6. 使用者可在前端查詢違規紀錄並提出申訴。
7. 員警可查詢並更新申訴狀態。

## 常用指令

```bash
# 啟動後端與資料庫
docker compose up --build

# 停止服務
docker compose down

# 前端開發
cd frontend
npm run dev

# 前端型別檢查與打包
cd frontend
npm run build

# Flutter 安裝依賴
cd app
flutter pub get

# Flutter 執行
cd app
flutter run
```

## 注意事項

- `.env` 不應提交到 Git。
- `node_modules/`、`dist/`、Flutter build output 和 Gradle build output 不應提交。
- 目前後端密碼欄位名稱為 `hashed_password`，部分 API 直接接收此欄位；正式環境應統一改成接收明文密碼後在後端雜湊。
- `backend/app/core/database.py` 會在啟動時建立資料表並確保 trigger 存在。
- Flutter App 內含 `.tflite` 模型，若模型檔過大，正式協作時可考慮改用 Git LFS。
