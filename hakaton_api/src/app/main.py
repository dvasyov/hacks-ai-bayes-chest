# -*- coding: utf-8 -*-
import asyncio

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from src.app.api.v1.api import v1_router
from src.app.core import config

sentry_sdk.init(config.SENTRY_DSN)

app = FastAPI(
    debug=config.DEBUG,
    title=config.APP_TITLE,
    version=config.APP_VERSION,
    redoc_url=None,
)

app.include_router(v1_router)
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(ProxyHeadersMiddleware)


async def main():
    uvicorn.run(
        app="main:app",
        debug=config.DEBUG,
        access_log=config.ACCESS_LOG,
        log_level=config.LOG_LEVEL,
        log_config=config.LOGGING_CONFIG,
        limit_concurrency=config.APP_LIMIT_CONCURRENCY,
        limit_max_requests=config.APP_LIMIT_MAX_REQUESTS,
        workers=config.APP_WORKERS,
        host=config.HOST,
        port=config.PORT,
        loop="uvloop",
        interface="asgi3",
        lifespan="off",
        http="httptools",
        timeout_keep_alive=config.TIMEOUT_KEEPALIVE,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
