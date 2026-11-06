# Thiago Alves Soares - 2502664
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.conftest import PAINEL_URL


def preencher_e_enviar(driver, astronauta, quantidade):
    driver.find_element(By.ID, "astronauta").send_keys(astronauta)
    driver.find_element(By.ID, "quantidade").send_keys(str(quantidade))
    driver.find_element(By.ID, "enviar").click()


def test_solicitacao_aprovada_atualiza_nivel(driver):
    driver.get(PAINEL_URL)
    espera = WebDriverWait(driver, 10)

    preencher_e_enviar(driver, "Ana", 200)

    espera.until(EC.text_to_be_present_in_element((By.ID, "nivel-oxigenio"), "800"))
    espera.until(EC.text_to_be_present_in_element((By.ID, "mensagem"), "Solicitação aprovada"))


def test_solicitacao_acima_do_estoque_e_recusada(driver):
    driver.get(PAINEL_URL)
    espera = WebDriverWait(driver, 10)

    preencher_e_enviar(driver, "Ana", 5000)

    espera.until(EC.text_to_be_present_in_element((By.ID, "mensagem"), "Oxigênio insuficiente"))
    assert driver.find_element(By.ID, "nivel-oxigenio").text == "1000"


def test_cabecalho_de_identificacao(driver):
    driver.get(PAINEL_URL)
    titulo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )
    assert titulo.text == "Thiago Alves Soares 2502664"
