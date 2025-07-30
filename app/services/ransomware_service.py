import json, httpx, textwrap
from app.core.config import get_settings
from typing import Optional
BASE = get_settings().ransomware_live_base
TIMEOUT = 120  # seconds

def _client():
    return httpx.AsyncClient(
        base_url=BASE,
        timeout=httpx.Timeout(TIMEOUT),
        headers={"User-Agent": "Cyber-Groq-Ransomware/1.0.0"},
    )

async def get_api_info():
    async with _client() as c:
        return (await c.get("/info")).json()

async def get_recent_victims(limit: int = 10):
    async with _client() as c:
        return (await c.get("/recentvictims", params={"limit": limit})).json()

async def get_group_info(group: str):
    async with _client() as c:
        return (await c.get(f"/group/{group}")).json()

async def get_all_groups():
    async with _client() as c:
        return (await c.get("/groups")).json()

async def get_all_cyberattacks(limit: int = 10):
    async with _client() as c:
        return (await c.get("/allcyberattacks", params={"limit": limit})).json()

async def get_recent_cyberattacks(limit: int = 10):
    async with _client() as c:
        return (await c.get("/recentcyberattacks", params={"limit": limit})).json()

async def get_group_victims(group: str):
    async with _client() as c:
        return (await c.get(f"/groupvictims/{group}")).json()

async def search_victims(keyword: str, limit: int = 10):
    async with _client() as c:
        return (await c.get(f"/searchvictims/{keyword}", params={"limit": limit})).json()

async def get_country_attacks(countryCode: str):
    async with _client() as c:
        return (await c.get(f"/countrycyberattacks/{countryCode.upper()}")).json()

async def get_country_victims(countryCode: str):
    async with _client() as c:
        return (await c.get(f"/countryvictims/{countryCode.upper()}")).json()

async def get_victims_by_date(year: int, month: int):
    async with _client() as c:
        return (await c.get(f"/victims/{year}/{month}")).json()

async def get_sector_victims(sector: str, countryCode: Optional[str] = None):
    endpoint = f"/sectorvictims/{sector}"
    if countryCode:
        endpoint += f"/{countryCode.upper()}"
    async with _client() as c:
        return (await c.get(endpoint)).json()

async def get_cert_contacts(countryCode: str):
    async with _client() as c:
        return (await c.get(f"/certs/{countryCode.upper()}")).json()

async def get_yara_rules(group: str):
    async with _client() as c:
        r = await c.get(f"/yara/{group}")
        if r.status_code == 204 or not r.text.strip():
            return {
                "error": f"No YARA rules returned for '{group}'.",
                "note": "Either the group has no rules or the endpoint is empty right now."
            }
        try:
            return r.json()
        except json.JSONDecodeError:
            # sometimes the API returns plain text — send it back
            return {"raw": textwrap.shorten(r.text, 200)}