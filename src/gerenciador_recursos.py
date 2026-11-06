# Thiago Alves Soares - 2502664

TAXAS_EMERGENCIA = {1: 1.0, 2: 1.25, 3: 1.5, 4: 2.0}
LIMITE_CRITICO_OXIGENIO = 100.0


class OxigenioInsuficienteError(Exception):
    pass


class AguaInsuficienteError(Exception):
    pass


class NivelEmergenciaInvalidoError(Exception):
    pass


class GerenciadorRecursosMarte:
    def __init__(self, oxigenio, agua, telemetria):
        if oxigenio < 0 or agua < 0:
            raise ValueError("estoque inicial não pode ser negativo")
        self.oxigenio = float(oxigenio)
        self.agua = float(agua)
        self.telemetria = telemetria

    def calcular_taxa_emergencia(self, nivel):
        if nivel not in TAXAS_EMERGENCIA:
            raise NivelEmergenciaInvalidoError(f"nível inválido: {nivel}")
        return TAXAS_EMERGENCIA[nivel]

    def calcular_consumo_diario(self, astronautas, consumo_por_astronauta, nivel=1):
        if astronautas <= 0 or consumo_por_astronauta < 0:
            raise ValueError("astronautas deve ser positivo e consumo não negativo")
        taxa = self.calcular_taxa_emergencia(nivel)
        return astronautas * consumo_por_astronauta * taxa

    def validar_estoque(self, oxigenio_necessario, agua_necessaria=0.0):
        if oxigenio_necessario > self.oxigenio:
            raise OxigenioInsuficienteError(
                f"necessário {oxigenio_necessario}, disponível {self.oxigenio}"
            )
        if agua_necessaria > self.agua:
            raise AguaInsuficienteError(
                f"necessário {agua_necessaria}, disponível {self.agua}"
            )
        return True

    def aplicar_racionamento(self, consumo, cota):
        if not 0 < cota <= 1:
            raise ValueError("cota deve estar entre 0 (exclusivo) e 1")
        return consumo * cota

    def solicitar_oxigenio_extra(self, astronauta, quantidade):
        if quantidade <= 0:
            raise ValueError("quantidade deve ser positiva")
        self.validar_estoque(quantidade)
        self.oxigenio -= quantidade
        if self.oxigenio < LIMITE_CRITICO_OXIGENIO:
            self.telemetria.disparar_alerta(
                "CRITICO", f"Oxigênio em {self.oxigenio:.1f} após pedido de {astronauta}"
            )
        return self.oxigenio

    def enviar_status(self):
        return self.telemetria.enviar_relatorio(
            {"oxigenio": self.oxigenio, "agua": self.agua}
        )
