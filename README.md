# TP - IA Générative : Prompt Engineering, RAG & Agents

L'objectif de ce TP est d'expérimenter différentes techniques d'IA générative (Prompt Engineering, RAG, Agents).

Au fil des notebooks, vous allez répondre au même use-case de différentes façons : **un assistant de planification de voyage**.

---
## I. Installation

### 1. Préparer la station de travail

Installer les outils système requis : Python, git et uv.

**Windows** : les commandes ci-dessous utilisent `winget`, l'outil officiel Microsoft. Il est installé par défaut sur **Windows 11**. Sur Windows 10, il faut avoir l'app "App Installer" à jour (disponible sur le Microsoft Store).

#### 1.1 Python

Installer Python 3.12 (version requise par le projet) :

**macOS / Linux** :
```bash
brew install python@3.12
```

**Windows** (PowerShell) :
```powershell
winget install --id Python.Python.3.12 -e
```

#### 1.2 git

Installer git (pour cloner le projet et gérer les versions) :

**macOS / Linux** :
```bash
brew install git
```

**Windows** (PowerShell) :
```powershell
winget install --id Git.Git -e --source winget
```

#### 1.3 uv

Installer uv (pour gérer l'environnement Python et les dépendances) :

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

Si `uv --version` ne fonctionne pas après l'installation, fermez et rouvrez votre terminal (PowerShell) pour recharger le PATH.

### 2. Cloner le projet et changer de branche

Cloner le dépôt et se positionner dans le dossier du projet (le nom du dossier créé dépend du nom du dépôt) :
```bash
git clone (lien du repository)
cd fdxia-formation-tp
```

Se positionner sur la branche du premier TP :
```bash
git switch TP1_travel_planner_LLM
git pull origin TP1_travel_planner_LLM
```

### 3. Configurer l'environnement de travail

Créer le fichier de configuration `.env` :
```bash
cp .env.example .env
```

Renseigner dans `.env` :
- `GOOGLE_API_GENERATIVE_KEY` (Gemini / Generative Language API)
- `GOOGLE_API_GEO_MAPS_KEY` (Google Maps Geocoding / Places)
- `GOOGLE_PROJECT_ID`
- `TAVILY_API_KEY`

**Les Clés d'API vous seront fournies par les formateurs**.

Si vous travaillez en autonomie :

> Pour l'obtention de votre clé API Gemini et la création de votre projet merci de vous rendre sur :
>https://aistudio.google.com/u/1/api-keys

>De même pour Tavily :
>https://www.tavily.com/

Créer l'environnement Python et installer les dépendances (dans cet ordre) :

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

Si PowerShell bloque l'activation (`execution of scripts is disabled`), lancez une fois :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Notebooks : choisir le bon kernel

Quand vous lancerez un notebook, votre IDE vous demandera de choisir un kernel (interpréteur Python). Sélectionnez celui de votre projet (`.venv`) pour que les dépendances soient correctement prises en compte.

Si `.venv` n'apparaît pas dans la liste des interpréteurs, assurez-vous d'avoir bien créé le dossier `.venv` et redémarrez votre IDE.

Si le notebook ne charge pas l'environnement virtuel, lancez `uv run python -c "import sys; print(sys.executable)"`, puis ajoutez ce chemin Python dans les parametres Jupyter.

---
## II. Parcours des TPs (ordre recommandé)

### 1. Liste des notebooks à traiter

**IMPORTANT** : Par souci de clarté, vous serez amené·e à coder des fonctions dans des fichiers externes `*.py` stockés dans le dossier `shared`.

| TP  | Thème                                                   | Notebook(s)                                                    | Utilitaires dans le dossier `shared` |
|-----|---------------------------------------------------------|----------------------------------------------------------------|---------------------------------------|
| 1.1 | Prompt Engineering                                      | `TP1_travel_planner_LLM/1_1_llm_assistant.ipynb`               | `config.py`<br>`llm_utils.py`<br>`misc_utils.py` |
| 1.2 | LLM as a Judge                                          | `TP1_travel_planner_LLM/1_2_llm_as_a_judge.ipynb`              | `llm_utils.py` |
| 2.1 | RAG - Préparer la base de données (version simple)      | `TP2_travel_planner_RAG/2_1_rag_db_preparation.ipynb`          | `config.py`<br>`rag_utils.py` |
| 2.2 | RAG - Assistant simple                                  | `TP2_travel_planner_RAG/2_2_rag_assistant_simple.ipynb`        | `config.py`<br>`llm_utils.py`<br>`rag_utils.py` |
| 2.3 | RAG - Préparer la base de données (version améliorée)   | `TP2_travel_planner_RAG/2_3_rag_db_improved_preparation.ipynb` | `config.py`<br>`rag_utils.py` |
| 2.4 | RAG - Assistant amélioré (Multi-Query, HyDE, reranking) | `TP2_travel_planner_RAG/2_4_rag_assistant_improved.ipynb`      | `config.py`<br>`llm_utils.py`<br>`rag_utils.py` |
| 3.1 | Agent IA outillé                                        | `TP3_travel_planner_Agent/3_1_tooling_assistant.ipynb`         | `config.py`<br>`agent_tools.py`<br>`agent_utils.py` |
| 3.2 | Agent MCP                                               | `TP3_travel_planner_Agent/3_2_mcp_assistant.ipynb`<br>`TP3_travel_planner_Agent/mcp_server.py` | `config.py`<br>`agent_utils.py`<br>`rag_utils.py` |



---
## III. Objectif de chaque partie

### TP1 - Prompt Engineering
- Faire un premier appel LLM
- Structurer la réponse avec un `system_prompt`
- Obtenir une sortie exploitable et industrialisable
- Utiliser un LLM pour évaluer automatiquement les réponses d'un autre LLM (LLM as a Judge)

### TP2 - RAG
- Construire une base vectorielle à partir des guides
- Récupérer les chunks pertinents pour une question utilisateur
- Générer une réponse ancrée sur les sources
- Techniques d'amélioration : Multi-Query, HyDE, Reranking

### TP3 - Agent IA
- Utiliser un agent qui choisit et enchaîne des outils
- Récupérer et combiner du contexte : date, géolocalisation, météo, recherche web et RAG
- Produire une réponse finale argumentée avec traces d'exécution
- Migrer les outils vers une architecture MCP (Model Context Protocol)


---
## IV. Comment faire ce TP ?

Lors du TP, positionnez-vous sur la branche correspondant au TP traité :
- `TP1_travel_planner_LLM`
- `TP2_travel_planner_RAG`
- `TP3_travel_planner_Agent`

```bash
git switch TPX_nom_du_TP
git pull origin TPX_nom_du_TP
```

Traitez ensuite le notebook correspondant en suivant les instructions et en complétant les parties indiquées (repérées par des `# TODO` ou `...`).

**IMPORTANT** : Chaque TP dépend des utilitaires (fichiers du dossier `shared`) développés dans les TPs précédents. *

En cas de blocage sur une fonction/classe pendant le TP, vous pouvez consulter la branche `dev` (solutions) pour débloquer et passer à la suite.

Si vous souhaitez réaliser certaines parties à votre manière, n'hésitez pas ! Suivre les questions du TP permet de faciliter la correction, mais vous êtes libre de procéder comme vous le souhaitez.

Bon Apprentissage !
