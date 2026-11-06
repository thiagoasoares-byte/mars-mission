# Thiago Alves Soares - 2502664
import io
import json

import pytest

from src.servico_telemetria import FalhaTelemetriaError, ServicoTelemetriaEspacial


def test_enviar_relatorio_posta_json(mocker):
    resposta = mocker.MagicMock()
    resposta.__enter__.return_value = io.BytesIO(json.dumps({"ok": True}).encode())
    abrir = mocker.patch("src.servico_telemetria.urllib.request.urlopen", return_value=resposta)

    assert ServicoTelemetriaEspacial("http://x").enviar_relatorio({"oxigenio": 1}) == {"ok": True}
    requisicao = abrir.call_args.args[0]
    assert requisicao.full_url == "http://x/relatorio"
    assert json.loads(requisicao.data) == {"oxigenio": 1}


def test_falha_de_rede_vira_excecao_propria(mocker):
    mocker.patch("src.servico_telemetria.urllib.request.urlopen", side_effect=OSError("sem sinal"))
    with pytest.raises(FalhaTelemetriaError):
        ServicoTelemetriaEspacial("http://x").disparar_alerta("CRITICO", "teste")
