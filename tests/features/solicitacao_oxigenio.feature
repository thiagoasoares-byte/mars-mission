# Thiago Alves Soares - 2502664
Feature: Solicitação de oxigênio extra no habitat

  Scenario: Solicitação em condições normais
    Given um habitat com 1000 kg de oxigênio em estoque
    When o astronauta "Ana" solicita 100 kg de oxigênio extra
    Then o estoque de oxigênio passa a ser 900 kg
    And nenhum alerta de crise é enviado à Terra

  Scenario: Solicitação que leva o habitat a condição de crise
    Given um habitat com 1000 kg de oxigênio em estoque
    When o astronauta "Bruno" solicita 950 kg de oxigênio extra
    Then o estoque de oxigênio passa a ser 50 kg
    And um alerta de crise é enviado à Terra

  Scenario: Solicitação maior que o estoque disponível
    Given um habitat com 1000 kg de oxigênio em estoque
    When o astronauta "Carla" solicita 5000 kg de oxigênio extra
    Then a solicitação é recusada por oxigênio insuficiente
    And nenhum alerta de crise é enviado à Terra
