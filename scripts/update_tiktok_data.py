#!/usr/bin/env python3
"""
Lee el perfil público de TikTok de Dimensión Zombi y actualiza data/tiktok-data.json
con el número de seguidores, me gusta, videos totales y los IDs de los videos más
recientes.

Este script usa una técnica NO oficial: descarga el HTML público del perfil y
extrae el bloque de datos que TikTok incrusta en la página para renderizarla
(la misma información que ve cualquier navegador, solo que aquí se lee directo
del HTML en vez de hacerlo visualmente).

Si TikTok cambia la estructura de esa página, este script puede empezar a fallar.
Está diseñado para fallar de forma segura: si no logra extraer los datos,
NO toca el archivo tiktok-data.json existente, así el sitio se queda mostrando
los últimos datos válidos en vez de romperse.
"""

import json
import re
import sys
from pathlib import Path

import requests

PROFILE_URL = "https://www.tiktok.com/@dimensionzombiclubdehor"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "tiktok-data.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def extract_json_blob(html: str) -> dict:
    """TikTok incrusta un <script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"> con
    todo el estado de la página en JSON. Lo buscamos y lo parseamos."""
    match = re.search(
        r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',
        html,
        re.DOTALL,
    )
    if not match:
        raise ValueError(
            "No se encontró el bloque __UNIVERSAL_DATA_FOR_REHYDRATION__. "
            "TikTok pudo haber cambiado la estructura de la página."
        )
    return json.loads(match.group(1))


def find_user_module(data: dict) -> dict:
    """Navega la estructura del JSON hasta encontrar el módulo con los datos
    del usuario (seguidores, likes, etc). La ruta exacta puede variar."""
    try:
        default_scope = data["__DEFAULT_SCOPE__"]
    except KeyError:
        raise ValueError("Estructura inesperada: falta __DEFAULT_SCOPE__")

    # El módulo de perfil de usuario suele vivir bajo esta llave.
    user_detail = default_scope.get("webapp.user-detail")
    if not user_detail:
        raise ValueError("No se encontró 'webapp.user-detail' en los datos.")

    user_info = user_detail.get("userInfo", {})
    stats = user_info.get("stats", {})
    if not stats:
        raise ValueError("No se encontraron estadísticas del usuario.")

    return stats


def find_recent_video_ids(data: dict, limit: int = 6) -> list:
    """Intenta extraer los IDs de los videos más recientes desde el módulo
    de la lista de publicaciones del usuario, si está presente en esta carga
    de página (TikTok no siempre incluye la lista completa en el HTML inicial)."""
    try:
        default_scope = data["__DEFAULT_SCOPE__"]
        item_list = default_scope.get("webapp.user-detail", {}).get("itemList", [])
        ids = [item["id"] for item in item_list if "id" in item]
        return ids[:limit]
    except Exception:
        return []


def main():
    try:
        html = fetch_html(PROFILE_URL)
        data = extract_json_blob(html)
        stats = find_user_module(data)
        video_ids = find_recent_video_ids(data)

        result = {
            "followers": int(stats.get("followerCount", 0)),
            "likes": int(stats.get("heartCount", 0)),
            "videoCount": int(stats.get("videoCount", 0)),
        }

        # Solo sobreescribimos la lista de videos si de verdad encontramos alguno;
        # si no, conservamos los que ya había en el archivo.
        if OUTPUT_PATH.exists():
            existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        else:
            existing = {}

        result["videoIds"] = video_ids if video_ids else existing.get("videoIds", [])
        result["lastUpdated"] = "auto"

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"✅ Datos actualizados: {result}")

    except Exception as err:
        # Falla segura: no tocamos el archivo existente, solo avisamos en el log.
        print(f"⚠️  No se pudo actualizar automáticamente: {err}", file=sys.stderr)
        print("El sitio seguirá mostrando los últimos datos válidos guardados.")
        # Salimos con código 0 a propósito: un fallo de lectura de TikTok
        # no debe marcar la Action como "rota" cada vez que TikTok cambie algo.
        sys.exit(0)


if __name__ == "__main__":
    main()
