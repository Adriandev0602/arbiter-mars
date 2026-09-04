"""
Mecanica politica (nucleo) de la expansion Turmoil. Funciones puras, mismo
estilo que colonies.py/board.py -- sin dependencias de FastAPI/Supabase.

Fuente del MECANISMO: rulebook oficial de la expansion (fryxgames.se,
TM_TURMOIL_ENG_RULES.pdf, 8 paginas, leido completo) -- alta confianza,
fuente primaria. Verificado ahi:
  - 6 partidos: Mars First, Kelvinists, Reds, Greens, Unity, Scientists
    (PARTY_NAMES abajo esta en el orden horario en que aparecen en el
    diagrama del Terraforming Committee board, pagina 3 del rulebook --
    Mars First arriba-izquierda, Kelvinists arriba-derecha, Reds derecha,
    Greens abajo-derecha, Unity abajo-izquierda, Scientists izquierda).
  - Setup: cada jugador arranca con 7 delegados -- 1 en el Lobby, 6 en la
    Reserva. GREENS arranca como partido Ruling (su Policy tile queda
    arriba de la pila). No hay partido Dominante hasta el primer Global
    Event (mazo de 31 cartas, fuera de alcance -- ver nota de alcance).
  - Accion "Lobbying" (nueva, no proyecto estandar; puede usarse cualquier
    cantidad de veces por generacion): mueve 1 delegado del Lobby (gratis)
    o de la Reserva (5 MC) al area de delegados del partido elegido.
  - Party Leader: el primer delegado colocado en un partido vacio es su
    lider automatico; si otro jugador consigue MAS delegados que el lider
    actual en ese partido, lo reemplaza.
  - Partido Dominante: el que tiene mas delegados TOTALES (de cualquier
    dueno). Se actualiza al instante si otro partido lo supera
    estrictamente (no hace falta esperar a fin de generacion).
  - Requisitos de carta que muestran el icono de un partido ("Project
    card requirements", pagina 4): jugables solo si ese partido esta
    Ruling actualmente, O si el jugador tiene al menos 2 delegados propios
    ahi (ej. Colonial Envoys: partido Unity).
  - Influencia (pagina 5, "0-3 influence"): +1 por ser Chairman; +1 por
    ser el Party Leader del partido Dominante; +1 (en vez del anterior,
    nunca ademas, para el MISMO jugador) por tener 1+ delegados NO-lider
    ahi. El total puede superar 3 con bonus de carta ("modified up or
    down, even beyond 5" -- el rulebook lo permite explicitamente para
    valores de Influencia sumados a otros contadores).
  - "New Government" (paso 3 de la fase Turmoil, tras produccion, pagina
    4/7): el partido Dominante pasa a ser el Ruling; el viejo Chairman Y
    todos los delegados del partido (ahora) Ruling vuelven a sus Reservas,
    EXCEPTO el delegado del Party Leader, que se mueve a la silla de
    Chairman en vez de volver (y ese jugador gana 1 TR en el juego real --
    ver nota de alcance); el partido Dominante se recalcula entre los
    partidos restantes (empate se rompe en sentido horario a partir del
    partido que se acaba de volver Ruling).

ALCANCE DE ESTA PRIMERA PASADA (decision explicita del usuario,
2026-09-04): se implementa el NUCLEO politico -- partidos, delegados,
Lobbying, Party Leader/Dominante/Chairman, Influencia -- lo suficiente
para que Colonial Envoys y Colonial Representation (las 2 cartas
pendientes que dependian de esto, ver CARDS_LOG.md) funcionen de verdad.
QUEDAN EXPLICITAMENTE PENDIENTES, cada uno del tamano de una feature
aparte:
  - Las Ruling Bonus / Ruling Policy de los 6 partidos (12 efectos
    distintos sobre recursos/producciones de TODOS los jugadores, ej.
    Reds: "Lose 3 M€ for each step your TR is raised").
  - El mazo de 31 Global Event cards (afectan a todos los jugadores cada
    generacion, usan Influencia para escalar contadores con tope 5).
  - La revision de TR (-1 a TODOS los jugadores cada generacion).
  - `resolve_new_government` esta ACOTADO a un solo jugador (modo un
    jugador de este proyecto, ver CLAUDE.md seccion 7 -- delegados
    neutrales/de otros jugadores en el partido Dominante no se simulan
    aparte, mismo criterio que el resto del proyecto en single-player):
    calcula cuantos delegados PROPIOS de `player_id` vuelven a su
    reserva y si `player_id` se vuelve Chairman, pero no itera sobre
    otros jugadores ni aplica el TR gratis del Chairman.
"""
from typing import TypedDict

