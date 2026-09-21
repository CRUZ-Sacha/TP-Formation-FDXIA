import json
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.messages import FunctionToolCallEvent, FunctionToolResultEvent
from pydantic_ai.usage import UsageLimits


TRACE_SEPARATOR = "-" * 80


class EventStreamHandler:
    """Gestionnaire de flux pour journaliser les appels outils en temps réel

    Méthodes
    - `__call__` : consomme les événements et ajoute des blocs formatés
    """

    async def __call__(self, _run_context, event_stream) -> None:
        step = 1
        async for event in event_stream:
            match event:
                case FunctionToolCallEvent():
                    full_payload = json.dumps(event.part.args_as_dict(), ensure_ascii=False, indent=2)
                    if len(full_payload) > 600:
                        preview_payload = full_payload[:600] + f"\n...[truncated, total chars : {len(full_payload)}]"
                    else:
                        preview_payload = full_payload
                    preview_block = [
                        f"STEP {step} : TOOL CALL",
                        f"- tool : {event.part.tool_name}",
                        "- args :",
                        preview_payload,
                        TRACE_SEPARATOR,
                    ]
                case FunctionToolResultEvent():
                    full_payload = json.dumps(event.result.content, ensure_ascii=False, indent=2)
                    if len(full_payload) > 600:
                        preview_payload = full_payload[:600] + f"\n...[truncated, total chars : {len(full_payload)}]"
                    else:
                        preview_payload = full_payload
                    preview_block = [
                        f"STEP {step} : TOOL RESULT",
                        f"- tool : {event.result.tool_name}",
                        "- output :",
                        preview_payload,
                        TRACE_SEPARATOR,
                    ]
                case _:
                    continue
            print("\n".join(preview_block))
            step += 1


class LoggingAgent(Agent):
    """Agent PydanticAI étendu avec exécution tracée en temps réel et log JSON complet"""

    async def run_with_logging(self, request: str, log_path: Path, max_steps: int = 12) -> AgentRunResult:
        # TODO : Copier la méthode après l'avoir codée dans le notebook 3_1
        raise NotImplementedError("Copiez votre implémentation depuis le notebook 3_1")
