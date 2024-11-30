from Indutor import Indutor

I = Indutor(tensaoEntrada=220,
            tensaoSaida=220,
            potenciaSaida=2000,
            frequencia=60,
            correnteSaida=9.1,
            rendimento=0.95,
            regulacao=5,
            densiFluxo=1,
            deltaTemp=30,
            densiCorrente=450,
            usoJanela=0.4)

I.calculoProjetoTransformador()
I.mostrarResultados()