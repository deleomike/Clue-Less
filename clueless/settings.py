import os


class Settings:

    @property
    def BACKEND_PORT(self):
        return os.environ.get("BACKEND_PORT", 8000)

    @BACKEND_PORT.setter
    def BACKEND_PORT(self, value):
        os.environ["BACKEND_PORT"] = str(value)

    @property
    def BACKEND_HOST(self):
        return os.environ.get("BACKEND_HOST", "127.0.0.1")

    @BACKEND_HOST.setter
    def BACKEND_HOST(self, value):
        os.environ["BACKEND_HOST"] = str(value)

    @property
    def BACKEND_URL(self):
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"


settings = Settings()
