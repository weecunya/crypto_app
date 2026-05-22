from src.http_client import client
from src.http_client import APIClient
import asyncio
import pytest


@pytest.mark.asyncio
async def test_get_weather():
    assert await APIClient.get_weather('Moscow') == {"result":{"moscow":["2026-05-16: макс.темп.- 21.79,\nмин.темп.- 14.64, вероятность осадков-1%"]}}
    assert type(await APIClient.get_weather('Moscow')) == str


