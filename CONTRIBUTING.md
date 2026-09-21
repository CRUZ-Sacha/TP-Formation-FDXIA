# Guide de contribution

Ce document s'adresse à celles et ceux qui maintiennent ou font évoluer ce dépôt (formateurs), pas aux apprenant·e·s. Pour suivre le TP, voir `README.md` et `mode_op.md`.

**Convention de nommage** : par souci de concision, `TP1_travel_planner_LLM` est raccourci en `TP1`, `TP2_travel_planner_RAG` en `TP2`, `TP3_travel_planner_Agent` en `TP3`. Un même nom (`TP1`, `TP2`, `TP3`) désigne à la fois une branche et un dossier du dépôt : le contexte précise toujours lequel des deux est concerné (ex. "sur la branche `TP2`" contre "le dossier `TP2/`").

---
## 1. Architecture des branches et checkpoints

4 branches sur le dépôt **GitLab (`origin`)**, seul dépôt de travail :

| Branche | Rôle |
|---|---|
| `dev` | Solutions complètes (référence) |
| `TP1` | Branche apprenant·e, checkpoint TP1 |
| `TP2` | Branche apprenant·e, checkpoint TP2 |
| `TP3` | Branche apprenant·e, checkpoint TP3 |

Le dépôt **GitHub (`github`)** sert uniquement à partager le projet à un public externe. Il ne contient que le dernier commit et se met à jour à partir du code du dépôt GitLab. On ne code jamais pour GitHub, c'est juste une copie.

**Règle de cohérence entre branches** : sur la branche `TPN` (N = 1, 2 ou 3), les dossiers des TP précédents doivent être des copies exactes de `dev` (solution complète). Seul le dossier `TPN`, celui du TP en cours, contient du code inachevé à compléter par l'apprenant·e (repéré par des `# TODO`, avec `raise NotImplementedError` là où il manque une fonction entière). Ça permet à un·e apprenant·e de faire son TP sans être bloqué·e par un TP précédent.

Concrètement :
- Sur la branche `TP2` : le dossier `TP1/` est une copie exacte de `TP1/` sur `dev` (solution complète), et seul le dossier `TP2/` contient du code à compléter.
- Sur la branche `TP3` : les dossiers `TP1/` et `TP2/` sont des copies exactes de `dev`, et seul le dossier `TP3/` contient du code à compléter.
- Le dossier `shared/` correspond toujours à la version de `dev`, sauf les fonctions du TP en cours qui redeviennent du code à compléter (à copier depuis les notebooks).

---
## 2. Le dossier `shared/` : à quoi sert chaque script

| Fichier | Rôle |
|---|---|
| `config.py` | Charge les clés API et les paramètres LLM depuis `.env`. |
| `llm_utils.py` | Fonctions d'appel au LLM (cloud et local). |
| `misc_utils.py` | Petites fonctions utilitaires (écriture JSON, extraction JSON depuis une sortie LLM). |
| `rag_utils.py` | Pipeline RAG complet : chargement des documents, chunking, embeddings, indexation et recherche. |
| `agent_tools.py` | Les outils utilisables par l'agent du TP3 (date, géolocalisation, météo, RAG, recherche web). |
| `agent_utils.py` | Fonctions pour exécuter l'agent et suivre son exécution en temps réel. |

Ces modules sont la version "solution" (branche `dev`). Sur la branche `TPN`, seules les fonctions du TP en cours redeviennent du code à compléter.

---
## 3. Conventions à respecter en éditant un TODO ou du code à compléter

### 3.1 Commentaire DOC sous un TODO

Quand un `# TODO` (dans un notebook apprenant·e) nécessite de chercher une API/classe/fonction externe, ajouter juste en dessous :

```python
# TODO : <ce qu'il faut faire>
# DOC (<NomDeLaClasseOuFonction>) : <lien>
```

