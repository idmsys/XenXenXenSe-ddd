from typing import Optional

import uvicorn
from fastapi import FastAPI


class Server(FastAPI):
    def __init__(
        self,
        ctx,
        host: str,
        port: int,
        title: str,
        description: str,
        log_config,
        dependencies=None,
        asgi_debug: bool = False,
        debug: bool = False,
        sock: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        self.controller = ctx

        # ASGI Server configuration parameters
        self.server = uvicorn
        self._host = host
        self._port = port
        self._sock = sock
        self._title = title
        self._description = description
        self.dependencies = dependencies
        self._log_config = log_config
        self._debug = debug
        self._exception_debug = debug
        self._asgi_debug = asgi_debug
        super().__init__(*args, **kwargs)

    def make_process(self):
        _connect_option = {
            "host": self._host,
            "port": self._port,
        }

        if self._sock is not None:
            _connect_option = {"uds": self._sock}

        self.server.run(
            app=self,
            # https://github.com/encode/uvicorn/pull/1640
            # debug=self._asgi_debug,
            log_config=self._log_config,
            **_connect_option,
        )
