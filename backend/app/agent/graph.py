"""
Definicion del StateGraph. Este es el flujo determinista descrito en el PRD:

  Ingesta -> Nodo LLM (parsea intencion, NO calcula) -> Ruteo condicional
  -> ToolNode (ejecuta Python puro) -> Nodo LLM (redacta veredicto con el
  resultado exacto de la tool) -> Respuesta

TODO: una vez que tools.py este implementado, probar el grafo end-to-end con
casos reales del motor de reglas elegido.
"""
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage

from app.config import settings
from app.agent.state import AgentState
from app.agent.tools import ALL_TOOLS
from app.agent.prompts import SYSTEM_PROMPT

llm = ChatAnthropic(model=settings.llm_model, api_key=settings.anthropic_api_key)
llm_with_tools = llm.bind_tools(ALL_TOOLS)


def call_model(state: AgentState) -> dict:
    """Nodo LLM: parsea intencion y decide si necesita llamar una tool."""
    messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("llm", call_model)
    graph.add_node("tools", ToolNode(ALL_TOOLS))

    graph.set_entry_point("llm")

    # tools_condition enruta a "tools" si el ultimo mensaje del LLM incluye
    # una tool call, o a END si ya puede responder directo (ej. pidiendo mas info)
    graph.add_conditional_edges("llm", tools_condition)
    graph.add_edge("tools", "llm")

    return graph.compile()


# Instancia compilada, lista para invocar desde la API
compiled_graph = build_graph()
