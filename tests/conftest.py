# Thiago Alves Soares - 2502664
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.gerenciador_recursos import GerenciadorRecursosMarte
from src.servico_telemetria import ServicoTelemetriaEspacial

RAIZ = Path(__file__).resolve().parent.parent
PAINEL_URL = (RAIZ / "web" / "painel.html").as_uri()
PASTA_EVIDENCIAS = RAIZ / "screenshots"


@pytest.fixture(scope="module")
def parametros_habitat():
    return {"oxigenio": 1000.0, "agua": 5000.0, "astronautas": 6, "consumo_o2": 0.84}


@pytest.fixture
def telemetria(mocker):
    return mocker.create_autospec(ServicoTelemetriaEspacial, instance=True)


@pytest.fixture
def gerenciador(parametros_habitat, telemetria):
    instancia = GerenciadorRecursosMarte(
        parametros_habitat["oxigenio"], parametros_habitat["agua"], telemetria
    )
    yield instancia
    instancia.oxigenio = 0.0
    instancia.agua = 0.0


@pytest.fixture
def driver(request):
    opcoes = Options()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1280,900")
    navegador = webdriver.Chrome(options=opcoes)
    request.node.driver = navegador
    yield navegador
    navegador.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    relatorio = resultado.get_result()
    navegador = getattr(item, "driver", None)
    if relatorio.when == "call" and relatorio.failed and navegador is not None:
        PASTA_EVIDENCIAS.mkdir(exist_ok=True)
        navegador.save_screenshot(str(PASTA_EVIDENCIAS / f"{item.name}.png"))
