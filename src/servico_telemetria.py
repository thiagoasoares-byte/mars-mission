# Thiago Alves Soares - 2502664
import json
import urllib.request


class FalhaTelemetriaError(Exception):
    pass


class ServicoTelemetriaEspacial:
    def __init__(self, url_estacao="https://estacao-terra.exemplo/api", timeout=5):
        self.url_estacao = url_estacao
        self.timeout = timeout

    def _post(self, caminho, corpo):
        requisicao = urllib.request.Request(
            f"{self.url_estacao}/{caminho}",
            data=json.dumps(corpo).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(requisicao, timeout=self.timeout) as resposta:
                return json.loads(resposta.read().decode("utf-8"))
        except OSError as erro:
            raise FalhaTelemetriaError(str(erro)) from erro

    def enviar_relatorio(self, status):
        return self._post("relatorio", status)

    def disparar_alerta(self, nivel, mensagem):
        return self._post("alerta", {"nivel": nivel, "mensagem": mensagem})
