from __future__ import annotations

from typing import Any, TypedDict


class DockerComposeHealthcheck(TypedDict, total=False):
    interval: str | None
    retries: int | None
    start_period: str | None
    test: str | list[str]
    timeout: str | None


class DockerComposeDeploy(TypedDict, total=False):
    labels: list[str] | None
    mode: str | None
    replicas: int | None
    resources: dict[str, dict[str, dict[str, int]]] | None
    restart_policy: dict[str, str | int] | None
    update_config: dict[str, str | int] | None


class DockerComposeService(TypedDict, total=False):
    build: str | dict[str, str | list[str]] | None
    command: str | list[str] | None
    container_name: str | None
    depends_on: list[str] | None
    deploy: DockerComposeDeploy | None
    entrypoint: str | list[str] | None
    environment: list[str] | dict[str, str] | None
    healthcheck: DockerComposeHealthcheck | None
    image: str | None
    networks: list[str] | None
    ports: list[str] | None
    privileged: bool | None
    restart: str | None
    stdin_open: bool | None
    tty: bool | None
    volumes: list[str] | None


class DockerComposeNetwork(TypedDict, total=False):
    driver: str | None
    driver_opts: dict[str, str] | None
    external: bool | None
    ipam: dict[str, Any] | None


class DockerComposeVolume(TypedDict, total=False):
    driver: str | None
    driver_opts: dict[str, str] | None
    external: bool | None


class DockerCompose(TypedDict, total=False):
    networks: dict[str, DockerComposeNetwork] | None
    services: dict[str, DockerComposeService]
    version: str
    volumes: dict[str, DockerComposeVolume] | None
