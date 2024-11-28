from imports import *
def sqrt(x):
    return m.sqrt(x)

class Indutor:
    def __init__(self):
        self.tensaoEntrada = 0
        self.tensaoSaida   = 0
        self.potenciaSaida = 0
        self.frequencia    = 0
        self.correnteSaida = 0
        self.rendimento    = 0
        self.regulacao     = 0
        self.densiFluxo    = 0
        self.deltaTemp     = 0
        self.densiCorrente = 0
        self.usoJanela     = 0
        self.fatorForma    = 0

        self.potenciaTotal   = 0
        self.produtoArea     = 0
        self.espirasPrimario = 0
        self.densiCorrenteTeste = 0
        self.Ae, self.Aw, self.Ap = 0,0,0 
    
    def calcularPotenciaTotal(self):
        # Determinação da potência total
        self.potenciaTotal = self.potenciaSaida * (2 * sqrt(2)) 

    def calcularProdutoArea(self):
        self.produtoArea = ((self.potenciaTotal * 1e4) / 
                            (self.densiFluxo * self.frequencia * self.densiCorrente * self.usoJanela * self.fatorForma))  
        
    def calcularEspirarPri(self):
        self.espirasPrimario = int(((self.tensaoEntrada * 1e4) / 
                                    (self.fatorForma * self.densiFluxo * self.frequencia * self.Ae)))
    
    def verificarDensiCorrente(self):
        self.densiCorrenteTeste = ((self.potenciaTotal * 1e4) / 
                                   (self.fatorForma * self.usoJanela * self.densiFluxo * self.frequencia * self.Ap))
    
    def calcularCorrenteEntrada(self):
        self.correntePrimario = ((self.potenciaSaida) / 
                                 (self.tensaoEntrada * self.rendimento))