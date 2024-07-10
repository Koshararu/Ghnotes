import base64
import json
import logging
import os

import requests
from requests.exceptions import ChunkedEncodingError, MissingSchema

from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(GitaddMod())


@loader.tds
class GitaddMod(loader.Module):
    """Загружает файлы на репозиторий GitHub"""

    strings = {
        "name": "GitUploader",
        "reply_to_file": "<b>Ответьте на файл</b>",
        "error_file": "Формат не поддерживается",
        "connection_error": "<i>Ошибка соединения</i>",
        "repo_error": "<i>Ошибка репозитория</i>",
        "token_error": "<i>Ошибка токена</i>",
        "exist_422": (
            "<b>Не удалось загрузить файл. Возможная причина: файл с таким названием"
            " уже существует в репозитории.</b>"
        ),
        "cfg_token": "Токен GitHub",
        "token_not_found": "Токен не найден",
        "username_not_found": "Имя пользователя GitHub не указано",
        "repo_not_found": "Репозиторий не указан",
        "cfg_gh_user": "Имя пользователя на GitHub",
        "cfg_gh_repo": "Репозиторий, куда нужно загружать модули",
        "list_files_header": "<b>Список файлов в репозитории:</b>\n",
        "no_files_found": "<i>Файлы не найдены в репозитории.</i>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "GH_TOKEN",
            "TOKEN",
            lambda m: self.strings("cfg_token", m),
            "GH_USERNAME",
            "USERNAME",
            lambda m: self.strings("cfg_gh_user", m),
            "GH_REPO",
            "REPOSITORY",
            lambda m: self.strings("cfg_gh_repo", m),
        )

    async def client_ready(self, client, db):
        self.client = client

    async def update_full_txt(self, username, repo, existing_files):
        try:
            url = f"https://api.github.com/repos/{username}/{repo}/contents/full.txt"
            head = {
                "Authorization": f"token {self.config['GH_TOKEN']}",
                "Accept": "application/vnd.github.v3+json",
            }
            if not existing_files:
                content = ""
            else:
                content = "\n".join(existing_files)

            encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
            commit_message = "Update full.txt"

            git_data = {
                "message": commit_message,
                "content": encoded_content,
                "sha": r.json()["sha"] if r.status_code == 200 else None,
            }

            r = requests.put(url, headers=head, data=json.dumps(git_data))
            return r.status_code == 200
        except Exception as e:
            logger.error(f"Failed to update full.txt: {e}")
            return False

    async def list_files_in_repo(self, username, repo):
        try:
            url = f"https://api.github.com/repos/{username}/{repo}/contents"
            head = {
                "Authorization": f"token {self.config['GH_TOKEN']}",
                "Accept": "application/vnd.github.v3+json",
            }
            r = requests.get(url, headers=head)
            if r.status_code == 200:
                files = [item["name"] for item in r.json() if item["type"] == "file"]
                return files
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to list files in repo: {e}")
            return None

    @loader.owner
    async def gitlistcmd(self, message):
        if self.config["GH_TOKEN"] == "TOKEN":
            await utils.answer(message, self.strings("token_not_found", message))
            return
        if self.config["GH_USERNAME"] == "USERNAME":
            await utils.answer(message, self.strings("username_not_found", message))
            return
        if self.config["GH_REPO"] == "REPOSITORY":
            await utils.answer(message, self.strings("repo_not_found", message))
            return

        username = self.config["GH_USERNAME"]
        repo = self.config["GH_REPO"]

        files = await self.list_files_in_repo(username, repo)

        if files is None:
            await utils.answer(message, self.strings("repo_error", message))
            return
        elif not files:
            await utils.answer(message, self.strings("no_files_found", message))
            return
        else:
            files_str = "\n".join(files)
            await utils.answer(message, f"{self.strings('list_files_header', message)}{files_str}")

    @loader.owner
    async def gitcheckcmd(self, message):
        if self.config["GH_TOKEN"] == "TOKEN":
            await utils.answer(message, self.strings("token_not_found", message))
            return
        if self.config["GH_USERNAME"] == "USERNAME":
            await utils.answer(message, self.strings("username_not_found", message))
            return
        if self.config["GH_REPO"] == "REPOSITORY":
            await utils.answer(message, self.strings("repo_not_found", message))
            return

        username = self.config["GH_USERNAME"]
        repo = self.config["GH_REPO"]

        # Проверяем наличие файла full.txt
        full_txt_exists = await self.list_files_in_repo(username, repo)
        if "full.txt" not in full_txt_exists:
            try:
                url = f"https://api.github.com/repos/{username}/{repo}/contents/full.txt"
                head = {
                    "Authorization": f"token {self.config['GH_TOKEN']}",
                    "Accept": "application/vnd.github.v3+json",
                }
                content = ""

                encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
                commit_message = "Create full.txt"

                git_data = {
                    "message": commit_message,
                    "content": encoded_content,
                }

                r = requests.put(url, headers=head, data=json.dumps(git_data))
                if r.status_code == 201:
                    await utils.answer(message, "Файл full.txt успешно создан.")
                else:
                    await utils.answer(message, "Не удалось создать файл full.txt.")
            except Exception as e:
                logger.error(f"Failed to create full.txt: {e}")
                await utils.answer(message, "Произошла ошибка при создании full.txt.")
            return

        # Получаем текущие имена файлов в репозитории
        current_files = await self.list_files_in_repo(username, repo)

        if current_files is None:
            await utils.answer(message, self.strings("repo_error", message))
            return

        # Проверяем, нужно ли обновить файл full.txt
        full_txt_url = f"https://raw.githubusercontent.com/{username}/{repo}/main/full.txt"
        try:
            r = requests.get(full_txt_url)
            if r.status_code == 200:
                content = r.text.strip().split("\n")
                existing_files = [line.strip() for line in content if line.strip()]
            else:
                existing_files = []
        except Exception as e:
            logger.error(f"Failed to fetch full.txt: {e}")
            existing_files = []

        files_to_update = list(set(existing_files) - set(current_files))

        if files_to_update:
            try:
                url = f"https://api.github.com/repos/{username}/{repo}/contents/full.txt"
                head = {
                    "Authorization": f"token {self.config['GH_TOKEN']}",
                    "Accept": "application/vnd.github.v3+json",
                }

                new_content = "\n".join(current_files)
                encoded_content = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
                commit_message = "Update full.txt"

                git_data = {
                    "message": commit_message,
                    "content": encoded_content,
                    "sha": r.json()["sha"] if r.status_code == 200 else None,
                }

                r = requests.put(url, headers=head, data=json.dumps(git_data))
                if r.status_code == 200:
                    await utils.answer(message, "Файл full.txt успешно обновлен.")
                else:
                    await utils.answer(message, "Не удалось обновить файл full.txt.")
            except Exception as e:
                logger.error(f"Failed to update full.txt: {e}")
                await utils.answer(message, "Произошла ошибка при обновлении full.txt.")
        else:
            await utils.answer(message, "Файл full.txt не требует обновления.")

    async def update_full_txt(self, username, repo, existing_files):
        try:
            url = f"https://api.github.com/repos/{username}/{repo}/contents/full.txt"
            head = {
                "Authorization": f"token {self.config['GH_TOKEN']}",
                "Accept": "application/vnd.github.v3+json
          
