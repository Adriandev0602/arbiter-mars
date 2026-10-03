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

ALCANCE (actualizado 2026-10-02): nucleo politico completo -- partidos,
delegados, Lobbying, Party Leader/Dominante/Chairman, Influencia -- mas las
Ruling Bonus/Policy y la revision de TR (2026-09-10, ver CARDS_LOG.md) y,
desde 2026-10-02, los DELEGADOS NEUTRALES con el mecanismo oficial
(rulebook paginas 2, 5, 6 y 7):
  - 14 delegados neutrales en total ("14 Neutral delegates", componentes,
    pagina 8). Setup: 1 en la silla de Chairman y el resto (13) en la
    Neutral Reserve. `chairman is None` representa ese Chairman neutral.
  - Los neutrales "do not belong to any player, but they do count as a
    separate player. These neutral delegates can become Party Leader and
    Chairman" (pagina 5). Se modelan como un jugador mas dentro de
    `PartyState.delegates`, bajo la clave reservada NEUTRAL: misma regla de
    Party Leader y de Dominante que cualquier delegado.
  - Entran SOLO via Global Events: setup (la carta Coming pone un neutral
    como Party Leader en el partido de arriba a la izquierda; la Distant,
    otro en el de arriba a la izquierda) y "Changing Times" (la que pasa de
    Coming a Current agrega uno en el partido de la mitad derecha; la nueva
    Distant, uno en el de arriba a la izquierda). Ver setup_global_events /
    changing_times. Los dos partidos de cada carta viven en el catalogo
    (`global_events.revealed_party` / `current_party`), verificados contra
    los 36 scans y contra la implementacion open-source de referencia.
  - New Government: el Chairman anterior y los delegados no-lider del
    partido Dominante vuelven a SU reserva -- los neutrales, a la Neutral
    Reserve. Si el Party Leader es neutral, el nuevo Chairman es neutral.
  - `resolve_new_government` sigue ACOTADO a un solo jugador humano (modo
    un jugador de este proyecto, ver CLAUDE.md seccion 7): calcula cuantos
    delegados PROPIOS de `player_id` vuelven a su reserva; los neutrales se
    mueven aca mismo porque su reserva vive en el estado de Turmoil.
