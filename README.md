# P1 · Call-log app

A tiny app that stores phone calls and lists them on a web page.
It's the "restaurant" from the FDE week 1 kickoff, built for real:

| Restaurant | Part | Folder | Runs on (deployed) |
|---|---|---|---|
| Dining room | **Frontend**: React page that lists the calls | `frontend/` | Vercel |
| Waiter | **API**: `GET /calls` and `POST /calls` | `backend/main.py` | Render |
| Kitchen | **Backend**: Python (FastAPI) | `backend/` | Render |
| Pantry | **Database**: Postgres table `calls` | `backend/schema.sql` | Neon |

```
curl / Postman ──POST /calls──▶  Python API (Render)  ──INSERT──▶  Postgres (Neon)
React page (Vercel) ──GET /calls──▶  Python API  ──SELECT──▶  Postgres
```

## What's in each file

```
backend/
  main.py           the API: two doors, GET /calls and POST /calls
  schema.sql        the table design (the API creates it automatically on start)
  requirements.txt  Python libraries Render must install
  .env.example      template for your secrets (the real .env never goes to GitHub)
frontend/
  index.html        the empty page React draws into
  src/App.jsx       asks the API for the calls and draws one row per call
  src/index.css     the looks
  .env.example      template: where the API lives (VITE_API_URL)
```

## 1 · Run it on your laptop

You need a database first. Easiest: create the Neon database (step 2a below), then put its
connection string in `backend/.env` (copy `backend/.env.example` to `backend/.env` and fill it in).

```bash
# Terminal 1: the API, at http://localhost:8000
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --reload
```

```bash
# Terminal 2: the page, at http://localhost:5173
cd frontend
cp .env.example .env        # VITE_API_URL=http://localhost:8000
npm install
npm run dev
```

Add a call, then press **Refresh** on the page:

```bash
curl -X POST http://localhost:8000/calls -H "Content-Type: application/json" -d '{"caller": "Asha", "summary": "Wants a loan"}'
```

## 2 · Put it online (all free plans, all your own accounts)

Do it in this order, starting from the back: database → API → page.
**Tip:** pick the **Singapore** region on both Neon and Render. They sit next to each other and close to
India, so every request is faster (that's the latency lesson from Part 2).

### 2a · Database on Neon
1. Sign up at neon.tech and create a project (region: AWS Asia Pacific, Singapore).
2. Click **Connect** and copy the **connection string** (it starts with `postgresql://`).
   It contains your database password: paste it only into `backend/.env` and Render's settings,
   never into code, GitHub, a chat or a screenshot.
3. Optional: open the **SQL Editor** and run `SELECT * FROM calls;` any time to look inside the pantry.
   (The table itself is created by the API the first time it starts.)

### 2b · API on Render
1. Sign up at render.com with your GitHub account.
2. **New → Web Service** → pick this repo.
3. Fill in:
   - **Root Directory:** `backend`
   - **Runtime / Language:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Region:** Singapore · **Instance type:** Free
   - **Environment Variables:** `DATABASE_URL` = your Neon connection string
4. Deploy. You get a link like `https://p1-call-log-xxxx.onrender.com`.
   Open it: you should see `{"status":"ok","try":"/calls"}`. Then open `/calls`: you should see `[]`.

### 2c · Page on Vercel
1. Sign up at vercel.com with your GitHub account.
2. **Add New → Project** → import this repo.
3. **Root Directory:** `frontend` (Vercel detects Vite by itself).
4. **Environment Variables:** `VITE_API_URL` = your Render link, with **no slash at the end**.
5. Deploy. You get a link like `https://p1-call-log-xxxx.vercel.app`.
   If you change `VITE_API_URL` later, press **Redeploy**: the address is baked in when the page is built.

## 3 · The "done when" test

```bash
curl -X POST https://YOUR-API.onrender.com/calls \
  -H "Content-Type: application/json" \
  -d '{"caller": "Asha", "summary": "Wants a loan for her shop"}'
```

You should get back `201` and the saved call with its new `id`. Open your Vercel page and press
**Refresh**: Asha is there. ✅

**Same thing in Postman:** New → HTTP request → method **POST** → URL `https://YOUR-API.onrender.com/calls`
→ **Headers**: `Content-Type: application/json` → **Body** → raw → JSON →
`{"caller": "Ravi", "summary": "Asked about interest rates"}` → **Send** → expect `201 Created`.

## When something breaks

| You see | Most likely cause | Fix |
|---|---|---|
| Page loads for up to a minute | Render's free server was asleep | Normal. Wait, then Refresh |
| "VITE_API_URL is not set" | Missing on Vercel | Add it in Vercel settings, then Redeploy |
| "Failed to fetch" | API link wrong, ends in `/`, or still `localhost` | Fix `VITE_API_URL`, then Redeploy |
| Render deploy fails with `KeyError: 'DATABASE_URL'` | Key missing on Render | Add it under Render → Environment |
| `422` from POST | Body missing `caller` or `summary` | Check your JSON |
| `404` | Wrong address (e.g. `/call` instead of `/calls`) | Check the URL |
| `500` | Something broke on the server | Read Render → Logs |

Works on your laptop but not online? Check two things first: a key missing from the host's settings,
or an address still pointing at `localhost`.

## What to submit (by Sunday of week 2)
- Link to this GitHub repo
- Live link to the React page (Vercel) and the API (Render)
- The curl command and the Postman request you used to add a call
- Before submitting: make sure no `.env` file or password is in the repo (`git status` should never show `.env`)
