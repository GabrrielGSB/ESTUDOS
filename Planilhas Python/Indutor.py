from imports import *

def sqrt(x):
    return m.sqrt(x)
def ceil(x):
    return m.ceil(x)

class Indutor:
    def __init__(self,  tensaoEntrada=1, 
                        tensaoSaida=1,
                        potenciaSaida=1,
                        frequencia=1,
                        correnteSaida=1,
                        rendimento=1,
                        regulacao=1,
                        densiFluxo=1,
                        deltaTemp=1,
                        densiCorrente=1,
                        usoJanela=1,
                        formaOnda='senoide'):
        
        self.tensaoEntrada = tensaoEntrada #[V]
        self.tensaoSaida   = tensaoSaida   #[V]
        self.potenciaSaida = potenciaSaida #[W]
        self.frequencia    = frequencia    #[Hz]
        self.correnteSaida = correnteSaida #[A]
        self.rendimento    = rendimento    #[η]
        self.regulacao     = regulacao     #[α]
        self.densiFluxo    = densiFluxo    #[T]
        self.deltaTemp     = deltaTemp     #[°C]
        self.densiCorrente = densiCorrente #[A/cm2]
        self.usoJanela     = usoJanela     #[Ku]
        self.fatorForma    = 0             #[Kf]
        self.formaOnda     = formaOnda 

        self.OhmPorCm           = 0
        self.OhmPorCmSec        = 0
        self.areaSuperficie     = 0
        self.wattKiloAperam     = 0
        self.comprimentoFioSec  = 0
        self.resistividadeCobre = 68.5  #[μΩ/cm] p/ 100°C (constante)
        self.Ae, self.Aw, self.Ap  = 0,0,0 
    
    def calculoProjetoTransformador(self):
        self.calcularPotenciaTotal()
        self.calcularProdutoArea()
        self.introducao()
        self.definirAw()
        self.definirAe()
        self.definirApChapa()
        self.calcularNumEspirasPri()
        self.verificarDensiCorrente()
        self.calcularCorrenteEntrada()
        self.calcularSecaoFioPri()
        self.calculoNumFiosParalelosPri()
        self.definirComprimentoEspiraPri()
        self.calculoResistenciaPri()
        self.calculoPerdasCobrePri()
        self.calculoNumEspirasSec()
        self.calcularSecaoFioSec()
        self.definirAreaFioSecundario_cm2()
        self.calculoNumFiosParalelosSec()
        self.calculoResistenciaSec()
        self.calculoPerdasCobreSec()
        self.calculoPerdasTotaisCobre()
        self.verificarRegulacaoTensao()
        self.definirPerdaWattKilo()
        self.definirDimensoesNucleo()
        self.calculoPerdasAcoSilicio()
        self.calculoPerdasTotais()



    def introducao(self):
        print("Defina algumas constantes tabeladas com base em Ap calculado. Sendo...")
        print(f"Ap = {self.produtoArea} [cm^4]")

    def definirAw(self):
        self.Aw = input("Área da Janela(Aw) escolhida: ")

    def definirAe(self):
        self.Ae = input("Área da seção transversal(Ae) escolhida: ")

    def definirApChapa(self):
        self.ApChapa = self.Aw * self.Ae

    def definirAWGprimario(self):
        self.AWGpri = input("O AWG escolhido para o primário é: ")

    def definirAWGsecundario(self):
        self.AWGsec = input("O AWG escolhido para o secundário é: ")
    
    def definirComprimentoEspiraPri(self):
        self.comprimentoFioPri = input("O comprimento da espira(MLT) primária escolhida é: ")
    
    def definirComprimentoEspiraSec(self):
        self.comprimentoFioSec = input("O comprimento da espira(MLT) secundária escolhida é: ")

    def definirPerdaWattKilo(self):
        self.wattKiloAperam = input("A perda em W/Kg Tabelada para o núcleo escolhido é: ")
    
    def definirDimensoesNucleo(self):
        self.areaLamina_cm2    = input("Definir Área da Lámina do transformador [cm^2]:  ")
        self.empilhamento_cm   = input("Definir Empilhamento de Láminas do transformador [cm]: ")
        self.areaLamina_inch2  = self.areaLamina_cm2 * 0.155
        self.empilhamento_inch = self.empilhamento_cm / 2.54

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
        
    def calcularNumEspirasPri(self):
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
        self.perdaFerro   = self.wattKiloAperam * self.pesoEstimado
    
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

   


                                


