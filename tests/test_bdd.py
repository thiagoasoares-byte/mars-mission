# Thiago Alves Soares - 2502664
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.gerenciador_recursos import GerenciadorRecursosMarte, OxigenioInsuficienteError

scenarios("features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto():
    return {}


@given(parsers.parse("um habitat com {estoque:d} kg de oxigênio em estoque"))
def habitat(contexto, telemetria, estoque):
    contexto["gerenciador"] = GerenciadorRecursosMarte(estoque, 5000, telemetria)


@when(parsers.parse('o astronauta "{nome}" solicita {quantidade:d} kg de oxigênio extra'))
def solicitar(contexto, nome, quantidade):
    try:
        contexto["gerenciador"].solicitar_oxigenio_extra(nome, quantidade)
    except OxigenioInsuficienteError as erro:
        contexto["erro"] = erro


@then(parsers.parse("o estoque de oxigênio passa a ser {estoque:d} kg"))
def estoque_final(contexto, estoque):
    assert contexto["gerenciador"].oxigenio == estoque


@then("um alerta de crise é enviado à Terra")
def alerta_enviado(telemetria):
    telemetria.disparar_alerta.assert_called_once()


@then("nenhum alerta de crise é enviado à Terra")
def alerta_nao_enviado(telemetria):
    telemetria.disparar_alerta.assert_not_called()


@then("a solicitação é recusada por oxigênio insuficiente")
def recusada(contexto):
    assert isinstance(contexto["erro"], OxigenioInsuficienteError)
