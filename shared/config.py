"""
Authentification :
Définir `GOOGLE_API_GENERATIVE_KEY`, `GOOGLE_API_GEO_MAPS_KEY`, `GOOGLE_PROJECT_ID` et `TAVILY_API_KEY` dans `.env` à la racine du projet
"""

import os
from pathlib import Path

from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field


ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env", override=True)
google_api_generative_key = os.getenv("GOOGLE_API_GENERATIVE_KEY", os.getenv("GOOGLE_API_GENERATIVE", "")).strip()
google_api_geo_maps_key = os.getenv("GOOGLE_API_GEO_MAPS_KEY", os.getenv("GOOGLE_API_GEO_MAPS", "")).strip()
google_project_id = os.getenv("GOOGLE_PROJECT_ID", "").strip()
tavily_api_key = os.getenv("TAVILY_API_KEY", "").strip()


class ProjectSettings(BaseModel):
    model_config = ConfigDict(validate_default=True)

    # Clé API pour Gemini / Generative Language API (nécessaire pour tous les TPs)
    google_api_generative_key: str = Field(default=google_api_generative_key, min_length=1)

    # Clé API pour Google Maps (Geo Maps et Tavily requis uniquement en TP3)
    google_project_id: str = Field(default=google_project_id)
    google_api_geo_maps_key: str = Field(default=google_api_geo_maps_key)
    tavily_api_key: str = Field(default=tavily_api_key)

    # Paramètres pour le LLM et l'agent
    llm_model_name: str = "gemini-2.5-flash-lite"
    llm_temperature: float = Field(default=0.4, ge=0.0, le=2.0)
    llm_top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    llm_top_k: int = Field(default=40, ge=1)
    llm_max_output_tokens: int = Field(default=5000, ge=512)
    llm_thinking_budget: int = Field(default=1000, ge=0)

    # Paramètres pour le RAG (génération augmentée par récupération)
    rag_embedding_model_name: str = "gemini-embedding-001"

    # Paramètres pour le LLM local et la vectorisation (LMStudio ou Ollama, compatibles OpenAI)
    local_llm_base_url: str = "http://localhost:1234/v1"
    local_llm_model_name: str = "local-model"
    local_embedding_model_name: str = "local-embedding-model"


project_settings = ProjectSettings()

genai_client = genai.Client(
    api_key=project_settings.google_api_generative_key,
)
