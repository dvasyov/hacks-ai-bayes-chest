"""
Модуль для загрузки конфигов.

Включает в себя:
- конфиг логеров
- загрузку переменных окружения
- загрузку значений из .yml конфига
"""
import os
import time
from pathlib import Path

import yaml

os.environ["TZ"] = "Asia/Yekaterinburg"
time.tzset()

CONFIG_FILE = "config.yml"
CURRENT_DIR = Path(__file__).resolve().parent
YAML_CONFIG_PATH = CURRENT_DIR.joinpath(CONFIG_FILE)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": str(
                {
                    "timestamp": "%(asctime)s",
                    "level": "%(levelname)s",
                    "message": "%(message)s",
                }
            ),
            "datefmt": "%d/%m/%Y %H:%M:%S",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": str(
                {
                    "timestamp": "%(asctime)s",
                    "level": "%(levelname)s",
                    "message": {
                        "status_code": "%(status_code)s",
                        "client_addr": "%(client_addr)s",
                        "request": "%(request_line)s",
                    },
                }
            ),
            "datefmt": "%d/%m/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}


def _load_yaml_cfg(path):
    try:
        with open(path, "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            return cfg
    except FileNotFoundError:  # Set default config if not found
        import logging.config

        logger = logging.getLogger("uvicorn.error")
        logging.config.dictConfig(LOGGING_CONFIG)
        msg = f"{YAML_CONFIG_PATH} not found. Using default config."
        logger.warning(msg)
        return {}


_yaml_cfg = _load_yaml_cfg(YAML_CONFIG_PATH)

APP_TITLE = "API для хакатона"
APP_VERSION = os.environ.get("APP_VERSION", "v0.1")
API_TOKEN = os.environ.get("API_TOKEN")
HOST = "0.0.0.0"
PORT = 8090
SENTRY_DSN = os.environ.get("SENTRY_DSN")

TIMEOUT_KEEPALIVE = _yaml_cfg.get("timeout_keepalive") or 10

DEBUG = _yaml_cfg.get("debug") or False
ACCESS_LOG = _yaml_cfg.get("access_log") or True
LOG_LEVEL = _yaml_cfg.get("log_level") or ("debug" if DEBUG else "error")
APP_WORKERS = _yaml_cfg.get("workers") or 1
APP_LIMIT_CONCURRENCY = _yaml_cfg.get("limit_concurrency")
APP_LIMIT_MAX_REQUESTS = _yaml_cfg.get("limit_max_requests")
