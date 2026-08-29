"""
Estado compartido del grafo de LangGraph. Cada nodo lee y escribe sobre esta
estructura. Mantenerla lo mas plana y explicita posible: es mas facil debuggear
un StateGraph cuando el estado no tiene sorpresas.
"""
from typing import Annotated, Any, TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # Historial de mensajes de la conversacion (LangGraph los acumula via add_messages)
    messages: Annotated[list, add_messages]

    # Id del jugador actual, para resolver su estado en Supabase
    player_id: str

    # Argumentos estructurados que el nodo LLM extrajo de la consulta en
    # lenguaje natural, ej: {"project_name": "power_plant"} o
    # {"card_id": "...", "mc_to_pay": 8, "steel_to_pay": 3}
    extracted_args: dict[str, Any] | None

    # Resultado devuelto por la(s) tool(s) deterministas -- esto es lo unico
    # que el LLM puede usar para redactar la respuesta final, nunca numeros propios
    tool_result: dict[str, Any] | None
