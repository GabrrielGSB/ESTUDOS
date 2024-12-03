from Transf import Transformador

# I = Indutor(tensaoEntrada = 400,
#             tensaoSaida   = 54,
#             correnteSaida = 9.26,
#             potenciaSaida = 500,
#             frequencia    = 100e3,
#             rendimento    = 0.98,
#             regulacao     = 0.5,
#             densiFluxo    = 0.05,
#             deltaTemp     = 30,
#             densiCorrente = 250,
#             usoJanela     = 0.4,
#             dutyCicle     = 0.4,
#             formaOnda     = 'quadrada',
#             tipoTransf    = 'tipo 1')

transformador = Transformador(tensaoEntrada  =220,
                              tensaoSaida    =220,
                              correnteSaida  =9.1,
                              potenciaSaida  =2000,
                              frequencia     =60,
                              rendimento     =0.95,
                              regulacao      =5,
                              densiFluxo     =1,
                              deltaTemp      =30,
                              densiCorrente  =450,
                              usoJanela      =0.4,
                              formaOnda      ="senoide",
                              tipoTransf     ="tipo 3")

transformador.calcularProjeto()