PARTY_NAMES = ["mars_first", "kelvinists", "reds", "greens", "unity", "scientists"]
STARTING_LOBBY_DELEGATES = 1
STARTING_RESERVE_DELEGATES = 6
LOBBY_FROM_RESERVE_COST_MC = 5


class PartyState(TypedDict):
    delegates: dict[str, int]  # player_id -> cantidad de delegados propios en este partido
    leader: str | None  # player_id del Party Leader, None si el partido esta vacio


class TurmoilState(TypedDict):
    parties: dict[str, PartyState]
    dominant_party: str | None
    ruling_party: str
    chairman: str | None


class UnknownPartyError(Exception):
    """El partido no existe en PARTY_NAMES."""


def new_turmoil() -> TurmoilState:
    """Setup: ver rulebook pagina 2 -- GREENS arranca Ruling, sin Dominante todavia."""
    return TurmoilState(
        parties={name: PartyState(delegates={}, leader=None) for name in PARTY_NAMES},
        dominant_party=None,
        ruling_party="greens",
        chairman=None,
    )


def _party_total(party: PartyState) -> int:
    return sum(party["delegates"].values())


def _recompute_dominant(parties: dict[str, PartyState], from_party: str) -> str | None:
    """
    Partido con mas delegados totales entre TODOS. Empate: el primero en
    sentido horario a partir de `from_party` (PARTY_NAMES ya esta en ese
    orden). Ninguno si todos estan vacios.
    """
    totals = {name: _party_total(p) for name, p in parties.items()}
    max_total = max(totals.values())
    if max_total == 0:
        return None
    start = PARTY_NAMES.index(from_party)
    rotated = PARTY_NAMES[start:] + PARTY_NAMES[:start]
    return next(name for name in rotated if totals[name] == max_total)


def place_delegate(turmoil: TurmoilState, party: str, player_id: str) -> TurmoilState:
    """
    Coloca 1 delegado de `player_id` en `party`. Actualiza el Party Leader
    (si `player_id` termina con MAS delegados ahi que el lider actual, lo
    reemplaza -- el primer delegado en un partido vacio es lider
    automatico) y el partido Dominante (si el nuevo total de `party`
    supera estrictamente al del Dominante actual, o si todavia no habia
    Dominante). NO cobra nada -- el caller (tools.py) es responsable del
    costo (Lobbying: gratis desde el Lobby, 5 MC desde la Reserva;
    Colonial Envoys: gratis, sale de la Reserva sin pasar por Lobbying).
    """
    if party not in turmoil["parties"]:
        raise UnknownPartyError(f"Partido '{party}' no existe")
    p = turmoil["parties"][party]
    new_delegates = {**p["delegates"], player_id: p["delegates"].get(player_id, 0) + 1}
    new_leader = p["leader"]
    if new_leader is None or new_delegates[player_id] > new_delegates.get(new_leader, 0):
        new_leader = player_id
    new_party = PartyState(delegates=new_delegates, leader=new_leader)
    new_parties = {**turmoil["parties"], party: new_party}

    new_dominant = turmoil["dominant_party"]
    new_total = _party_total(new_party)
    dominant_total = _party_total(new_parties[new_dominant]) if new_dominant is not None else -1
    if new_dominant is None or new_total > dominant_total:
        new_dominant = party

    return TurmoilState(
        parties=new_parties, dominant_party=new_dominant,
        ruling_party=turmoil["ruling_party"], chairman=turmoil["chairman"],
    )


