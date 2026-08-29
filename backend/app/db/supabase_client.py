"""
Cliente de Supabase, instanciado una sola vez y reutilizado en toda la app.
"""
from supabase import create_client, Client

from app.config import settings

supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
