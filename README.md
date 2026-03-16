# start-sitebridge-fastapi

Full-stack boilerplate: FastAPI server + Vite React SPA client, designed for SiteBridge deployment.

## Stack

- **Server**: FastAPI with SQLite (WAL mode), served by uvicorn
- **Client**: React 19, React Router, Tailwind CSS v4, Vite 7
- **Deploy**: GitHub Actions CI/CD via SiteBridge

## Local Development

### Server (port 4001)

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4001
```

### Client (port 5173)

```bash
cd client
npm install
npm run dev
```

The client dev server proxies API calls to `http://localhost:4001` automatically via the `api.ts` helper.

## Production Build

```bash
cd client
npm run build
mkdir -p ../server/static
cp -r dist/* ../server/static/
```

Then run the server -- it serves the SPA from `server/static/`.

## Project Structure

```
client/          React SPA (Vite + Tailwind)
server/          FastAPI backend
  app/main.py    Application entry point
  data/          SQLite database (gitignored, created at runtime)
  static/        Client build output (gitignored, generated)
.github/         CI/CD workflow for SiteBridge
```
