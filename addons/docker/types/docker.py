from typing import TypedDict, Optional, List, Union, Dict, Any


class DockerComposeHealthcheck(TypedDict, total=False):
    test: Union[str, List[str]]
    interval: Optional[str]
    timeout: Optional[str]
    retries: Optional[int]
    start_period: Optional[str]


class DockerComposeDeploy(TypedDict, total=False):
    mode: Optional[str]
    replicas: Optional[int]
    labels: Optional[List[str]]
    update_config: Optional[Dict[str, Union[str, int]]]
    resources: Optional[Dict[str, Dict[str, Dict[str, int]]]]
    restart_policy: Optional[Dict[str, Union[str, int]]]


class DockerComposeService(TypedDict, total=False):
    container_name: Optional[str]
    environment: Optional[Union[List[str], Dict[str, str]]]
    image: Optional[str]
    build: Optional[Union[str, Dict[str, Union[str, List[str]]]]]
    command: Optional[Union[str, List[str]]]
    entrypoint: Optional[Union[str, List[str]]]
    ports: Optional[List[str]]
    volumes: Optional[List[str]]
    networks: Optional[List[str]]
    depends_on: Optional[List[str]]
    privileged: Optional[bool]
    restart: Optional[str]
    stdin_open: Optional[bool]
    tty: Optional[bool]
    deploy: Optional[DockerComposeDeploy]
    healthcheck: Optional[DockerComposeHealthcheck]


class DockerComposeNetwork(TypedDict, total=False):
    driver: Optional[str]
    driver_opts: Optional[Dict[str, str]]
    ipam: Optional[Dict[str, Any]]
    external: Optional[bool]


class DockerComposeVolume(TypedDict, total=False):
    driver: Optional[str]
    driver_opts: Optional[Dict[str, str]]
    external: Optional[bool]


class DockerCompose(TypedDict, total=False):
    version: str
    services: Dict[str, DockerComposeService]
    networks: Optional[Dict[str, DockerComposeNetwork]]
    volumes: Optional[Dict[str, DockerComposeVolume]]
