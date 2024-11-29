
import asyncio
import platform
import subprocess
import sys
import logging
import importlib.metadata
from .. import loader, utils


def get_platform():
    """Определение платформы и архитектуры."""
    system = platform.system()
    machine = platform.machine()
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return system, machine, python_version


class TestLoadLIB(loader.Library):
    developer = "@its_pussykiller"
    version = (2, 0, 0)
