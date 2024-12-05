import subprocess
import os
from settings import DB_CONFIG

class BackupService:
    def __init__(self):
        self.db_name = DB_CONFIG["dbname"]
        self.user = DB_CONFIG["user"]
        self.password = DB_CONFIG["password"]
        self.host = DB_CONFIG["host"]
        self.port = DB_CONFIG["port"]

    def create_backup(self, backup_path: str):
        os.environ["PGPASSWORD"] = self.password

        backup_path_in_container = f"/backups/{os.path.basename(backup_path)}"
        
        try:
            subprocess.run(
                [
                    "docker",
                    "exec",
                    "-i",
                    "PostgresDB",
                    "pg_dump",
                    "-U", self.user,
                    "-F", "c",
                    "-b",
                    "-v",
                    "-f", backup_path_in_container,
                    self.db_name,
                ],
                check=True
            )
            return f"Резервная копия успешно создана: {backup_path}"
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ошибка при создании резервной копии: {e}")

    def restore_backup(self, backup_path: str):
        os.environ["PGPASSWORD"] = self.password
        
        backup_path_in_container = f"/backups/{os.path.basename(backup_path)}"

        try:
            subprocess.run(
                [
                    "docker",
                    "exec",
                    "-i",
                    "PostgresDB",
                    "pg_restore",
                    "-U", self.user,
                    "-d", self.db_name,
                    "-v",
                    backup_path_in_container,
                ],
                check=True
            )
            return "Данные успешно восстановлены из резервной копии."
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ошибка при восстановлении данных: {e}")
