from datetime import date

import googlemaps
import requests
from googlemaps.exceptions import ApiError, TransportError
from pydantic import BaseModel, ConfigDict
from tavily import TavilyClient

from shared.config import ROOT_DIR, project_settings
from shared.rag_utils import RAGAssistant, rag_embed_text_batch, rag_embed_text_batch_local

# ---------------
# OUTIL RAG

# INFO : Choix entre mode local ou mode distant (embeddings)
RAG_EMBED_FN = rag_embed_text_batch  # Mode distant
# RAG_EMBED_FN = rag_embed_text_batch_local  # Mode local

RAG_VECTOR_DB_DIR = ROOT_DIR / "TP2_travel_planner_RAG" / "data" / "chroma_db_rag_v2"
RAG_ASSISTANT: RAGAssistant | None = None


def get_rag_assistant() -> RAGAssistant:
    """Chargement paresseux de l'assistant RAG, instancié à la première utilisation"""
    global RAG_ASSISTANT
    if RAG_ASSISTANT is None:
        RAG_ASSISTANT = RAGAssistant(persist_dir=RAG_VECTOR_DB_DIR, embed_fn=RAG_EMBED_FN)
    return RAG_ASSISTANT


def tool_retrieve_docs(query: str, top_k: int = 5) -> list[dict[str, object]]:
    # TODO : Copier depuis le notebook 3_1
    raise NotImplementedError("Copiez votre implémentation depuis le notebook 3_1")


# ---------------
# AUTRES OUTILS


class Place(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    latitude: float
    longitude: float


def tool_get_current_date() -> dict[str, str]:
    """Retourner la date courante pour ancrer les dates relatives

    Sortie
    - dictionnaire avec
      - current_date : date ISO (`YYYY-MM-DD`)
      - weekday_name : nom du jour de la semaine
    """
    today = date.today()
    return {
        "current_date": today.isoformat(),
        "weekday_name": today.strftime("%A"),
    }


def tool_geocode_location(query: str) -> dict[str, object]:
    """Convertir un lieu texte en coordonnées (Google Maps Geocoding API)

    Entrées
    - query : lieu au format texte libre

    Sortie
    - dictionnaire `Place` sérialisé avec `name`, `latitude`, `longitude`
    """
    gmaps = googlemaps.Client(key=project_settings.google_api_geo_maps_key)
    results = gmaps.geocode(query)
    if not results:
        raise ValueError(f"Aucun résultat de géocodage pour : {query}")

    location = results[0]["geometry"]["location"]
    place = Place(
        name=results[0]["formatted_address"],
        latitude=location["lat"],
        longitude=location["lng"],
    )
    return place.model_dump()


def tool_get_weather(latitude: float, longitude: float, start_date: str, end_date: str) -> dict[str, object]:
    """Récupérer une prévision météo sur une plage de dates (Open-Meteo API)

    Entrées
    - latitude : latitude du lieu
    - longitude : longitude du lieu
    - start_date : date de début incluse au format ISO (`YYYY-MM-DD`)
    - end_date : date de fin incluse au format ISO (`YYYY-MM-DD`)

    Sortie
    - dictionnaire avec
      - timezone : fuseau de la réponse
      - days : liste journalière (date, min/max température, précipitations)
    """
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "start_date": start_date,
            "end_date": end_date,
        },
        timeout=45,
    )
    response.raise_for_status()
    data = response.json()

    daily = data["daily"]
    days: list[dict[str, object]] = []
    for index, day_date in enumerate(daily["time"]):
        days.append({
            "date": day_date,
            "min_temp_c": daily["temperature_2m_min"][index],
            "max_temp_c": daily["temperature_2m_max"][index],
            "precipitation_mm": daily["precipitation_sum"][index],
        })
    return {"timezone": data["timezone"], "days": days}


def tool_search_nearby(
    latitude: float,
    longitude: float,
    place_type: str = "restaurant",
    keyword: str = "",
    radius_m: int = 1500,
    limit: int = 8,
) -> dict[str, object]:
    """Rechercher des lieux proches à partir de coordonnées (Google Maps Places API)

    Entrées
    - latitude : latitude de référence
    - longitude : longitude de référence
    - place_type : type Google Places (`restaurant`, `museum`, `park`, ...)
    - keyword : filtre texte optionnel
    - radius_m : rayon de recherche en mètres
    - limit : nombre maximal de lieux retournés

    Sortie
    - dictionnaire avec `count` et `items` (liste de `Place` sérialisés)
    """
    gmaps = googlemaps.Client(key=project_settings.google_api_geo_maps_key)
    results = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=radius_m,
        type=place_type,
        keyword=keyword or None,
    )

    places = []
    for result in results.get("results", [])[:limit]:
        location = result["geometry"]["location"]
        places.append(
            Place(
                name=result.get("name", ""),
                latitude=location["lat"],
                longitude=location["lng"],
            ).model_dump()
        )
    return {
        "count": len(places),
        "items": places,
    }


def web_search(query: str, max_results: int = 5) -> dict[str, object]:
    """Rechercher des sources web externes (Tavily Search API)

    Entrées
    - query : requête de recherche
    - max_results : nombre maximal de résultats

    Sortie
    - dictionnaire avec `count` et `items` (`title`, `link`, `snippet`)
    """
    tavily_client = TavilyClient(api_key=project_settings.tavily_api_key)
    response_data = tavily_client.search(query=query, max_results=max_results)

    items = [
        {
            "title": result["title"],
            "link": result["url"],
            "snippet": result["content"],
        }
        for result in response_data.get("results", [])
    ]
    return {
        "count": len(items),
        "items": items,
    }


def web_extract(urls: str | list[str], query: str = "") -> dict[str, object]:
    """Extraire du contenu web depuis une ou plusieurs URL (Tavily Extract API)

    Entrées
    - urls : une URL ou une liste d'URL
    - query : filtre optionnel de focalisation

    Sortie
    - dictionnaire avec `count` et `items` contenant `url` et `content`
    """
    tavily_client = TavilyClient(api_key=project_settings.tavily_api_key)
    url_list = [urls] if isinstance(urls, str) else urls
    response_data = tavily_client.extract(urls=url_list, query=query or None)

    items = [
        {
            "url": result["url"],
            "content": result["raw_content"],
        }
        for result in response_data.get("results", [])
    ]
    return {
        "count": len(items),
        "items": items,
    }
