# Thiago Alves Soares - 2502664
import pytest

from src.gerenciador_recursos import (
    AguaInsuficienteError,
    GerenciadorRecursosMarte,
    NivelEmergenciaInvalidoError,
    OxigenioInsuficienteError,
)


@pytest.mark.parametrize(
    "astronautas, consumo, nivel, esperado",
    [
        (1, 0.84, 1, 0.84),
        (4, 0.84, 1, 3.36),
        (6, 0.84, 2, 6.3),
        (6, 1.0, 3, 9.0),
        (10, 0.5, 4, 10.0),
    ],
)
def test_consumo_diario(gerenciador, astronautas, consumo, nivel, esperado):
    assert gerenciador.calcular_consumo_diario(astronautas, consumo, nivel) == pytest.approx(esperado)


@pytest.mark.parametrize("nivel, taxa", [(1, 1.0), (2, 1.25), (3, 1.5), (4, 2.0)])
def test_taxa_emergencia(gerenciador, nivel, taxa):
    assert gerenciador.calcular_taxa_emergencia(nivel) == taxa


@pytest.mark.parametrize("nivel", [0, 5, -1, 99])
def test_nivel_emergencia_invalido(gerenciador, nivel):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador.calcular_taxa_emergencia(nivel)


@pytest.mark.parametrize("astronautas, consumo", [(0, 0.84), (-2, 0.84), (3, -1.0)])
def test_consumo_com_entrada_invalida(gerenciador, astronautas, consumo):
    with pytest.raises(ValueError):
        gerenciador.calcular_consumo_diario(astronautas, consumo)


def test_estoque_inicial_negativo(telemetria):
    with pytest.raises(ValueError):
        GerenciadorRecursosMarte(-1, 10, telemetria)


def test_validar_estoque_suficiente(gerenciador):
    assert gerenciador.validar_estoque(500, 1000) is True


def test_oxigenio_insuficiente(gerenciador):
    with pytest.raises(OxigenioInsuficienteError):
        gerenciador.validar_estoque(1001)


def test_agua_insuficiente(gerenciador):
    with pytest.raises(AguaInsuficienteError):
        gerenciador.validar_estoque(10, 5001)


@pytest.mark.parametrize("consumo, cota, esperado", [(10, 1, 10), (10, 0.5, 5), (8, 0.25, 2)])
def test_racionamento(gerenciador, consumo, cota, esperado):
    assert gerenciador.aplicar_racionamento(consumo, cota) == pytest.approx(esperado)


@pytest.mark.parametrize("cota", [0, -0.1, 1.5])
def test_racionamento_cota_invalida(gerenciador, cota):
    with pytest.raises(ValueError):
        gerenciador.aplicar_racionamento(10, cota)


def test_pedido_extra_sem_alerta(gerenciador, telemetria):
    restante = gerenciador.solicitar_oxigenio_extra("Ana", 100)
    assert restante == 900
    telemetria.disparar_alerta.assert_not_called()


def test_pedido_extra_dispara_alerta_critico(gerenciador, telemetria):
    gerenciador.solicitar_oxigenio_extra("Ana", 950)
    telemetria.disparar_alerta.assert_called_once_with(
        "CRITICO", "Oxigênio em 50.0 após pedido de Ana"
    )


def test_pedido_extra_sem_estoque_nao_alerta(gerenciador, telemetria):
    with pytest.raises(OxigenioInsuficienteError):
        gerenciador.solicitar_oxigenio_extra("Ana", 5000)
    telemetria.disparar_alerta.assert_not_called()
    assert gerenciador.oxigenio == 1000


def test_pedido_extra_quantidade_invalida(gerenciador):
    with pytest.raises(ValueError):
        gerenciador.solicitar_oxigenio_extra("Ana", 0)


def test_envio_de_status_usa_resposta_da_estacao(gerenciador, telemetria):
    telemetria.enviar_relatorio.return_value = {"recebido": True}
    assert gerenciador.enviar_status() == {"recebido": True}
    telemetria.enviar_relatorio.assert_called_once_with({"oxigenio": 1000.0, "agua": 5000.0})
