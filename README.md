# API Steam + Postagens (Fase 3 - SendGrid)

## Setup local (sem Docker)

1. Crie e ative um virtualenv
   - Windows: `python -m venv venv` → `venv\\Scripts\\activate`

2. Copie `.env.example` para `.env` e preencha suas chaves (SECRET_KEY, SENDGRID_API_KEY, MAIL_FROM)

3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Garanta que o PostgreSQL está rodando localmente e acessível pela variável `DATABASE_URL`.

5. Rode a API:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Acesse a documentação: http://localhost:8000/docs

## Teste rápido
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/forgot-password` (recebe e-mail via SendGrid)
- `POST /api/auth/reset-password`
