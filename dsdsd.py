import asyncio
import platform
import sys
import logging
from .. import loader


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


class TestLoadLIB(loader.Library):
    """Library for installing Py-TgCalls"""

    developer = "@its_pussykiller"
    version = (2, 0, 0)

    async def client_ready(self):
        """
        Метод, вызываемый, когда клиент готов. Проверяет, установлена ли библиотека,
        и выполняет установку, если необходимо.
        """
        try:
            await self.install_pytg()
        except Exception as e:
            raise loader.LoadError(f"Ошибка загрузки библиотеки: {e}")

    def get_platform(self):
        """
        Определение платформы и архитектуры для выбора подходящего файла.
        """
        system = platform.system()
        machine = platform.machine()
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        return system, machine, python_version

    async def run_command(self, command: list):
        """
        Выполнение системной команды в асинхронном режиме.
        """
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Команда завершилась ошибкой: {stderr.decode().strip()}")
        return stdout.decode().strip()

    async def install_pytg(self):
        """
        Установка библиотеки Py-TgCalls, если она отсутствует или версия не соответствует.
        """
        platform_info = self.get_platform()
        whl_file = WHL_FILES.get(platform_info)

        if not whl_file:
            logging.error(f"Не найден подходящий файл для платформы: {platform_info}")
            return

        whl_url = f"{GITHUB_REPO}/{whl_file}"
        command = [sys.executable, "-m", "pip", "install", "--force-reinstall", whl_url]

        try:
            logging.info(f"Начинаем установку библиотеки из {whl_url}")
            output = await self.run_command(command)
            logging.info(f"Успешная установка: {output}")
        except Exception as e:
            raise loader.LoadError(f"Ошибка при установке библиотеки: {e}")

