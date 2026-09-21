from mcp.server.fastmcp import FastMCP

from shared.config import ROOT_DIR
from shared.rag_utils import RAGAssistant, rag_embed_text_batch


DEFAULT_TOP_K = 5
MCP_SERVER_NAME = "travel-tools-local"
RAG_VECTOR_DB_DIR = ROOT_DIR / "TP2_travel_planner_RAG" / "data" / "chroma_db_rag_v2"

mcp = FastMCP(name=MCP_SERVER_NAME)

RAG_ASSISTANT: RAGAssistant | None = None


def get_rag_assistant() -> RAGAssistant:
    """Chargement paresseux de l'assistant RAG : instancié à la première utilisation"""
    global RAG_ASSISTANT
    if RAG_ASSISTANT is None:
        RAG_ASSISTANT = RAGAssistant(persist_dir=RAG_VECTOR_DB_DIR, embed_fn=rag_embed_text_batch)
    return RAG_ASSISTANT


@mcp.tool(name="rag_search")
def rag_search(query: str, top_k: int = DEFAULT_TOP_K) -> list[dict[str, object]]:
    """Récupérer les chunks RAG locaux les plus pertinents

    Entrées
    - query : requête texte
    - top_k : nombre maximal de chunks retournés

    Sortie
    - liste d'objets : source, chunk_id, text, score
    """
    rag_assistant = get_rag_assistant()
    chunks_with_scores = rag_assistant.search(query, top_k)
    return [
        {
            "source": chunk.source,
            "chunk_id": chunk.chunk_id,
            "text": chunk.text,
            "score": score,
        }
        for chunk, score in chunks_with_scores
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
