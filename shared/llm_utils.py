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
    """Exécuter un appel LLM

    Entrée
    - request : `LLMRequest` (`system_prompt`, `user_prompt`)

    Sortie
    - `LLMResponse` avec texte, métriques tokens et réponse brute
    """
    config = types.GenerateContentConfig(
        temperature=project_settings.llm_temperature,
        top_p=project_settings.llm_top_p,
        top_k=project_settings.llm_top_k,
        max_output_tokens=project_settings.llm_max_output_tokens,
        thinking_config=types.ThinkingConfig(
            thinking_budget=project_settings.llm_thinking_budget
        ),
        system_instruction=request.system_prompt,
    )

    response = await genai_client.aio.models.generate_content(
        model=project_settings.llm_model_name,
        contents=request.user_prompt,
        config=config,
    )

    usage_metadata = response.usage_metadata

    return LLMResponse(
        output=response.text,
        input_tokens=int(usage_metadata.prompt_token_count),
        output_tokens=int(usage_metadata.candidates_token_count),
        total_tokens=int(usage_metadata.total_token_count),
        raw_response=response.model_dump(mode="json"),
    )


async def run_llm_structured(request: LLMRequest, response_schema: type[BaseModel]) -> LLMResponse:
    """Exécuter un appel LLM avec sortie structurée (JSON garanti conforme à response_schema)

    Entrée
    - request : `LLMRequest` (`system_prompt`, `user_prompt`)
    - response_schema : modèle Pydantic décrivant le JSON attendu

    Sortie
    - `LLMResponse` avec texte (JSON valide), métriques tokens et réponse brute
    """
    config = types.GenerateContentConfig(
        temperature=project_settings.llm_temperature,
        top_p=project_settings.llm_top_p,
        top_k=project_settings.llm_top_k,
        max_output_tokens=project_settings.llm_max_output_tokens,
        thinking_config=types.ThinkingConfig(
            thinking_budget=project_settings.llm_thinking_budget
        ),
        system_instruction=request.system_prompt,
        response_mime_type="application/json",
        response_schema=response_schema,
    )

    response = await genai_client.aio.models.generate_content(
        model=project_settings.llm_model_name,
        contents=request.user_prompt,
        config=config,
    )

    usage_metadata = response.usage_metadata

    return LLMResponse(
        output=response.text,
        input_tokens=int(usage_metadata.prompt_token_count),
        output_tokens=int(usage_metadata.candidates_token_count),
        total_tokens=int(usage_metadata.total_token_count),
        raw_response=response.model_dump(mode="json"),
    )

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
    messages = []
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    messages.append({"role": "user", "content": request.user_prompt})

    response = await local_llm_client.chat.completions.create(
        model=project_settings.local_llm_model_name,
        messages=messages,
        temperature=project_settings.llm_temperature,
        max_tokens=project_settings.llm_max_output_tokens,
    )

    usage = response.usage
    return LLMResponse(
        output=response.choices[0].message.content,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
        raw_response=response.model_dump(),
    )


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
    messages = []
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    messages.append({"role": "user", "content": request.user_prompt})

    response = await local_llm_client.chat.completions.create(
        model=project_settings.local_llm_model_name,
        messages=messages,
        temperature=project_settings.llm_temperature,
        max_tokens=project_settings.llm_max_output_tokens,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": response_schema.__name__,
                "schema": response_schema.model_json_schema(),
            },
        },
    )

    usage = response.usage
    return LLMResponse(
        output=response.choices[0].message.content,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
        raw_response=response.model_dump(),
    )
