
import asyncio
import platform
import subprocess
import sys
import logging
from .. import loader, utils


class TestLoadLIB(loader.Library):
    developer = "@its_pussykiller"
    version = (2, 0, 0)
