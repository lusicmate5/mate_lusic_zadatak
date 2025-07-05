# 🎟️ TicketHub – FastAPI servis za tickete

**TicketHub** je jednostavan FastAPI servis za pregled i analizu ticketa. Omogućuje autentikaciju, dohvat ticketa s filtrima i pretragom, statistiku, keširanje i zaštitu putem rate limita.

---

## 🚀 Tehnologije

- **FastAPI** – web framework
- **Redis** – keširanje podataka (s fallbackom na in-memory cache)
- **slowapi** – rate limiting
- **Pytest** – testiranje
- **Docker & Docker Compose** – kontejnerizacija
- **GitHub Actions** – CI/CD

---

## 📦 Instalacija

### Lokalno pokretanje

1. Kloniraj repozitorij:

   ```bash
   git clone https://github.com/lusicmate5/mate_lusic_zadatak.git
   cd mate_lusic_zadatak
   ```

2. Kreiraj virtualno okruženje i instaliraj ovisnosti:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Pokreni aplikaciju:

   ```bash
   uvicorn src.main:app --reload
   ```

### Docker pokretanje

```bash
docker-compose up --build
```

Aplikacija će biti dostupna na 👉 `http://localhost:8000/docs`

---

## 🧪 Testiranje

Pokreni sve testove:

```bash
pytest -v
```

---

## 🔐 Autentikacija

- Endpoint: `POST /auth/login`
- Prijava preko DummyJSON API-ja
- Vraća JWT token (dummy)

---

## 📚 Endpointi

| Metoda | Ruta            | Opis                                 |
|--------|-----------------|--------------------------------------|
| POST   | `/auth/login`   | Prijava korisnika                    |
| GET    | `/tickets`      | Lista ticketa s filtrima i pretragom |
| GET    | `/tickets/{id}` | Detalji ticketa                      |
| GET    | `/stats`        | Statistika po statusima/prioritetima |
| GET    | `/health`       | Provjera statusa API-ja              |

---

## 🧠 Caching (Redis)

**Keširani endpointi:**

- `GET /tickets` – bazirano na parametrima
- `GET /tickets/{id}`
- `GET /stats`

**Vrijeme isteka:** 60 sekundi

Ako Redis nije dostupan, koristi se lokalni (in-memory) cache.

---

## 🦃 Rate Limiting

- `POST /auth/login` → max **5 zahtjeva u 60 sekundi**
- `GET /tickets*` → max **10 zahtjeva u 60 sekundi**

Rate limiting se temelji na IP adresi (`X-Forwarded-For` header).

---

## 📄 Logging

Logiranje je omogućeno putem Python `logging` modula:

- INFO logovi za uspješne zahtjeve
- ERROR logovi za iznimke i greške

Logovi se definiraju u `src/logger.py` i integrirani su u `main.py`, `auth.py` i `services.py`.

---

## 🩺 Health check

Endpoint: `GET /health`

```json
{
  "status": "ok",
  "redis": "available/unavailable"
}
```

---

## ⚙️ CI/CD

- Automatizirano testiranje putem **GitHub Actions**
- Dockerfile + `docker-compose.yml` uključuju:
  - aplikaciju
  - Redis

---

## 🐳 Docker

Pokreni sve servise (API + Redis) preko Docker Compose:

```bash
docker-compose up --build
```

Aplikacija će biti dostupna na:
👉 http://localhost:8000/docs

---

## ⚡ Windows skripte (.bat)

Za jednostavno lokalno pokretanje na Windowsu dostupne su `.bat` skripte:

| Skripta       | Opis                                               |
|---------------|----------------------------------------------------|
| `install.bat` | Kreira virtualno okruženje i instalira ovisnosti   |
| `test.bat`    | Pokreće testove pomoću `pytest -v`                 |
| `docker.bat`  | Pokreće aplikaciju u Dockeru                       |

✅ Primjeri:

```bash
install.bat
test.bat
docker.bat
```

**Napomena:** Skripte su prilagođene PowerShellu ili CMD-u. Ako koristiš Git Bash, preporuča se ručno pokretanje komandi.

---

## 📘 Bonus: statička HTML dokumentacija (Redoc)

Uz OpenAPI shemu (`/openapi.json`), moguće je generirati statičku HTML dokumentaciju koristeći Redoc.

### 📄 Generiranje dokumentacije

Instaliraj alat ako već nisi:

```bash
npm install -g @redocly/cli
```

Preuzmi OpenAPI JSON iz aplikacije:

👉 Pokreni aplikaciju (npr. `uvicorn`) i otvori u pregledniku:
[http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

Spremi sadržaj kao `openapi.json` u root projekta.

Generiraj statički HTML:

```bash
npx @redocly/cli build-docs openapi.json -o docs/redoc-static.html
```

Otvaranje:
👉 Dvaput klikni `docs/redoc-static.html` ili ga otvori u pregledniku.

---

🎉 Hvala na čitanju! Za dodatna pitanja ili prijedloge, slobodno me kontaktirajte.

📬 Autor: Mate Lušić

