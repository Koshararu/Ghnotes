import os
import requests
from telethon import events, types
from .. import loader, utils

class UpdateGithubFilesMod(loader.Module):
    """Модуль для проверки новых файлов .py на GitHub репозитории"""

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.repo_owner = None
        self.repo_name = None

    async def update_files_command(self, message):
        """.ug - Проверить наличие новых файлов .py на GitHub репозитории"""
        config = self.db.get(name, {})
        repo_owner = config.get("repo_owner")
        repo_name = config.get("repo_name")
        if not repo_owner or not repo_name:
            await utils.answer(message, "Репозиторий не настроен. Используй .setrepo <владелец> <название репозитория> для настройки.")
            return

        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
        try:
            response = requests.get(url)
            response.raise_for_status()
            files = [item["name"] for item in response.json() if item["name"].endswith(".py")]
            
            if not files:
                await utils.answer(message, "В репозитории нет новых файлов .py.")
                return
            
            full_txt = "\n".join([os.path.splitext(file)[0] for file in files])
            with open("full.txt", "w", encoding="utf-8") as f:
                f.write(full_txt)
            
            await utils.answer(message, "Файл full.txt успешно создан с перечислением файлов .py в репозитории.")
        except requests.exceptions.RequestException as e:
            await utils.answer(message, f"Произошла ошибка при запросе к GitHub API: {e}")

    async def set_repo_command(self, message):
        """.setrepo <владелец> <название репозитория> - Установить репозиторий GitHub для проверки"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Укажите владельца и название репозитория.")
            return
        
        try:
            repo_owner, repo_name = args.split()
            self.db.set(name, {"repo_owner": repo_owner, "repo_name": repo_name})
            await utils.answer(message, f"Репозиторий успешно установлен: {repo_owner}/{repo_name}")
        except ValueError:
            await utils.answer(message, "Неверный формат. Используйте .setrepo <владелец> <название репозитория>")

    async def watcher(self, message):
        if isinstance(message, types.Message) and message.text.startswith(".setrepo"):
            # Clear repo settings if .setrepo is called to avoid confusion
            self.db.set(name, {"repo_owner": None, "repo_name": None})