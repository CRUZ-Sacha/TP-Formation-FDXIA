# Mode Opératoire : Installation et vérification du projet

## 1. Prérequis système

> **Recommandation** : macOS ou Linux sont fortement conseillés. Windows est supporté mais moins bien intégré (notamment pour les environnements virtuels et certaines dépendances), des frictions supplémentaires sont à prévoir.

> **Note** : ce document utilise `python` dans ses commandes. Sur macOS/Linux, vous pouvez aussi utiliser `python3` selon votre installation.

### 1.1 Python

Python exécute le code du projet (notebooks, scripts).

**macOS / Linux** :
```bash
brew install python@3.12
python --version
```

**Windows** (PowerShell) :
```powershell
winget install --id Python.Python.3.12 -e
python --version
```

### 1.2 git

git clone le dépôt et gère le changement de branche entre les TPs.

**macOS / Linux** :
```bash
brew install git
git --version
```

**Windows** (PowerShell) :
```powershell
winget install --id Git.Git -e --source winget
git --version
```

### 1.3 uv

uv crée l'environnement virtuel et installe les dépendances Python du projet.

**macOS / Linux** :
```bash
brew install uv
uv --version
```

**Windows** (PowerShell) :
```powershell
winget install --id astral-sh.uv -e
uv --version
```

---

## 2. Configurer l'environnement

### 2.1 Fichier `.env`

Créer le fichier de configuration (les clés vous seront transmises le jour de la formation) :

```bash
cp .env.example .env
```

### 2.2 Environnement Python

**macOS / Linux** :
```bash
uv venv .venv
source .venv/bin/activate
uv sync
```

**Windows** (PowerShell) :
```powershell
uv venv .venv
.venv\Scripts\Activate.ps1
uv sync
```

---

## 3. Sélectionner le kernel dans l'IDE

Au lancement d'un notebook, sélectionner le kernel `.venv` (Python du projet).

Si `.venv` n'apparaît pas :
1. Vérifier que `uv venv .venv` a bien été exécuté.
2. Redémarrer l'IDE.
3. Ajouter manuellement : `uv run python -c "import sys; print(sys.executable)"` puis copier ce chemin dans les paramètres Jupyter.

Une fois le kernel sélectionné, ouvrir `TP1_travel_planner_LLM/1_1_llm_assistant.ipynb` et exécuter la première cellule (imports) pour vérifier que le kernel et les dépendances sont bien reconnus.

---

## 4. Vérification de la connectivité aux APIs

Ces commandes permettent de vérifier que les endpoints externes sont joignables **sans clé API**.
Un code HTTP `400/401/403` en réponse signifie que le réseau fonctionne : c'est la clé qui est attendue.

### 4.1 Open-Meteo (météo, gratuit, sans clé)

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&daily=temperature_2m_max&timezone=auto&forecast_days=2"
```

Résultat attendu (`200 OK`) :
```json
{"latitude":48.84,"longitude":2.3599997,"generationtime_ms":0.02,"utc_offset_seconds":7200,"timezone":"Europe/Paris","timezone_abbreviation":"GMT+2","elevation":46.0,"daily_units":{"time":"iso8601","temperature_2m_max":"°C"},"daily":{"time":["2026-08-31","2026-09-01"],"temperature_2m_max":[23.5,23.8]}}
```

### 4.2 Google Generative AI (Gemini)

```bash
curl -s -w "\nHTTP %{http_code}\n" \
  -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"hello"}]}]}'
```

Résultat attendu : `HTTP 403`, `"status": "PERMISSION_DENIED"` (endpoint joignable, clé manquante).

### 4.3 Tavily (recherche web)

```bash
curl -s -w "\nHTTP %{http_code}\n" \
  -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}'
```

Résultat attendu : `HTTP 401`, `"error": "Unauthorized: missing or invalid API key."` (endpoint joignable, clé manquante).

### 4.4 Google Maps Geocoding

```bash
curl -s -w "\nHTTP %{http_code}\n" \
  "https://maps.googleapis.com/maps/api/geocode/json?address=Paris"
```

Résultat attendu : `HTTP 200`, `"status": "REQUEST_DENIED"` (endpoint joignable, clé manquante).

### 4.5 LLM local (LM Studio / Ollama), optionnel

```bash
curl -s "http://localhost:1234/v1/models" | python -c "import sys,json; d=json.load(sys.stdin); [print(m['id']) for m in d.get('data',[])]"
```

Résultat attendu : liste des modèles chargés.
Si aucune réponse : LM Studio n'est pas démarré (normal si vous utilisez le mode cloud).

---

## 5. Vérification complète en une seule commande

Ce bloc est écrit en syntaxe bash (macOS/Linux). Sous Windows, exécutez plutôt les commandes de la section 4 une par une dans PowerShell (`curl` y est disponible nativement depuis Windows 10).

```bash
echo "=== open-meteo ===" && \
curl -s -o /dev/null -w "HTTP %{http_code}\n" "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&daily=temperature_2m_max&timezone=auto&forecast_days=2" && \
echo "=== Google Generative AI ===" && \
curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"hello"}]}]}' && \
echo "=== Tavily ===" && \
curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST "https://api.tavily.com/search" -H "Content-Type: application/json" -d '{"query":"test"}' && \
echo "=== Google Maps ===" && \
curl -s -o /dev/null -w "HTTP %{http_code}\n" "https://maps.googleapis.com/maps/api/geocode/json?address=Paris" && \
echo "=== LM Studio local ===" && \
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 3 "http://localhost:1234/v1/models" 2>/dev/null || echo "non démarré"
```

Résultats de référence (validés le 2026-04-13) :

| Service | Code attendu | Signification |
|---|---|---|
| open-meteo | `200` | Fonctionne sans clé |
| Google Generative AI | `403` | Endpoint joignable, clé requise |
| Tavily | `401` | Endpoint joignable, clé requise |
| Google Maps | `200` | Endpoint joignable, clé requise |
| LM Studio | `200` | Serveur local actif |

---

## 6. Configuration LLM local (optionnel)

Si vous souhaitez utiliser LM Studio ou Ollama à la place de l'API Gemini :

1. Démarrer LM Studio et charger un modèle.
2. Dans `shared/config.py`, adapter si besoin :
   ```python
   local_llm_base_url: str = "http://localhost:1234/v1"
   local_llm_model_name: str = "local-model"
   local_embedding_model_name: str = "local-embedding-model"
   ```
3. Dans les notebooks ou utilitaires, basculer sur les fonctions `_local` (ex: `rag_embed_text_batch_local`).

Exemple de modèles chargés sur une machine de formateur (au 2026-04-13, à titre indicatif, les modèles disponibles dépendent de ce que vous avez téléchargé dans LM Studio/Ollama) :
- `qwen/qwen3-1.7b`
- `mistralai/ministral-3-14b-reasoning`
- `qwen/qwen3-4b-thinking-2507`
- `qwen/qwen3-vl-4b`
- `text-embedding-nomic-embed-text-v1.5` (embeddings)
