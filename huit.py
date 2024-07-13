# -*- coding: utf-8 -*-

import json
import logging
import os

import requests
from .. import loader, utils

logger = logging.getLogger(name)


def register(cb):
    cb(GitChecker())


@loader.tds
class GitChecker(loader.Module):
    """Модуль для проверки новых файлов .py на GitHub репозитории"""

    strings = {
        "name": "GitChecker",
        "repo_not_set": "<b>Репозиторий не установлен. Используйте .setrepo &lt;владелец&gt; &lt;название репозитория&gt;</b>",
        "repo_set": "<b>Репозиторий успешно установлен: {owner}/{repo}</b>",
        "no_new_files": "На текущий момент новые файлы .py в репозитории не обнаружены.",
        "file_list_created": "Файл full.txt успешно создан с перечислением существующих файлов .py в репозитории.",
        "error_api": "<b>Ошибка при использовании GitHub API.</b>",
    }

    def init(self):
        self.config = loader.ModuleConfig(
            "GH_USERNAME",
            None,
            lambda m: self.strings("repo_not_set", m),
            "GH_REPO",
            None,
            lambda m: self.strings("repo_not_set", m),
        )

    async def client_ready(self, client, db):
        self.client = client

    @loader.owner
    async def setrepocmd(self, message):
        """Установить репозиторий для отслеживания"""
        args = utils.get_args(message)
        if len(args) != 2:
            await utils.answer(message, self.strings("repo_not_set", message))
            return
        owner = args[0]
        repo = args[1]
        self.config["GH_USERNAME"] = owner
        self.config["GH_REPO"] = repo
        await utils.answer(message, self.strings("repo_set", message).format(owner=owner, repo=repo))

    @loader.owner
    async def ugcmd(self, message):
        """Проверить наличие новых файлов .py в репозитории"""
        if not self.config["GH_USERNAME"] or not self.config["GH_REPO"]:
            await utils.answer(message, self.strings("repo_not_set", message))
            return

        owner = self.config["GH_USERNAME"]
        repo = self.config["GH_REPO"]
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/"

        try:
            response = requests.get(url)
            response.raise_for_status()
            files = [file["name"][:-3] for file in response.json() if file["name"].endswith(".py")]
            
            if not files:
                await utils.answer(message, self.strings("no_new_files", message))
                return

            file_content = "\n".join(files)
            with open("full.txt", "w", encoding="utf-8") as file:
                file.write(file_content)

            await utils.answer(message, self.strings("file_list_created", message))
        
        except requests.exceptions.RequestException:
            await utils.answer(message, self.strings("error_api", message))

    async def client_message(self, message):
        """Обработка событий входящих сообщений"""
        if message.text.startswith(".setrepo"):
            await self.setrepocmd(message)
        elif message.text.startswith(".ug"):
            await self.ugcmd(message)