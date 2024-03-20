from uuid import uuid4, UUID
from fastapi import Depends, HTTPException, Response, Request
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend

from clueless.app.core.session.SessionData import SessionCreate, SessionData
from clueless.app.core.session.BasicVerifier import BasicVerifier
# from clueless.app.core.session import SessionCreate, SessionData, BasicVerifier


class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


# @singleton
class SessionCRUD(Singleton):

    def __init__(self,
                 cookie_params: CookieParameters = None,
                 cookie: SessionCookie = None,
                 backend: InMemoryBackend = None):

        self.cookie_params = CookieParameters() if cookie_params is None else cookie_params

        # Uses UUID
        if cookie:
            self.cookie = cookie
        else:
            self.cookie = SessionCookie(
                cookie_name="cookie",
                identifier="general_verifier",
                auto_error=True,
                secret_key="DONOTUSE",
                cookie_params=self.cookie_params,
            )

        self.backend = InMemoryBackend[UUID, SessionData]() if backend is None else backend

        self.verifier = BasicVerifier(
            identifier="general_verifier",
            auto_error=True,
            backend=self.backend,
            auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
        )

    async def create(self, data: SessionCreate, response: Response) -> SessionData:
        data = SessionData(username=data.username)

        await self.backend.create(data.id, data)
        self.cookie.attach_to_response(response, data.id)

        print(f"created session for {data.username}")

        return data

    async def delete(self, response: Response, session_id: UUID) -> bool:
        await self.backend.delete(session_id)
        self.cookie.delete_from_response(response)
        return True

    async def whoami(self, reqeust: Request) -> SessionData:
        return await self.verifier(request=reqeust)

    def get(self, session_data: SessionData) -> SessionData:
        self.verifier.verify_session(session_data)
        return session_data


session = SessionCRUD()