def can_play_party_gated_card(turmoil: TurmoilState, party: str, player_id: str, min_delegates: int = 2) -> bool:
    """
    Vocabulario de requirement "ruling_or_delegates" (ver
    rules_engine.check_card_requirements): True si `party` es el Ruling
    actual, o si `player_id` tiene al menos `min_delegates` delegados
    propios ahi (ej. Colonial Envoys: partido Unity, min_delegates=2).
    """
    if party not in turmoil["parties"]:
        raise UnknownPartyError(f"Partido '{party}' no existe")
    if turmoil["ruling_party"] == party:
        return True
    return turmoil["parties"][party]["delegates"].get(player_id, 0) >= min_delegates


def compute_influence(turmoil: TurmoilState, player_id: str, bonus: int = 0) -> int:
    """
    Formula oficial (0-3 antes de bonus de carta, rulebook pagina 5): +1
    si `player_id` es Chairman; +1 si es el Party Leader del partido
    Dominante; +1 (en vez del anterior, nunca ademas, para el mismo
    jugador) si tiene 1+ delegados NO-lider ahi. `bonus` se suma aparte
    (ej. Colonial Representation: +1 fijo, pieza `passive.influence_bonus`
    en rules_engine.register_passive_effect) -- el total puede superar 3,
    el rulebook lo permite explicitamente.
    """
    influence = bonus
    if turmoil["chairman"] == player_id:
        influence += 1
    dominant = turmoil["dominant_party"]
    if dominant is not None:
        dom = turmoil["parties"][dominant]
        if dom["leader"] == player_id:
            influence += 1
        elif dom["delegates"].get(player_id, 0) > 0:
            influence += 1
    return influence


def resolve_new_government(turmoil: TurmoilState, player_id: str) -> tuple[TurmoilState, int]:
    """
    Paso "New Government" (rulebook pagina 4/7), ACOTADO a un solo jugador
    -- ver nota de alcance arriba del modulo. No hace nada (devuelve 0
    delegados) si todavia no hay partido Dominante.

    El partido Dominante pasa a ser el Ruling. Si `player_id` era su
    Party Leader, se vuelve el nuevo Chairman (su delegado se mueve a la
    silla de Chairman, no vuelve a la reserva). El resto de los delegados
    PROPIOS de `player_id` en ese partido, mas su delegado de Chairman
    ANTERIOR si lo tenia, vuelven a su Reserva -- el caller (tools.py) es
    quien de verdad suma ese numero a `player["reserve_delegates"]`, esta
    funcion solo lo calcula. El partido Dominante se recalcula entre los
    partidos restantes (ver _recompute_dominant).

    No aplica Ruling Bonus/Ruling Policy ni la revision de TR -- fuera de
    alcance de esta primera pasada.

    Devuelve (turmoil actualizado, delegados de `player_id` que vuelven a
    su reserva).
    """
    dominant = turmoil["dominant_party"]
    if dominant is None:
        return turmoil, 0
    dom = turmoil["parties"][dominant]
    own_in_dominant = dom["delegates"].get(player_id, 0)
    was_leader = dom["leader"] == player_id
    was_old_chairman = turmoil["chairman"] == player_id

    returned = (own_in_dominant - (1 if was_leader else 0)) + (1 if was_old_chairman else 0)
    new_chairman = dom["leader"]

    new_parties = {**turmoil["parties"], dominant: PartyState(delegates={}, leader=None)}
    new_dominant = _recompute_dominant(new_parties, dominant)

    return TurmoilState(
        parties=new_parties, dominant_party=new_dominant, ruling_party=dominant, chairman=new_chairman,
    ), returned