"""
from typing import TypedDict

PARTY_NAMES = ["mars_first", "kelvinists", "reds", "greens", "unity", "scientists"]
STARTING_LOBBY_DELEGATES = 1
STARTING_RESERVE_DELEGATES = 6
LOBBY_FROM_RESERVE_COST_MC = 5
# "14 Neutral delegates" (rulebook, componentes, pagina 8). En el setup uno va
# a la silla de Chairman y el resto a la Neutral Reserve (pagina 2).
TOTAL_NEUTRAL_DELEGATES = 14
# Clave reservada de los delegados neutrales dentro de PartyState.delegates:
# "they do count as a separate player" (pagina 5). Ningun player_id real
# puede valer esto (los jugadores son uuid).
NEUTRAL = "neutral"


class PartyState(TypedDict):
    # owner -> cantidad de delegados en este partido. `owner` es un player_id
    # o NEUTRAL para los delegados neutrales.
    delegates: dict[str, int]
    leader: str | None  # owner del Party Leader (player_id o NEUTRAL), None si esta vacio


class TurmoilState(TypedDict):
    parties: dict[str, PartyState]
    dominant_party: str | None
    ruling_party: str
    # player_id del Chairman, o None si la silla la ocupa un neutral.
    chairman: str | None
    # Delegados neutrales que todavia no estan en la mesa (ni en partidos ni
    # en la silla de Chairman).
    neutral_reserve: int
    # Track de Global Events (pagina 6): Distant (recien revelada), Coming y
    # Current (la que se ejecuta en la fase Turmoil). None = vacio.
    distant_event: str | None
    coming_event: str | None
    current_event: str | None
    # Mazo de Global Events boca abajo, ya mezclado (lo mezcla tools.py).
    global_event_deck: list[str]


class UnknownPartyError(Exception):
    """El partido no existe en PARTY_NAMES."""


def new_turmoil() -> TurmoilState:
    """
    Setup (rulebook pagina 2): GREENS arranca Ruling; un neutral en la silla
    de Chairman y los otros 13 en la Neutral Reserve; sin Dominante hasta que
    se arme el track de Global Events (setup_global_events).
    """
    return TurmoilState(
        parties={name: PartyState(delegates={}, leader=None) for name in PARTY_NAMES},
        dominant_party=None,
        ruling_party="greens",
        chairman=None,
        neutral_reserve=TOTAL_NEUTRAL_DELEGATES - 1,
        distant_event=None,
        coming_event=None,
        current_event=None,
        global_event_deck=[],
    )


def normalize_turmoil(turmoil: dict) -> TurmoilState:
    """
    Lleva un estado de Turmoil guardado con una forma vieja a la actual, sin
    tocar lo que ya esta bien. Hasta 2026-10-02 cada partido traia un campo
    `neutral: 2` FIJO (supuesto de diseno para Recruitment, no la regla
    oficial): se descarta, porque los neutrales oficiales solo entran via
    Global Events. Las claves nuevas de TurmoilState toman su valor inicial.
    """
    base = new_turmoil()
    if not turmoil:
        return base
    parties = {}
    for name in PARTY_NAMES:
        p = (turmoil.get("parties") or {}).get(name) or {}
        parties[name] = PartyState(delegates=dict(p.get("delegates") or {}), leader=p.get("leader"))
    return TurmoilState(**{  # type: ignore[typeddict-item]
        **base,
        **{k: v for k, v in turmoil.items() if k in base and k != "parties"},
        "parties": parties,
    })


def _party_total(party: PartyState) -> int:
    return sum(party["delegates"].values())


def _recompute_dominant(parties: dict[str, PartyState], from_party: str) -> str | None:
    """
    Partido con mas delegados totales (de cualquier dueno, neutrales
    incluidos). Empate: el primero en sentido horario a partir de
    `from_party` (PARTY_NAMES ya esta en ese orden). Ninguno si todos estan
    vacios.
    """
    totals = {name: _party_total(p) for name, p in parties.items()}
    max_total = max(totals.values())
    if max_total == 0:
        return None
    start = PARTY_NAMES.index(from_party)
    rotated = PARTY_NAMES[start:] + PARTY_NAMES[:start]
    return next(name for name in rotated if totals[name] == max_total)


def _check_party(turmoil: TurmoilState, party: str) -> None:
    if party not in turmoil["parties"]:
        raise UnknownPartyError(f"Partido '{party}' no existe")


def _add_to_party(turmoil: TurmoilState, party: str, owner: str) -> TurmoilState:
    """
    Suma 1 delegado de `owner` (player_id o NEUTRAL) a `party` y actualiza
    Party Leader y Dominante. Party Leader: el primer delegado de un partido
    vacio es lider automatico; quien tenga MAS delegados que el lider actual
    lo reemplaza ("If a player (including the neutral 'player') ever has more
    delegates in a party than the current Party Leader", pagina 4).
    Dominante: cambia si el total de `party` supera ESTRICTAMENTE al del
    Dominante actual, o si todavia no habia.
    """
    p = turmoil["parties"][party]
    new_delegates = {**p["delegates"], owner: p["delegates"].get(owner, 0) + 1}
    new_leader = p["leader"]
    if new_leader is None or new_delegates[owner] > new_delegates.get(new_leader, 0):
        new_leader = owner
    new_party = PartyState(delegates=new_delegates, leader=new_leader)
    new_parties = {**turmoil["parties"], party: new_party}

    new_dominant = turmoil["dominant_party"]
    dominant_total = _party_total(new_parties[new_dominant]) if new_dominant is not None else -1
    if new_dominant is None or _party_total(new_party) > dominant_total:
        new_dominant = party
    return TurmoilState(**{**turmoil, "parties": new_parties, "dominant_party": new_dominant})  # type: ignore[typeddict-item]


def place_delegate(turmoil: TurmoilState, party: str, player_id: str) -> TurmoilState:
    """
    Coloca 1 delegado de `player_id` en `party` (ver _add_to_party para el
    Party Leader y el Dominante). NO cobra nada -- el caller (tools.py) es
    responsable del costo (Lobbying: gratis desde el Lobby, 5 MC desde la
    Reserva; Colonial Envoys: gratis, sale de la Reserva sin pasar por
    Lobbying).
    """
    _check_party(turmoil, party)
    return _add_to_party(turmoil, party, player_id)


def place_neutral_delegate(turmoil: TurmoilState, party: str) -> TurmoilState:
    """
    Un Global Event agrega un delegado neutral a `party`, sacandolo de la
    Neutral Reserve. Puede volverse Party Leader y cambiar el Dominante como
    cualquier delegado. Si la Neutral Reserve esta vacia no pasa nada (el
    rulebook no preve reponerla).
    """
    _check_party(turmoil, party)
    if turmoil["neutral_reserve"] < 1:
        return turmoil
    placed = _add_to_party(turmoil, party, NEUTRAL)
    return TurmoilState(**{**placed, "neutral_reserve": turmoil["neutral_reserve"] - 1})  # type: ignore[typeddict-item]


def neutral_non_leader_count(turmoil: TurmoilState, party: str) -> int:
    """Delegados neutrales de `party` que NO son su Party Leader."""
    _check_party(turmoil, party)
    p = turmoil["parties"][party]
    return p["delegates"].get(NEUTRAL, 0) - (1 if p["leader"] == NEUTRAL else 0)


def exchange_neutral_delegate(turmoil: TurmoilState, party: str, player_id: str) -> TurmoilState:
    """
    Recruitment (T11): "exchange one NEUTRAL NON-LEADER delegate with one of
    your own from the reserve" -- un neutral NO-lider de `party` vuelve a la
    Neutral Reserve y uno propio de `player_id` ocupa su lugar (puede
    volverlo Party Leader, con la regla de siempre). El total del partido no
    cambia, asi que el Dominante tampoco.

    No saca el delegado de la Reserva del jugador -- el caller (tools.py) es
    quien debita `player.reserve_delegates`, igual criterio que
    place_delegate no cobra MC.

    Lanza UnknownPartyError si el partido no existe o no tiene neutrales
    no-lider.
    """
    if neutral_non_leader_count(turmoil, party) < 1:
        raise UnknownPartyError(f"'{party}' no tiene delegados neutrales NO-lider para intercambiar")
    p = turmoil["parties"][party]
    new_delegates = {**p["delegates"], NEUTRAL: p["delegates"][NEUTRAL] - 1}
    if new_delegates[NEUTRAL] == 0:
        del new_delegates[NEUTRAL]
    new_delegates[player_id] = new_delegates.get(player_id, 0) + 1
    new_leader = p["leader"]
    if new_leader is None or new_delegates[player_id] > new_delegates.get(new_leader, 0):
        new_leader = player_id
    new_parties = {**turmoil["parties"], party: PartyState(delegates=new_delegates, leader=new_leader)}
    return TurmoilState(**{  # type: ignore[typeddict-item]
        **turmoil, "parties": new_parties, "neutral_reserve": turmoil["neutral_reserve"] + 1,
    })


def remove_delegate(
    turmoil: TurmoilState, party: str, player_id: str, allow_leader: bool = False,
) -> TurmoilState:
    """
    Saca 1 delegado propio de `party` y lo devuelve a la Reserva del jugador
    (el caller es quien suma a `player["reserve_delegates"]`). Por defecto solo
    se pueden remover delegados NO-lider: si `player_id` es el Party Leader de
    ese partido, se rechaza (Banned Delegate dice "remove any NON-LEADER
    delegate"). `allow_leader=True` levanta esa restriccion para cartas que NO
    la imprimen (ej. Red Appeasement, cuya accion cuesta 2 delegados propios:
    con exactamente 2 en un partido, uno es forzosamente el lider). Si el
    lider se queda sin delegados ahi, el liderazgo pasa a quien tenga mas
    (neutrales incluidos). Recalcula el partido Dominante -- el FAQ oficial
    confirma que la remocion puede cambiarlo AL INSTANTE, con el mismo
    desempate horario de _recompute_dominant.
    """
    _check_party(turmoil, party)
    p = turmoil["parties"][party]
    if p["delegates"].get(player_id, 0) < 1:
        raise UnknownPartyError(f"El jugador no tiene delegados en '{party}'")
    if p["leader"] == player_id and not allow_leader:
        raise UnknownPartyError(
            f"El delegado de '{player_id}' en '{party}' es el Party Leader: solo se pueden remover NO-lideres"
        )
    new_delegates = {**p["delegates"], player_id: p["delegates"][player_id] - 1}
    new_leader = p["leader"]
    if new_delegates[player_id] == 0:
        del new_delegates[player_id]
        if new_leader == player_id:
            new_leader = max(new_delegates, key=lambda owner: new_delegates[owner], default=None)
    new_parties = {**turmoil["parties"], party: PartyState(delegates=new_delegates, leader=new_leader)}
    from_party = turmoil["dominant_party"] or party
    return TurmoilState(**{  # type: ignore[typeddict-item]
        **turmoil, "parties": new_parties, "dominant_party": _recompute_dominant(new_parties, from_party),
    })


def can_play_party_gated_card(turmoil: TurmoilState, party: str, player_id: str, min_delegates: int = 2) -> bool:
    """
    Vocabulario de requirement "ruling_or_delegates" (ver
    rules_engine.check_card_requirements): True si `party` es el Ruling
    actual, o si `player_id` tiene al menos `min_delegates` delegados
    propios ahi (ej. Colonial Envoys: partido Unity, min_delegates=2).
    """
    _check_party(turmoil, party)
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
    Paso "New Government" (rulebook paginas 4 y 7, pasos 3a-3e). No hace
    nada (devuelve 0 delegados) si todavia no hay partido Dominante.

    El partido Dominante pasa a ser el Ruling. "Return the former Chairman
    and all non-leader delegates from Dominant party to reserve" y "Party
    Leader from the Dominant party becomes new Chairman":
      - Los delegados PROPIOS de `player_id` que vuelven a su reserva (sus
        no-lider del Dominante, mas el Chairman anterior si era suyo) se
        DEVUELVEN como numero: el caller (tools.py) los suma a
        `player["reserve_delegates"]`.
      - Los NEUTRALES se mueven aca mismo, porque su reserva vive en este
        estado: los no-lider del Dominante y el Chairman anterior si era
        neutral vuelven a `neutral_reserve`.
      - Si el Party Leader es neutral, la silla queda neutral
        (`chairman = None`); si es un jugador, ese jugador es el Chairman
        (el +1 TR lo aplica tools.py).
    El partido Dominante se recalcula entre los partidos restantes (ver
    _recompute_dominant). Los delegados de OTROS jugadores no se simulan
    (modo un jugador).

    Devuelve (turmoil actualizado, delegados de `player_id` que vuelven a
    su reserva).
    """
    dominant = turmoil["dominant_party"]
    if dominant is None:
        return turmoil, 0
    dom = turmoil["parties"][dominant]
    leader = dom["leader"]

    own_in_dominant = dom["delegates"].get(player_id, 0)
    returned = (own_in_dominant - (1 if leader == player_id else 0)) + (1 if turmoil["chairman"] == player_id else 0)

    neutral_in_dominant = dom["delegates"].get(NEUTRAL, 0)
    neutral_returned = neutral_in_dominant - (1 if leader == NEUTRAL else 0)
    if turmoil["chairman"] is None:
        neutral_returned += 1  # el Chairman anterior era neutral

    new_chairman = None if leader in (None, NEUTRAL) else leader
    new_parties = {**turmoil["parties"], dominant: PartyState(delegates={}, leader=None)}
    return TurmoilState(**{  # type: ignore[typeddict-item]
        **turmoil,
        "parties": new_parties,
        "dominant_party": _recompute_dominant(new_parties, dominant),
        "ruling_party": dominant,
        "chairman": new_chairman,
        "neutral_reserve": turmoil["neutral_reserve"] + neutral_returned,
    }), returned


def setup_global_events(
    turmoil: TurmoilState, shuffled_deck: list[str], event_parties: dict[str, tuple[str, str]],
) -> TurmoilState:
    """
    Paso 3 del setup de Turmoil (rulebook pagina 2): con el mazo ya mezclado,
    la primera carta va a COMING y pone un neutral (como Party Leader, el
    partido esta vacio) en el partido de su esquina superior izquierda -- ese
    partido pasa a ser el Dominante; la segunda va a DISTANT y pone otro
    neutral en el partido de su esquina superior izquierda ("If it is in the
    same party as the other neutral delegate, place it in the area for
    delegates instead" -- sale solo de la regla de Party Leader). No hay
    Current en la primera generacion.

    `event_parties`: {event_id: (revealed_party, current_party)} -- arriba a
    la izquierda y mitad derecha de cada carta (catalogo `global_events`).
    Lanza ValueError si el mazo tiene menos de 2 cartas o ya hay un track.
    """
    if turmoil["coming_event"] is not None or turmoil["distant_event"] is not None:
        raise ValueError("El track de Global Events ya esta armado")
    if len(shuffled_deck) < 2:
        raise ValueError("Hacen falta al menos 2 Global Events para el setup")
    coming, distant, *rest = shuffled_deck
    new_turmoil = place_neutral_delegate(turmoil, event_parties[coming][0])
    new_turmoil = place_neutral_delegate(new_turmoil, event_parties[distant][0])
    return TurmoilState(**{  # type: ignore[typeddict-item]
        **new_turmoil, "coming_event": coming, "distant_event": distant,
        "current_event": None, "global_event_deck": rest,
    })


def changing_times(turmoil: TurmoilState, event_parties: dict[str, tuple[str, str]]) -> TurmoilState:
    """
    Paso 4 de la fase Turmoil, "Changing Times" (rulebook pagina 7), despues
    del New Government:
      a) la Coming pasa a Current y agrega un neutral en el partido de su
         mitad derecha;
      b) la Distant pasa a Coming;
      c) se da vuelta la primera del mazo como nueva Distant y agrega un
         neutral en el partido de su esquina superior izquierda.
    Si el mazo se agoto, la Distant queda vacia (el rulebook no preve
    remezclar). Lanza ValueError si el track no esta armado.
    """
    if turmoil["coming_event"] is None:
        raise ValueError("No hay Global Event en Coming: arma el track con setup_global_events")
    current = turmoil["coming_event"]
    new_turmoil = place_neutral_delegate(turmoil, event_parties[current][1])
    deck = list(turmoil["global_event_deck"])
    distant = deck.pop(0) if deck else None
    if distant is not None:
        new_turmoil = place_neutral_delegate(new_turmoil, event_parties[distant][0])
    return TurmoilState(**{  # type: ignore[typeddict-item]
        **new_turmoil, "current_event": current, "coming_event": turmoil["distant_event"],
        "distant_event": distant, "global_event_deck": deck,
    })
