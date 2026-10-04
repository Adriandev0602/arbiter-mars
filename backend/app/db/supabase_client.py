"""
Cliente de Supabase, instanciado una sola vez y reutilizado en toda la app.

Usa un cliente HTTP propio en vez del que arma supabase-py por defecto: aquel
multiplexa todo sobre UNA conexion HTTP/2, y cuando Supabase la cierra caen
juntas todas las consultas en vuelo ("Server disconnected"; el dashboard pide
estado, tablero y parametros en paralelo, asi que pasaba seguido). Con
HTTP/1.1 cada consulta va por su conexion, y las LECTURAS que se cortan asi se
reintentan: repetir un GET no cambia nada. Las escrituras nunca se reintentan
solas, porque el servidor pudo haberlas aplicado antes de cortar.
"""
import httpx
from supabase import ClientOptions, create_client, Client

from app.config import settings

_SAFE_METHODS = {"GET", "HEAD"}
_READ_RETRIES = 2


class _RetryReadsTransport(httpx.HTTPTransport):
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            try:
                return super().handle_request(request)
            except (httpx.RemoteProtocolError, httpx.ReadError):
                if request.method not in _SAFE_METHODS or attempt >= _READ_RETRIES:
                    raise
                attempt += 1


_http = httpx.Client(
    transport=_RetryReadsTransport(retries=1),  # retries=1: reintenta fallas al CONECTAR (no hubo pedido)
    timeout=httpx.Timeout(30.0, connect=10.0),
    follow_redirects=True,
)

supabase: Client = create_client(settings.supabase_url, settings.supabase_key, options=ClientOptions(httpx_client=_http))
