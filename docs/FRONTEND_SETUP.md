# Frontend Setup Guide

## Prerequisites

- **Node.js** 18+ (LTS recommended)
- **npm** 9+ (ships with Node 18)

Verify your versions:

```bash
node -v   # v18.x.x or higher
npm -v    # 9.x.x or higher
```

---

## Installation

```bash
cd frontend
npm install
```

This installs all dependencies listed in `package.json`, including React, TailwindCSS,
TypeScript, and React Query.

---

## Development

Start the development server with hot reload:

```bash
npm start
```

The app opens at **http://localhost:3000**.

### Hot Reload

The development server supports **hot module replacement** (HMR). Any change you save
in `src/` is reflected instantly in the browser — no manual refresh needed.

---

## Production Build

Generate an optimized production bundle:

```bash
npm run build
```

Output is written to `frontend/build/`. This directory is what the Docker image
copies into the Nginx container.

---

## Environment Variables

Copy the example file and adjust values as needed:

```bash
cp .env.example .env
```

| Variable              | Default                          | Description                  |
|-----------------------|----------------------------------|------------------------------|
| `REACT_APP_API_URL`   | `http://localhost:8001`          | Dashboard API base URL       |
| `REACT_APP_WS_URL`    | `ws://localhost:8001/api/v2/dashboard/ws` | WebSocket endpoint  |

> **Note:** All custom environment variables must be prefixed with `REACT_APP_` so that
> Create React App includes them in the build.

---

## Running Tests

```bash
npm test
```

Tests use **Jest** and **React Testing Library**. Test files live in `frontend/__tests__/`.
