import os
from functools import lru_cache
from typing import Any, Literal

from supabase import Client, create_client

PredictionTable = Literal["fare_predictions", "delay_predictions"]


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not service_role_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be configured "
            "for prediction storage."
        )

    return create_client(supabase_url, service_role_key)


def insert_prediction(table: PredictionTable, values: dict[str, Any]) -> None:
    get_supabase_client().table(table).insert(values).execute()


def fetch_predictions(table: PredictionTable) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    page_size = 1000
    start = 0

    while True:
        response = (
            get_supabase_client()
            .table(table)
            .select("*")
            .order("id")
            .range(start, start + page_size - 1)
            .execute()
        )
        rows.extend(response.data)
        if len(response.data) < page_size:
            return rows
        start += page_size
