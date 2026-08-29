# Árbitro Asistente de Reglas

Agente de IA que resuelve cálculos de turnos y verifica reglas de redención de cartas para un juego
de estrategia, usando LangGraph para forzar tool-calling determinista en lugar de dejar que el LLM
"alucine" matemática.

Ver [`CLAUDE.md`](./CLAUDE.md) para el contexto arquitectónico completo (léelo antes de iterar con
Claude Code).

## Quick start

### Backend

```bash
cd backend
cp .env.example .env      # completar SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

### Tests

```bash
cd backend
pytest tests/ -v
```

## Estado del proyecto

Esqueleto inicial — estructura de carpetas, stubs y contratos definidos, sin lógica de negocio
implementada todavía. Ver la sección 8 de `CLAUDE.md` para el roadmap de implementación sugerido.

## Stack

- **IA**: Python + LangGraph (tool-calling, StateGraph)
- **Backend**: FastAPI
- **DB**: Supabase (Postgres)
- **Frontend**: Next.js + TypeScript + Tailwind, desplegado en Vercel
- **Infra**: Docker (backend)