Règles :
- Une ligne DOC par élément externe distinct à chercher.
- Le lien doit être le plus précis possible (ancre ciblée plutôt que dump complet du module) et vérifié avant d'être ajouté.
- Ne pas ajouter de DOC pour un élément trivial et déjà connu de Python.
- Ne pas répéter la même DOC/explication deux fois dans le même notebook, ni entre notebooks (renvoyer vers le TP précédent).

### 3.2 Pas de TODO sans vrai trou à remplir

Ne jamais mettre `# TODO` au-dessus d'un code déjà entièrement écrit (sans `...` à compléter). Soit c'est un vrai exercice (avec des `...`), soit ce n'est pas un exercice (l'indiquer clairement, ex. "rien à coder ici").

### 3.3 Format du code à compléter dans `shared/*.py`

Chaque fonction que l'apprenant·e doit coder elle-même/lui-même reste réduite à sa signature, sans docstring dupliquant le contrat du notebook :

```python
def some_function(args...) -> ReturnType:
    # TODO : Copier la fonction après l'avoir codée dans le notebook N_X
    raise NotImplementedError("Copiez votre implementation depuis le notebook N_X")
```

Le contrat détaillé (entrées/sortie) vit uniquement dans le notebook, jamais dans `shared/`.

### 3.4 Quoi laisser en exercice, quoi donner tout fait

- **Algorithme réel** (logique à concevoir soi-même) : vrai exercice, indices minimaux, l'apprenant·e doit trouver sa propre approche.
- **Plomberie technique** (configuration ou intégration d'une API tierce, sans contenu algorithmique) : donnée entièrement, pas de TODO.
- **Prompt engineering / choix de design** : vrai exercice, ça demande du jugement, pas de code technique.
- Préférer des éléments indépendants et explicites d'un cas d'usage à l'autre, plutôt que des éléments dérivés mécaniquement d'un cas précédent, pour forcer la réflexion plutôt que la copie.

---
## 4. Comment travailler sur le dépôt

Pour l'installation et l'environnement, suivre `README.md` (section I) et `mode_op.md`, identiques pour un formateur et un·e apprenant·e.

Pour modifier une solution, se positionner sur `dev`. Pour modifier le code à compléter d'un TP, se positionner sur la branche `TPN` correspondante et vérifier ensuite que la règle de cohérence de la section 1 est respectée (les TP précédents doivent rester identiques à `dev`).

Le dossier `devtools/` contient deux scripts pour ça, à lancer depuis la racine du dépôt.

### 4.1 Propager un changement de `dev` vers les branches `TPN`

Script : `devtools/git cherry pick all branches`

Il prend le dernier commit de `dev` (ou un autre commit/branche via `--source-branch`/`--source-commit`), regarde quels fichiers ont changé, et pour chaque branche `TP1`, `TP2`, `TP3` : si le fichier existe déjà sur cette branche, il en recopie le contenu tel quel depuis `dev` et commit. Il ignore les fichiers absents de la branche cible.

```bash
bash "devtools/git cherry pick all branches" --dry-run   # aperçu, rien n'est modifié
bash "devtools/git cherry pick all branches"              # applique et commit
```

**Attention** : le script recopie le contenu tel quel, il ne fait pas la conversion solution → code à compléter. Si le fichier modifié fait partie du TP en cours sur la branche cible (donc censé rester un exercice), le script écrase le code à compléter par la solution complète. Dans ce cas, après le script, il faut réadapter ce fichier à la main (ou avec un agent de code) selon les conventions de la section 3, avant de committer pour de bon.

### 4.2 Publier les branches (GitLab et GitHub)

Script : `devtools/git push all`

Pour `dev`, `TP1`, `TP2`, `TP3` : pousse l'historique complet vers GitLab (`origin`, `--force-with-lease`), puis crée un commit unique (squash de tout l'historique) et le pousse en forçant vers GitHub (`github`). C'est pour ça que le dépôt GitHub n'affiche jamais qu'un seul commit par branche.

```bash
bash "devtools/git push all"
```

**Attention** : ce script force-push à chaque fois, y compris sur GitHub où il réécrit l'historique en entier. Ne le lancer que quand tout est prêt à être publié.
