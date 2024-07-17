# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: ArchiveExtractor
# Description: Extracts files from various archive formats
# Author: ChatGPT
# Commands:
# .extract
# ---------------------------------------------------------------------------------

import shutil
import tarfile
import zipfile
import os

from .. import loader, utils

try:
    import py7zr
    import rarfile
except ImportError:
    os.system("pip install py7zr rarfile")
    import py7zr
    import rarfile

class ArchiveExtractor(loader.Module):
    """Extracts files from various archive formats"""

    strings = {
        "name": "ArchiveExtractor",
        "reply_to_archive": "<b>Reply to an archive file to extract it</b>",
        "unsupported_format": "<b>Unsupported file format</b>",
        "extracting": "<b>Extracting...</b>",
        "extracted": "<b>Extraction complete: {}</b>",
        "extraction_failed": "<b>Extraction failed: {}</b>"
    }

    async def extractcmd(self, message):
        """Extracts the replied archive file"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings("reply_to_archive", message))
            return
        
        file = await message.client.download_media(reply.media)
        await utils.answer(message, self.strings("extracting", message))

        try:
            if file.endswith(".zip"):
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall()
            elif file.endswith((".tar.gz", ".tgz", ".tar", ".gz", ".bz2", ".xz")):
                with tarfile.open(file, 'r:*') as tar_ref:
                    tar_ref.extractall()
            elif file.endswith(".7z"):
                with py7zr.SevenZipFile(file, mode='r') as z:
                    z.extractall()
            elif file.endswith(".rar"):
                with rarfile.RarFile(file, 'r') as rar_ref:
                    rar_ref.extractall()
            else:
                os.remove(file)
                await utils.answer(message, self.strings("unsupported_format", message))
                return

            extracted_files = [f for f in os.listdir() if os.path.isfile(f)]
            extracted_dirs = [d for d in os.listdir() if os.path.isdir(d)]
            extracted_items = extracted_files + extracted_dirs

            if extracted_items:
                await utils.answer(message, self.strings("extracted", message).format(", ".join(extracted_items)))
            else:
                await utils.answer(message, self.strings("extraction_failed", message).format("No files extracted"))
        except Exception as e:
            await utils.answer(message, self.strings("extraction_failed", message).format(str(e)))
        finally:
            if os.path.exists(file):
                os.remove(file)