from pydantic import BaseModel, Field

from shared.config import ollama_client, project_settings


class LLMRequest(BaseModel):
    """TODO définir le format d'entrée d'un appel LLM TP1

    Champs
    - system_prompt : consigne système optionnelle
    - user_prompt : prompt utilisateur obligatoire
    """
    system_prompt: str | None = None
    user_prompt: str = Field(min_length=1)


class LLMResponse(BaseModel):
    """TODO définir le format de sortie normalisé de `run_llm`

    Champs
    - output : texte final du modèle
    - input_tokens : nombre de tokens d'entrée
    - output_tokens : nombre de tokens de sortie
    - total_tokens : total des tokens
    - raw_response : réponse brute du provider pour debug
    """
    output: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    raw_response: dict[str, object]


async def run_llm(request: LLMRequest) -> LLMResponse:
    """Exécuter un appel modèle unique via Ollama (réutilisable dans TP1).

    Entrée
    - request : `LLMRequest` (`system_prompt`, `user_prompt`)

    Sortie
    - `LLMResponse` avec texte, métriques tokens et réponse brute
    """
    messages: list[dict[str, str]] = []
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    messages.append({"role": "user", "content": request.user_prompt})

    response = await ollama_client.chat(
        model=project_settings.llm_model_name,
        messages=messages,
        options={
            "temperature": project_settings.llm_temperature,
            "top_p": project_settings.llm_top_p,
            "top_k": project_settings.llm_top_k,
            "num_predict": project_settings.llm_max_output_tokens,
        },
    )

    msg = response.get("message") or {}
    content = msg.get("content") or ""
    prompt_eval = response.get("prompt_eval_count") or 0
    eval_count = response.get("eval_count") or 0

    return LLMResponse(
        output=content,
        input_tokens=int(prompt_eval),
        output_tokens=int(eval_count),
        total_tokens=int(prompt_eval) + int(eval_count),
        raw_response=dict(response),
    )
