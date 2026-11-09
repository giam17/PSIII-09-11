from pathlib import Path
import socket
import subprocess
import sys
import time

import httpx
import pytest
from fastapi.testclient import TestClient

from app import crud
from app.main import app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(crud, "_datos", {"categorias": [], "productos": []})
    with TestClient(app) as cliente:
        yield cliente


@pytest.fixture
def servidor():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        puerto = sock.getsockname()[1]

    proceso = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(puerto)],
        cwd=Path(__file__).resolve().parents[1],
    )

    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{puerto}", timeout=2, trust_env=False) as cliente:
            limite = time.monotonic() + 15
            while time.monotonic() < limite:
                if proceso.poll() is not None:
                    pytest.fail("El servidor no pudo iniciar")
                try:
                    if cliente.get("/categorias").status_code == 200:
                        break
                except httpx.TransportError:
                    pass
                time.sleep(0.1)
            else:
                pytest.fail("El servidor no respondio a tiempo")
            yield cliente
    finally:
        proceso.terminate()
        try:
            proceso.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proceso.kill()
            proceso.wait(timeout=5)
