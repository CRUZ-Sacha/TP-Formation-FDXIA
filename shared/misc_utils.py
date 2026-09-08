"""Utilitaires génériques pour écrire des JSON et parser du texte"""

import json
from pathlib import Path


def write_json_file(file_path: str | Path, data: dict[str, object]) -> None:
    """Écrire un dictionnaire JSON formaté, en créant le dossier parent si nécessaire"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
