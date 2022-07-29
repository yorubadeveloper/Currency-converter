import os
from dotenv import load_dotenv
import aioredis
from fastapi import FastAPI, APIRouter, Depends, Path
from fastapi.security.api_key import APIKey
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import schemas
import helper
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_utils.tasks import repeat_every
load_dotenv()

REDIS_URL = os.environ.get('REDIS_URL')

app = FastAPI()


# Setup for using Redis together with FASTAPI CACHE to cache requests
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# Runs every day async to fetch currencies and update currencies.json file
@app.on_event("startup")
@repeat_every(seconds=86400)
async def fetch_currencies():
    helper.fetch_currencies_from_api()

# Application middleware to avoid cross-origin errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter(prefix="/api/v1")


# Get all currencies route
@router.get("/currencies", response_model=schemas.SupportedCurrencies)
@cache(expire=3600)
async def get_currencies(api_key: APIKey = Depends(helper.get_api_key)):
    return helper.get_all_currencies()


# Get exchange rate and convert route
@router.get("/currencies/convert/{base}/{to}/{amount}", response_model=schemas.ConvertCurrencies)
async def convert_currencies(api_key: APIKey = Depends(helper.get_api_key),
                             base: str = Path(
                                 ...,
                                 title="Base currency",
                                description="Base currency for conversion",
                             ),
                             to: str = Path(
                                 ...,
                                 title="Target currency",
                                description="Target currency for conversion",
                             ),
                             amount: float = Path(
                                 ...,
                                 gt=0,
                                 title="Amount of money",
                                 description="Amount of money that going to be converted",
                             )
                             ):
    exchange_rate = helper.fetch_rates_from_api(base, to)
    result = helper.convert_currencies(amount, exchange_rate)

    return {
        "base": base,
        "to": to,
        "amount": amount,
        "exchange_rate": exchange_rate,
        "result": result,
    }


app.include_router(router)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info")
