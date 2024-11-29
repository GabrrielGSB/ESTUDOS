from imports import *
def sqrt(x):
    return m.sqrt(x)
def ceil(x):
    return m.ceil(x)

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

        self.AWGpri             = 0
        self.OhmPorCm           = 0
        self.OhmPorCmSec        = 0
        self.alamina_cm2        = 0 
        self.alamina_inch2      = 0
        self.areaSuperficie     = 0
        self.wattKilo_Aperam    = 0
        self.empilhamento_cm    = 0
        self.empilhamento_inch  = 0
        self.comprimentoFioPri  = 0
        self.comprimentoFioSec  = 0
        self.resistividadeCobre = 68.5  #[μΩ/cm] p/ 100°C (constante)
        self.Ae, self.Aw, self.Ap  = 0,0,0 
    
    # def sequenciaCalculo(self):

    def definirAWG_primario(self, AWG):
        self.AWGpri = AWG

    def definirAWG_secundario(self, AWG):
        self.AWGsec = AWG
    
    def definirAreaFioPrimario_cm2(self, mm2):
        self.areaFioPri_mm2 = mm2
        self.areaFioPri_cm2 = self.areaFioPri_mm2 / 100

    def definirAreaFioSecundario_cm2(self, mm2):
        self.areaFioSec_mm2 = mm2
        self.areaFioSec_cm2 = self.areaFioSec_mm2 / 100
        
    def calcularPotenciaTotal(self):
        self.potenciaTotal = self.potenciaSaida * (2 * sqrt(2)) 

    def calcularProdutoArea(self):
        self.produtoArea = ((self.potenciaTotal * 1e4) / 
                            (self.densiFluxo * self.frequencia * self.densiCorrente * self.usoJanela * self.fatorForma))  
        
    def calcularEspirarPri(self):
        self.numEspirasPri   = int(((self.tensaoEntrada * 1e4) / 
                                    (self.fatorForma * self.densiFluxo * self.frequencia * self.Ae)))

    def calculoNumEspirasSec(self):
        self.numEspirasSec = int(((self.numEspirasPri * self.tensaoSaida) / 
                                  (self.tensaoEntrada)) * (1 + self.regulacao / 100))
    
    def verificarDensiCorrente(self):
        self.densiCorrenteTeste = ((self.potenciaTotal * 1e4) / 
                                   (self.fatorForma * self.usoJanela * self.densiFluxo * self.frequencia * self.Ap))
    
    def calcularCorrenteEntrada(self):
        self.correntePrimario = ((self.potenciaSaida) / 
                                 (self.tensaoEntrada * self.rendimento))

    def calcularSecaoFioPri(self):
        self.secaoFioPri   = ceil((self.correntePrimario / 
                                        self.densiCorrente))

    def calcularSecaoFioSec(self):
        self.secaoFioSec = ceil((self.correnteSaida / 
                                        self.densiCorrente))

    def calculoNumFiosParalelosPri(self):
        self.numFiosPriParalelos = ((self.secaoFioPri) /
                                    (self.areaFioPri_cm2 / 100))
    
    def calculoNumFiosParalelosSec(self):
        self.numFiosSecParalelos = ((self.secaoFioSec) /
                                    (self.areaFioSec_cm2 / 100))

    def calculoResistenciaPri(self):
        self.resistenciaPrimario   = ((self.comprimentoFioPri * self.OhmPorCm * self.resistividadeCobre * 1e-6) / 
                                      (self.numFiosPriParalelos))

    def calculoResistenciaSec(self):
        self.resistenciaSecundario = ((self.comprimentoFioSec * self.OhmPorCmSec * self.resistividadeCobre *1e-6) / 
                                      (self.numFiosSecParalelos))

    def calculoPerdasCobrePri(self):
        self.perdaCobrePrimario = self.correntePrimario**2 * self.resistenciaPrimario
         
    def calculoPerdasCobreSec(self):
        self.perdaCobreSecundario = self.correnteSaida**2 * self.resistenciaPrimario
    
    def calculoPerdasTotaisCobre(self):
        self.perdasTotaisCobre = self.perdaCobrePrimario + self.perdaCobreSecundario
    
    def verificarRegulacaoTensao(self):
        self.rendimentoCalculado = (self.perdasTotaisCobre / 
                                    self.potenciaSaida)

    def calculoPerdasAcoSilicio(self):
        self.pesoEstimado = self.alamina_inch2 * self.empilhamento_inch * 0.125
        self.perdaFerro   = self.wattKilo_Aperam * self.pesoEstimado
    
    def calculoPerdasTotais(self):
        self.perdaTotal = self.perdasTotaisCobre + self.perdaFerro
    
    def calculoWattArea(self):
        self.wattsPorArea = self.perdaTotal / self.areaSuperficie
    
    def calculoElevacaoTemp(self):
        self.elevTemp = 450 * pow(self.wattsPorArea, 0.826)
    
    def calculoFatorUtilizacaoJanela(self):
        self.usoJanelaPri = (self.numEspirasPri * self.secaoFioPri) / (self.Aw)
        self.usoJanelaSec = (self.numEspirasSec * self.secaoFioSec) / (self.Aw)
        self.usoJanela = self.usoJanelaPri + self.usoJanelaSec

   


                                


