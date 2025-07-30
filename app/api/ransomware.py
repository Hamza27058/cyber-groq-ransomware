from fastapi import APIRouter, HTTPException
from app.models.schemas import *
from app.services import ransomware_service as rs

router = APIRouter(prefix="/ransomware", tags=["Ransomware Tools"])

@router.get("/info")
async def api_info():
    return await rs.get_api_info()

@router.get("/victims/recent")
async def recent_victims(limit: int = 10):
    return await rs.get_recent_victims(limit)

@router.get("/groups")
async def all_groups():
    return await rs.get_all_groups()

@router.get("/groups/{group}")
async def group_info(group: str):
    return await rs.get_group_info(group)

@router.get("/groups/{group}/victims")
async def group_victims(group: str):
    return await rs.get_group_victims(group)

@router.get("/attacks")
async def all_attacks(limit: int = 10):
    return await rs.get_all_cyberattacks(limit)

@router.get("/attacks/recent")
async def recent_attacks(limit: int = 10):
    return await rs.get_recent_cyberattacks(limit)

@router.get("/victims/search")
async def search(keyword: str, limit: int = 10):
    return await rs.search_victims(keyword, limit)

@router.get("/country/{countryCode}/attacks")
async def country_attacks(countryCode: str):
    return await rs.get_country_attacks(countryCode)

@router.get("/country/{countryCode}/victims")
async def country_victims(countryCode: str):
    return await rs.get_country_victims(countryCode)

@router.get("/date/{year}/{month}/victims")
async def victims_by_date(year: int, month: int):
    return await rs.get_victims_by_date(year, month)

@router.get("/sector/{sector}/victims")
async def sector_victims(sector: str, countryCode: str = None):
    return await rs.get_sector_victims(sector, countryCode)

@router.get("/country/{countryCode}/cert")
async def cert_contacts(countryCode: str):
    return await rs.get_cert_contacts(countryCode)

@router.get("/groups/{group}/yara")
async def yara_rules(group: str):
    return await rs.get_yara_rules(group)