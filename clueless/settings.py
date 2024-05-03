import os


class Settings:

    # def __init__(self):
    #     self.refresh_calculated()

    # def refresh_calculated(self):
        # self._update_backend_url_env()

    @property
    def BACKEND_PORT(self) -> int:
        return int(os.environ.get("BACKEND_PORT", 8000))

    @BACKEND_PORT.setter
    def BACKEND_PORT(self, value):
        os.environ["BACKEND_PORT"] = str(value)
        # self.refresh_calculated()

    @property
    def BACKEND_HOST(self) -> str:
        return os.environ.get("BACKEND_HOST", "127.0.0.1")

    @BACKEND_HOST.setter
    def BACKEND_HOST(self, value):
        os.environ["BACKEND_HOST"] = str(value)
        # self.refresh_calculated()

    @property
    def BACKEND_URL(self):
        val = f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"
        return val


settings = Settings()
