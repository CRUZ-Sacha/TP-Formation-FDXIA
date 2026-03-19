import json
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.messages import FunctionToolCallEvent, FunctionToolResultEvent
from pydantic_ai.usage import UsageLimits


TRACE_SEPARATOR = "-" * 80


class EventStreamHandler:
    """Gestionnaire de flux pour journaliser les appels outils en temps réel

    Champs
    - `trace_lines` : tampon texte partagé avec l'appelant
    - `step` : compteur d'étapes

    Méthodes
    - `__call__` : consomme les événements et ajoute des blocs formatés
    """

    def __init__(self, trace_lines: list[str]):
        """Initialiser l'état du gestionnaire pour une exécution agent

        Entrées
        - trace_lines : liste utilisée pour accumuler la trace
        """
        self.trace_lines = trace_lines
        self.step = 1

    async def __call__(self, _run_context, event_stream) -> None:
        """Formater les événements d'appel outil et de résultat outil

        Entrées
        - _run_context : contexte d'exécution pydantic-ai
        - event_stream : flux asynchrone des événements modèle/outils
        """
        async for event in event_stream:
            match event:
                case FunctionToolCallEvent():
                    block = [
                        f"STEP {self.step} : TOOL CALL",
                        f"- tool : {event.part.tool_name}",
                        "- args :",
                        json.dumps(event.part.args_as_dict(), ensure_ascii=False, indent=2),
                        TRACE_SEPARATOR,
                    ]
                case FunctionToolResultEvent():
                    block = [
                        f"STEP {self.step} : TOOL RESULT",
                        f"- tool : {event.result.tool_name}",
                        "- output :",
                        json.dumps(event.result.content, ensure_ascii=False, indent=2),
                        TRACE_SEPARATOR,
                    ]
                case _:
                    continue
            self.trace_lines.extend(block)
            print("\n".join(block))
            self.step += 1


async def run_agent_realtime_logging(
    agent: Agent,
    prompt: str,
    log_path: Path,
    max_steps: int = 12,
) -> AgentRunResult:
    """Exécuter un agent avec trace temps réel des appels outils

    Entrées
    - agent : instance d'agent pydantic-ai configurée
    - prompt : prompt utilisateur envoyé à `agent.run`
    - log_path : chemin du fichier de log
    - max_steps : nombre maximal d'étapes autorisées

    Sortie
    - `AgentRunResult`
    """
    trace_lines = [
        "RUN TRACE",
        f"- prompt : {prompt}",
        "=" * 80,
    ]
    print("\n".join(trace_lines))

    run_result = await agent.run(
        prompt,
        event_stream_handler=EventStreamHandler(trace_lines),
        usage_limits=UsageLimits(request_limit=max_steps),
    )

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(trace_lines), encoding="utf-8")
    print(f"log_path : {log_path.resolve()}")

    return run_result
