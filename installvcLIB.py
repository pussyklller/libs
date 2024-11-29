import asyncio
import io
import logging
import typing
import platform
import sys
import subprocess
import requests
from telethon.errors.rpcerrorlist import BotResponseTimeoutError
from telethon.events import MessageEdited, StopPropagation
from telethon.tl.types import Document

import importlib.metadata
from .. import loader, utils


GITHUB_REPO = "https://github.com/pvssykiller/py-tgcalls_host/tree/main"

WHL_FILES = {
        ("Windows", "amd64", "3.11"): "py_tgcalls-0.9.7-cp311-cp311-win_amd64.whl",
        ("Windows", "amd64", "3.10"): "py_tgcalls-0.9.7-cp310-cp310-win_amd64.whl",
        ("Windows", "amd64", "3.9"): "py_tgcalls-0.9.7-cp39-cp39-win_amd64.whl",
        ("Windows", "amd64", "3.8"): "py_tgcalls-0.9.7-cp38-cp38-win_amd64.whl",
        ("Windows", "amd64", "3.7"): "py_tgcalls-0.9.7-cp37-cp37m-win_amd64.whl",

        ("Linux", "x86_64", "3.11"): "py_tgcalls-0.9.7-cp311-cp311-manylinux2014_x86_64.whl",
        ("Linux", "x86_64", "3.10"): "py_tgcalls-0.9.7-cp310-cp310-manylinux2014_x86_64.whl",
        ("Linux", "x86_64", "3.9"): "py_tgcalls-0.9.7-cp39-cp39-manylinux2014_x86_64.whl",
        ("Linux", "x86_64", "3.8"): "py_tgcalls-0.9.7-cp38-cp38-manylinux2014_x86_64.whl",
        ("Linux", "x86_64", "3.7"): "py_tgcalls-0.9.7-cp37-cp37m-manylinux2014_x86_64.whl",

        ("Linux", "armv7l", "3.11"): "py_tgcalls-0.9.7-cp311-cp311-manylinux2014_armv7l.whl",
        ("Linux", "armv7l", "3.10"): "py_tgcalls-0.9.7-cp310-cp310-manylinux2014_armv7l.whl",
        ("Linux", "armv7l", "3.9"): "py_tgcalls-0.9.7-cp39-cp39-manylinux2014_armv7l.whl",
        ("Linux", "armv7l", "3.8"): "py_tgcalls-0.9.7-cp38-cp38-manylinux2014_armv7l.whl",
        ("Linux", "armv7l", "3.7"): "py_tgcalls-0.9.7-cp37-cp37m-manylinux2014_armv7l.whl",

        ("Linux", "aarch64", "3.11"): "py_tgcalls-0.9.7-cp311-cp311-manylinux2014_aarch64.whl",
        ("Linux", "aarch64", "3.10"): "py_tgcalls-0.9.7-cp310-cp310-manylinux2014_aarch64.whl",
        ("Linux", "aarch64", "3.9"): "py_tgcalls-0.9.7-cp39-cp39-manylinux2014_aarch64.whl",
        ("Linux", "aarch64", "3.8"): "py_tgcalls-0.9.7-cp38-cp38-manylinux2014_aarch64.whl",
        ("Linux", "aarch64", "3.7"): "py_tgcalls-0.9.7-cp37-cp37m-manylinux2014_aarch64.whl",

        ("Darwin", "universal2", "3.11"): "py_tgcalls-0.9.7-cp311-cp311-macosx_10_9_universal2.whl",
        ("Darwin", "universal2", "3.10"): "py_tgcalls-0.9.7-cp310-cp310-macosx_10_9_universal2.whl",
        ("Darwin", "x86_64", "3.9"): "py_tgcalls-0.9.7-cp39-cp39-macosx_11_0_x86_64.whl",
        ("Darwin", "x86_64", "3.8"): "py_tgcalls-0.9.7-cp38-cp38-macosx_10_15_x86_64.whl",
        ("Darwin", "x86_64", "3.7"): "py_tgcalls-0.9.7-cp37-cp37m-macosx_10_15_x86_64.whl",
    }


def get_platform():
    """Определение платформы и архитектуры."""
    system =  platform.system()
    machine = platform.machine()
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return system, machine, python_version

async def install_pytg():
    """Установка подходящего файла .whl."""
    platform_info = get_platform()
    whl_file = WHL_FILES.get(platform_info)

    if not whl_file:
        logging.debug(f"Не найден подходящий файл для платформы: {platform_info}")
        return

    whl_url = f"{GITHUB_REPO}/{whl_file}"

    library_name, version = whl_file.split('-')[:2]

    try:
        installed_version = importlib.metadata.version(library_name)
        if installed_version == version:
            logging.debug(f"Библиотека {library_name} версии {version} уже установлена.")
            return
        else:
            logging.debug(f"Обнаружена версия {installed_version} библиотеки {library_name}. Переустанавливаем на версию {version}.")
    except importlib.metadata.PackageNotFoundError:
        logging.debug(f"Библиотека {library_name} не установлена. Устанавливаем версию {version}.")

    logging.debug(f"Устанавливаем: {whl_url}")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", whl_url])
        logging.debug("Установка завершена успешно!")
    except subprocess.CalledProcessError as e:
        logging.debug(f"Ошибка при установке: {e}")


