from imports import *
from funcoesAuxiliares import *

class TransformadorAltaFrequencia:
    def __init__(self,  tensaoEntrada  =1,
                        tensaoSaida    =1,
                        correnteSaida  =1,
                        potenciaSaida  =1,
                        frequencia     =1,
                        rendimento     =1,
                        regulacao      =1,
                        densiFluxo     =1,
                        deltaTemp      =1,
                        densiCorrente  =1,
                        usoJanela      =1,
                        formaOnda      ="senoide",
                        tipoTransf     ="tipo 1" ):
    # def calcularProjeto(self):
