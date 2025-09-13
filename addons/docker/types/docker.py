from __future__ import annotations

from typing import Any, TypedDict


class DockerComposeHealthcheck(TypedDict, total=False):
    test: str | list[str]
    interval: str | None
    timeout: str | None
    retries: int | None
    start_period: str | None


class DockerComposeDeploy(TypedDict, total=False):
    mode: str | None
    replicas: int | None
    labels: list[str] | None
    update_config: dict[str, str | int] | None
    resources: dict[str, dict[str, dict[str, int]]] | None
    restart_policy: dict[str, str | int] | None


class DockerComposeService(TypedDict, total=False):
    container_name: str | None
    environment: list[str] | dict[str, str] | None
    image: str | None
    build: str | dict[str, str | list[str]] | None
    command: str | list[str] | None
    entrypoint: str | list[str] | None
    ports: list[str] | None
    volumes: list[str] | None
    networks: list[str] | None
    depends_on: list[str] | None
    privileged: bool | None
    restart: str | None
    stdin_open: bool | None
    tty: bool | None
    deploy: DockerComposeDeploy | None
    healthcheck: DockerComposeHealthcheck | None


class DockerComposeNetwork(TypedDict, total=False):
    driver: str | None
    driver_opts: dict[str, str] | None
    ipam: dict[str, Any] | None
    external: bool | None


class DockerComposeVolume(TypedDict, total=False):
    driver: str | None
    driver_opts: dict[str, str] | None
    external: bool | None


class DockerCompose(TypedDict, total=False):
    version: str
    services: dict[str, DockerComposeService]
    networks: dict[str, DockerComposeNetwork] | None
    volumes: dict[str, DockerComposeVolume] | None
