"""
Endpoints de la API. Delgados a proposito: la logica vive en agent/graph.py
y db/, esto solo traduce HTTP <-> el grafo.
"""
from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from app.agent.graph import compiled_graph
from app.models.schemas import ChatRequest, ChatResponse, PlayerState

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Recibe una consulta en lenguaje natural, la corre a traves del grafo
    (LLM -> tools -> LLM) y devuelve el veredicto + estado actualizado.
    """
    result = compiled_graph.invoke(
        {
            "messages": [HumanMessage(content=request.message)],
            "player_id": request.player_id,
            "extracted_args": None,
            "tool_result": None,
        }
    )
    last_message = result["messages"][-1]

    # TODO: una vez que tools.py devuelva resulting_balance real, propagarlo aqui
    return ChatResponse(reply=last_message.content, updated_state=None)


@router.get("/state/{player_id}", response_model=PlayerState)
def get_state(player_id: str):
    """
    Devuelve el estado actual del jugador para pintar el dashboard.
    TODO: implementar el query real a Supabase (reutilizar get_player_state de tools.py).
    """
    raise NotImplementedError("Definir el schema de estado antes de implementar esto")
