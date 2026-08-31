from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from google.genai import types

from shared.config import genai_client, project_settings


class LLMRequest(BaseModel):
    """Format d'entrée d'un appel LLM

    Champs
    - system_prompt : consigne système optionnelle
    - user_prompt : prompt utilisateur obligatoire
    """
    system_prompt: str | None = None
    user_prompt: str = Field(min_length=1)


class LLMResponse(BaseModel):
    """Format de sortie d'un appel LLM

    Champs
    - output : texte final du modèle
    - input_tokens : nombre de tokens d'entrée
    - output_tokens : nombre de tokens de sortie
    - total_tokens : total des tokens
    - raw_response : réponse brute du fournisseur pour débogage
    """
    output: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    raw_response: dict[str, object]


async def run_llm(request: LLMRequest) -> LLMResponse:
    # TODO : Copier la fonction après l'avoir codée dans le notebook
    raise NotImplementedError("Copiez votre implementation depuis le notebook TP1_1")


async def run_llm_structured(request: LLMRequest, response_schema: type[BaseModel]) -> LLMResponse:
    # TODO : Copier la fonction après l'avoir codée dans le notebook
    raise NotImplementedError("Copiez votre implementation depuis le notebook TP1_1")


# ------ LLM LOCAL ------

local_llm_client = AsyncOpenAI(
    base_url=project_settings.local_llm_base_url,
    api_key="not-needed",
)


async def run_llm_local(request: LLMRequest) -> LLMResponse:
    """Exécuter un appel LLM sur un modèle local (LMStudio ou Ollama)

    Utilise l'API compatible OpenAI exposée par LMStudio ou Ollama.
    Changer `local_llm_base_url` et `local_llm_model_name` dans `shared/config.py`.

    Entrée
    - request : `LLMRequest` (`system_prompt`, `user_prompt`)

    Sortie
    - `LLMResponse` avec texte, métriques tokens et réponse brute
    """
    # TODO : Implémenter cette variante si vous êtes intéressé par lancer un LLM en local
    raise NotImplementedError("Fonction optionnelle non implémentée")


async def run_llm_local_structured(request: LLMRequest, response_schema: type[BaseModel]) -> LLMResponse:
    """Exécuter un appel LLM local avec sortie structurée (JSON conforme à response_schema)

    Utilise l'API compatible OpenAI exposée par LMStudio ou Ollama.
    Changer `local_llm_base_url` et `local_llm_model_name` dans `shared/config.py`.

    Entrée
    - request : `LLMRequest` (`system_prompt`, `user_prompt`)
    - response_schema : modèle Pydantic décrivant le JSON attendu

    Sortie
    - `LLMResponse` avec texte (JSON valide), métriques tokens et réponse brute
    """
    # TODO : Implémenter cette variante si vous êtes intéressé par lancer un LLM en local
    raise NotImplementedError("Fonction optionnelle non implémentée")


