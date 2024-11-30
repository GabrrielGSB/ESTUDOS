from imports import *

def sqrt(x):
    return m.sqrt(x)
def ceil(x):
    return m.ceil(x)

class Indutor:
    def __init__(self,  tensaoEntrada =1, 
                        tensaoSaida   =1,
                        potenciaSaida =1,
                        frequencia    =1,
                        correnteSaida =1,
                        rendimento    =1,
                        regulacao     =1,
                        densiFluxo    =1,
                        deltaTemp     =1,
                        densiCorrente =1,
                        usoJanela     =1,
                        formaOnda     ="senoide"):
        
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

        self.resistividadeCobre = 68.5  #[μΩ/cm] p/ 100°C (constante)

    def calculoProjetoTransformador(self):
        self.definirFormaOnda()
        self.calcularPotenciaTotal()
        self.calcularAp()
        self.introducao()
        self.definirAw()
        self.definirAe()
        self.definirApChapa()
        self.calcularNumEspirasPri()
        self.verificarDensiCorrente()
        self.calcularCorrenteEntrada()
        self.calcularSecaoFioPri()
        self.definirAWGpri()
        self.definirAreaFioPri_cm2()
        self.calculoNumFiosParalelosPri()
        self.definirComprimentoEspiraPri()
        self.calculoResistenciaPri()
        self.calculoPerdasCobrePri()
        self.calculoNumEspirasSec()
        self.calcularSecaoFioSec()
        self.definirAWGsec()
        self.definirAreaFioSec_cm2()
        self.calculoNumFiosParalelosSec()
        self.definirComprimentoEspiraSec()
        self.calculoResistenciaSec()
        self.calculoPerdasCobreSec()
        self.calculoPerdasTotaisCobre()
        self.verificarRegulacaoTensao()
        self.definirPerdaWattKilo()
        self.definirDimensoesNucleo()
        self.definirAreaSuperficie()
        self.calculoPerdasAcoSilicio()
        self.calculoPerdasTotais()
        self.calculoWattArea()
        self.calculoElevacaoTemp()
        self.calculoFatorUtilizacaoJanela()

   


    def definirFormaOnda(self):
        if self.formaOnda == "senoide":
            self.fatorForma = 4.44

    def introducao(self):
        print("Defina algumas constantes tabeladas com base em Ap calculado. Sendo...")
        print(f"Ap = {self.Ap:.2f} [cm4]")

    def definirAw(self):
        self.Aw = int(input("Área da Janela (Aw) escolhida [cm2]: "))

    def definirAe(self):
        self.Ae = int(input("Área da seção transversal (Ae) escolhida [cm2]: "))

    def definirApChapa(self):
        self.ApChapa = self.Aw * self.Ae

    def definirAWGpri(self):
        self.AWGpri = input("O AWG escolhido para o primário é: ")

    def definirAWGsec(self):
        self.AWGsec = input("O AWG escolhido para o secundário é: ")
    
    def definirComprimentoEspiraPri(self):
        self.comprimentoFioPri = int(input("O comprimento da espira (MLT) primária escolhida é [cm]: "))
    
    def definirComprimentoEspiraSec(self):
        self.comprimentoFioSec = int(input("O comprimento da espira (MLT) secundária escolhida é [cm]: "))

    def definirPerdaWattKilo(self):
        self.wattKiloAperam = float(input("A perda em W/Kg Tabelada para o núcleo escolhido é: "))
    
    def definirDimensoesNucleo(self):
        self.areaLamina_cm2    = int(input("Definir Área da Lámina do transformador [cm^2]: "))
        self.empilhamento_cm   = int(input("Definir Empilhamento de Láminas do transformador [cm]: "))
        self.areaLamina_inch2  = self.areaLamina_cm2 * 0.155
        self.empilhamento_inch = self.empilhamento_cm / 2.54

    def definirAreaFioPri_cm2(self):
        self.areaFioPri_mm2 = float(input("A área do fio primário é [mm2]: "))
        self.areaFioPri_cm2 = self.areaFioPri_mm2 / 100

    def definirAreaFioSec_cm2(self):
        self.areaFioSec_mm2 = float(input("A área do fio secundário é [mm2]: "))
        self.areaFioSec_cm2 = self.areaFioSec_mm2 / 100
        
    def calcularPotenciaTotal(self):
        self.potenciaTotal = self.potenciaSaida * (2 * sqrt(2)) 

    def definirAreaSuperficie(self):
        self.areaSuperficie = float(input("A área da superfície escolhida é: "))

    def calcularAp(self):
        self.Ap = ((self.potenciaTotal * 1e4) / 
                   (self.densiFluxo * self.frequencia * self.densiCorrente * self.usoJanela * self.fatorForma))  
        
    def calcularNumEspirasPri(self):
        self.numEspirasPri   = ceil(((self.tensaoEntrada * 1e4) / 
                                     (self.fatorForma * self.densiFluxo * self.frequencia * self.Ae)))

    def calculoNumEspirasSec(self):
        self.numEspirasSec = ceil(((self.numEspirasPri * self.tensaoSaida) / 
                                   (self.tensaoEntrada)) * (1 + self.regulacao / 100))
    
    def verificarDensiCorrente(self):
        self.densiCorrenteTeste = ((self.potenciaTotal * 1e4) / 
                                   (self.fatorForma * self.usoJanela * self.densiFluxo * self.frequencia * self.ApChapa))
    
    def calcularCorrenteEntrada(self):
        self.correntePri = ((self.potenciaSaida) / 
                            (self.tensaoEntrada * self.rendimento))

    def calcularSecaoFioPri(self):
        self.secaoFioPri   = ((self.correntePri / 
                               self.densiCorrente))

    def calcularSecaoFioSec(self):
        self.secaoFioSec = ((self.correnteSaida / 
                             self.densiCorrente))

    def calculoNumFiosParalelosPri(self):
        self.numFiosPriParalelos = ceil((self.secaoFioPri) /
                                        (self.areaFioPri_cm2))
    
    def calculoNumFiosParalelosSec(self):
        self.numFiosSecParalelos = ceil((self.secaoFioSec) /
                                        (self.areaFioSec_cm2))

    def calculoResistenciaPri(self):
        self.resistenciaPri   = ((self.comprimentoFioPri * self.numEspirasPri * self.resistividadeCobre * 1e-6) / 
                                 (self.numFiosPriParalelos))

    def calculoResistenciaSec(self):
        self.resistenciaSec = ((self.comprimentoFioSec * self.numEspirasSec * self.resistividadeCobre *1e-6) / 
                               (self.numFiosSecParalelos))

    def calculoPerdasCobrePri(self):
        self.perdaCobrePri = self.correntePri**2 * self.resistenciaPri
         
    def calculoPerdasCobreSec(self):
        self.perdaCobreSec = self.correnteSaida**2 * self.resistenciaSec
    
    def calculoPerdasTotaisCobre(self):
        self.perdasTotaisCobre = self.perdaCobrePri + self.perdaCobreSec
    
    def verificarRegulacaoTensao(self):
        self.regulacaoCalculada = (100 * (self.perdasTotaisCobre / 
                                          self.potenciaSaida))

    def calculoPerdasAcoSilicio(self):
        self.pesoEstimado = self.areaLamina_inch2 * self.empilhamento_inch * 0.125
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
        self.usoJanelaCalculado = self.usoJanelaPri + self.usoJanelaSec

    def mostrarResultados(self):
        print("\nRESULTADOS")
        print(f"A forma de onda escolhida foi {self.formaOnda}, logo o fator de forma é {self.fatorForma}")
        print(f"A potência total calculada é {self.potenciaTotal:.4f} [W]\n")

        print(f"O produto das áreas calculado é {self.Ap:.4f} [cm4]")
        print(f"A área da janela usada é {self.Aw} [cm2]")
        print(f"A área da seção transversal é {self.Ae} [cm2]")
        print(f"Portanto o produto das áreas da chapa escolhida é {self.ApChapa} [cm4],")
        print(f"e densidade de corrente calculada é {self.densiCorrenteTeste:.4f} [A/cm2]\n")

        print(f"O número de espiras do primário é {self.numEspirasPri}")
        print(f"A corrente no primário é {self.correntePri:.4f} [A]")
        print(f"Assim é preciso de uma seção de fio na bobina do primário de {self.secaoFioPri:.4f} [cm2]")
        print(f"Logo o AWG escolhido para o primário é {self.AWGpri}")
        print(f"O que gera uma seção de fio de {self.areaFioPri_cm2} [cm2]")
        print(f"Com isso o número de fios em paralelo no primário é {self.numFiosPriParalelos}")
        print(f"Assim é preciso de um comprimento de fio de {self.comprimentoFioPri} [cm]")
        print(f"Por fim, essa configuração gera uma resistência na bobina do primário de {self.resistenciaPri:.4f} [Ω],")
        print(f"que gera uma perda ohmica de {self.perdaCobrePri:.4f} [W]\n")

        print(f"O número de espiras do secundário é {self.numEspirasSec}")
        print(f"A corrente no secundário é {self.correnteSaida} [A]")
        print(f"O que gera uma seção de fio para o secundário de {self.secaoFioSec:.4f} [cm2]")
        print(f"O AWG escolhido para o secundário é {self.AWGsec},")
        print(f"O que gera uma seção de fio de {self.areaFioSec_cm2} [cm2]")
        print(f"Com isso o número de fios em paralelo no secundário é {self.numFiosSecParalelos}")
        print(f"Assim é preciso de um comprimento de fio de {self.comprimentoFioSec} [cm]")
        print(f"Por fim, essa configuração gera uma resistência na bobina do secundário de {self.resistenciaSec:.4f} [Ω],")
        print(f"que gera uma perda ohmica de {self.perdaCobreSec:.4f} [W]\n")

        print(f"As perdas ohmicas totais são {self.perdasTotaisCobre:.4f} [W]")
        print(f"Isso faz com que a regulação do transformador fique em {self.regulacaoCalculada:.4f} [%]")
        print(f"Agora a perda em W/Kg defina pela tabela é {self.wattKiloAperam}")
        print(f"O peso estimado do transformador é {self.pesoEstimado:.4f} [Kg]\n")

        print(f"Isso gera uma perda no ferro de {self.perdaFerro:.4f} [W]")
        print(f"Portanto, as perdas totais no transformador são {self.perdaTotal:.4f} [W],")
        print(f"o que gera uma perda por unidade de área de {self.wattsPorArea:.4f} [W/cm2]")
        print(f"Desse modo, a elevação de temperatura do gerador é {self.elevTemp:.4f} [°C]\n")

        print(f"Por fim, o fator de utilização do primário é {self.usoJanelaPri:.4f},")
        print(f"e o uso da janela do secundário é {self.usoJanelaSec:.4f}")
        print(f"Isso gera um fator de utilização total de {self.usoJanelaCalculado:.4f}")


                                


