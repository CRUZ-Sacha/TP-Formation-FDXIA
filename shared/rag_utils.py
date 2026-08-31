"""Utilitaires RAG ordonnés par flux : charger -> découper -> vectoriser -> indexer -> rechercher"""

import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Callable, TypedDict

import chromadb
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
from tqdm import tqdm

from shared.config import genai_client, project_settings


CHROMA_MAX_BATCH_SIZE = 5000


class MarkdownDocument(TypedDict):
    source: str
    text: str


class RAGChunk:
    """Chunk RAG unique utilisé partout dans le pipeline

    Champs
    - source : fichier source du chunk
    - chunk_id : identifiant local au document source
    - text : contenu texte du chunk
    - char_count : longueur du texte
    - embedding : vecteur du chunk, initialisé à [0.0] tant qu'il n'est pas calculé
    """

    def __init__(
        self,
        source: str,
        chunk_id: int | str,
        text: str,
        embedding: list[float] | None = None,
    ) -> None:
        self.source: str = source
        self.chunk_id: int | str = chunk_id
        self.text: str = text
        self.char_count: int = len(text)
        self.embedding: list[float] = embedding if embedding is not None else [0.0]


def rag_load_markdown_documents(md_dir: Path) -> list[MarkdownDocument]:
    """Charger les documents Markdown depuis un dossier

    Entrées
    - md_dir : chemin du dossier contenant les fichiers `.md`

    Sortie
    - liste `list[MarkdownDocument]` avec
      - `source` : nom du fichier
      - `text` : contenu brut du fichier
    """
    md_files = sorted(md_dir.glob("*.md"))
    documents: list[MarkdownDocument] = []

    for file_path in md_files:
        text = file_path.read_text(encoding="utf-8")
        if text.strip():
            documents.append({"source": file_path.name, "text": text})

    return documents


def rag_chunk_document_by_chars(
    document: MarkdownDocument,
    chunk_chars: int = 100,
    chunk_overlap_chars: int = 20,
) -> list[RAGChunk]:
    # TODO : Copier la fonction après l'avoir codée dans le notebook 2_1
    raise NotImplementedError("Copiez votre implémentation depuis le notebook 2_1")


def rag_chunk_markdown_document_by_headers(
    document: MarkdownDocument,
    min_chunk_chars: int = 10,
    max_chunk_chars: int = 100,
) -> list[RAGChunk]:
    # TODO : Copier la fonction après l'avoir codée dans le notebook 2_3
    raise NotImplementedError("Copiez votre implémentation depuis le notebook 2_3")


def rag_describe_chunks(chunks: list[RAGChunk]) -> None:
    """Afficher des statistiques de taille et la distribution des chunks par document source

    Entrées
    - chunks : liste de `RAGChunk`
    """
    chunk_lengths = [chunk.char_count for chunk in chunks]
    chunk_array = np.array(chunk_lengths)

    print(f"Nombre de chunks : {len(chunks)}")
    print(f"Taille min/moy/max (caractères) : {chunk_array.min()} / {chunk_array.mean():.0f} / {chunk_array.max()}")

    chunks_per_source = Counter(chunk.source for chunk in chunks)

    fig, (axis_lengths, axis_sources) = plt.subplots(1, 2, figsize=(12, 4))

    axis_lengths.hist(chunk_lengths, bins=30)
    axis_lengths.set_title("Distribution des tailles de chunks")
    axis_lengths.set_xlabel("Caractères")
    axis_lengths.set_ylabel("Nombre de chunks")

    axis_sources.bar(chunks_per_source.keys(), chunks_per_source.values())
    axis_sources.set_title("Chunks par document source")
    axis_sources.tick_params(axis="x", rotation=90)

    fig.tight_layout()
    plt.show()


def rag_embed_text_batch(texts: list[str]) -> list[list[float]]:
    # TODO : Copier la fonction après l'avoir codée dans le notebook 2_1
    raise NotImplementedError("Copiez votre implémentation depuis le notebook 2_1")


def rag_embed_all_chunks(
    chunks: list[RAGChunk],
    batch_size: int = 16,
    embed_fn: Callable[[list[str]], list[list[float]]] = rag_embed_text_batch,
) -> list[RAGChunk]:
    # TODO : Copier la fonction après l'avoir codée dans le notebook 2_1
    raise NotImplementedError("Copiez votre implémentation depuis le notebook 2_1")


def rag_index_chunks_chroma(persist_dir: Path, chunks: list[RAGChunk]) -> None:
    # TODO : Copier la fonction après l'avoir codée dans le notebook 2_1
    raise NotImplementedError("Copiez votre implémentation depuis le notebook 2_1")


class RAGAssistant:
    def __init__(self):
        # TODO : Copier la classe après l'avoir codée dans le notebook 2_2
        raise NotImplementedError("Copiez votre implémentation depuis le notebook 2_2")


def rag_deduplicate_and_sort_chunks(
    chunks_with_scores: list[tuple[RAGChunk, float]],
) -> list[tuple[RAGChunk, float]]:
    """Dédupliquer les résultats par (source, chunk_id) puis trier par score décroissant"""
    best_chunks: dict[tuple[str, str], tuple[RAGChunk, float]] = {}

    for chunk, score in chunks_with_scores:
        key = (chunk.source, str(chunk.chunk_id))
        existing = best_chunks.get(key)
        if existing is None or score > existing[1]:
            best_chunks[key] = (chunk, score)

    return sorted(best_chunks.values(), key=lambda item: item[1], reverse=True)


# ------ EMBEDDINGS LOCAUX (OPTIONNEL) ------

local_embedding_client = OpenAI(
    base_url=project_settings.local_llm_base_url,
    api_key="not-needed",
)


def rag_embed_text_batch_local(texts: list[str]) -> list[list[float]]:
    # Fonction optionnelle : utiliser un modèle local (LMStudio ou Ollama)
    raise NotImplementedError("Fonction optionnelle non implémentée")


def rag_embed_all_chunks_local(chunks: list[RAGChunk], batch_size: int = 16) -> list[RAGChunk]:
    # Fonction optionnelle : variante locale de `rag_embed_all_chunks`
    raise NotImplementedError("Fonction optionnelle non implémentée")
