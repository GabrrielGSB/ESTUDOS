from Indutor import Indutor

I = Indutor(tensaoEntrada = 400,
            tensaoSaida   = 54,
            correnteSaida = 9.26,
            potenciaSaida = 500,
            frequencia    = 100e3,
            rendimento    = 0.98,
            regulacao     = 0.5,
            densiFluxo    = 0.05,
            deltaTemp     = 30,
            densiCorrente = 250,
            usoJanela     = 0.4,
            dutyCicle     = 0.4,
            formaOnda     = 'quadrada',
            tipoTransf    = 'tipo 1')

I.calcularProjetoTransformadorAltaFreq()
