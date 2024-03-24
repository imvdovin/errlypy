from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPConnectionKey:
    kind = "http_connection_key"
    value: str


@dataclass(frozen=True)
class HTTPConnectionSecretKey:
    kind = "http_connection_secret_key"
    value: str


@dataclass(frozen=True)
class HTTPConnectionURL:
    kind = "http_connection_url"
    value: str


@dataclass(frozen=True)
class HTTPConnection:
    key: HTTPConnectionKey
    secret_key: HTTPConnectionSecretKey
    url: HTTPConnectionURL
