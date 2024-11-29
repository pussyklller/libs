
import asyncio
import platform
import subprocess
import sys
import logging
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
    system = platform.system()
    machine = platform.machine()
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return system, machine, python_version


class TestLoadLIB(loader.Library):
    developer = "@its_pussykiller"
    version = (2, 0, 0)
