from imports import *
from funcoesAuxiliares import *

class Transformador:
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
        self.tipoTranf     = tipoTransf

        self.resistividadeCobre = 68.5  #[μΩ/cm] p/ 100°C (constante)

    def calcularProjeto(self):
        #Considerações iniciais
        self.definirFormaOnda()
        self.calcularPotenciaTotal()
        self.calcularProdutoAreas()
        self.definicoesTabeladasTrasformador()
        self.calcularDensiCorrente()

        #Calculos do Primário
        self.calcularNumEspirasPri()
        self.calcularCorrenteEntrada()
        self.calcularSecaoFioPri()
        self.calcularNumFiosParalelosPri()
        self.calcularResistenciaPri()
        self.calcularPerdasCobrePri()

        #Calculos do Secundário
        self.calcularNumEspirasSec()
        self.calcularSecaoFioSec()
        self.calcularNumFiosParalelosSec()
        self.calcularResistenciaSec()
        self.calcularPerdasCobreSec()

        #Calculos Gerais
        self.calcularPerdasTotaisCobre()
        self.calcularRegulacaoTensao()
        self.definirPerdaWattKilo()
        self.definirDimensoesNucleo()
        self.calcularPerdasAcoSilicio()
        self.calcularPerdasTotais()
        self.calcularWattArea()
        self.calcularElevacaoTemp()
        self.calcularFatorUtilizacaoJanela()

    def definirFormaOnda(self):
        if   self.formaOnda == "senoide":
            self.fatorForma = 4.44
        elif self.formaOnda == "quadrada":
            self.fatorForma = 4

        print(f"\n► A forma de onda escolhida é uma \033[31m{self.formaOnda}\033[0m, com fator de forma de \033[31m{self.fatorForma}\033[0m")

    def definirAw(self):
        self.Aw = float(input(" ▻ Área da Janela (Aw) tabelada [cm2]: "))

    def definirAe(self):
        self.Ae = float(input(" ▻ Área da seção transversal (Ae) tabelada [cm2]: "))

    def definirApTabelado(self):
        self.ApTabelado = self.Aw * self.Ae
        print(f"\n► O produto das áreas tabelado é \033[31m{self.ApTabelado:.3f}\033[0m [cm4]\n")

    def definirCaminhoMedioEspira(self):
        self.MLTfioPri = float(input(" ▻ O comprimento da espira (MLT) tabelado [cm]: "))
        self.MLTfioSec = self.MLTfioPri

    def definirAreaSuperficie(self):
        self.areaSuperficie = float(input(" ▻ A Área da Superfície (At) tabelada [cm2]: "))

    def definirDensidadeCorrente(self):
        self.densiCorrenteEscolhida = float(input(" ▻ A Densidade de Corrente (J) tabelada [A/cm2]: ")) 

    def definicoesTabeladasTrasformador(self):
        print("\n● Defina algumas constantes tabeladas com base em Ap (Produto de Areas) calculado.")
        self.definirAw()
        self.definirAe()
        self.definirApTabelado()
        self.definirCaminhoMedioEspira()
        self.definirAreaSuperficie()
        self.definirDensidadeCorrente()

    def definirPerdaWattKilo(self):
        self.wattKiloAperam = float(input(" ▻ A perda em W/Kg Tabelada para o núcleo escolhido é: "))

    def definirDimensoesNucleo(self, pesoTabelado=True):
        if pesoTabelado != True:
            self.areaLamina_cm2    = int(input(" ▻ Definir Área da Lámina do transformador [cm^2]: "))
            self.empilhamento_cm   = int(input(" ▻ Definir Empilhamento de Láminas do transformador [cm]: "))
            self.areaLamina_inch2  = self.areaLamina_cm2 * 0.155
            self.empilhamento_inch = self.empilhamento_cm / 2.54
            self.pesoEstimado      = self.areaLamina_inch2 * self.empilhamento_inch * 0.125
        else:
            self.pesoEstimado = float(input(" ▻ O peso estimado tabelado do núcleo é: "))

        self.definirAreaSuperficie()

    def definirAWGpri(self):
        self.AWGpri = input(" ▻ O AWG escolhido para o Primário é: ")

    def definirAWGsec(self):
        self.AWGsec = input("\n ▻ O AWG escolhido para o Secundário é: ")

    def definirBitolaFioPri(self):
        self.areaFioPri_mm2 = float(input(" ▻ A Área do Fio Primário tabelada é [mm2]: "))
        self.areaFioPri_cm2 = self.areaFioPri_mm2 / 100
        print(f"\n► A Área do Fio Primário tabelada é \033[31m{self.areaFioPri_cm2:.4f}\033[0m [cm2]")

    def definirBitolaFioSec(self):
        self.areaFioSec_mm2 = float(input(" ▻ A Área do Fio Secundário tabelada é [mm2]: "))
        self.areaFioSec_cm2 = self.areaFioSec_mm2 / 100
        print(f"\n► A Área do Fio Secundário tabelada é \033[31m{self.areaFioPri_cm2:.4f}\033[0m [cm2]")

    def calcularPotenciaTotal(self):
        if   self.tipoTranf == "tipo 3":
            self.potenciaTotal = self.potenciaSaida * (2 * sqrt(2))
        elif self.tipoTranf == "tipo 1":
            self.potenciaTotal = self.potenciaSaida * ((1/self.rendimento) + 1)

        print(f"\n► O tipo de transformador escolhido é o \033[31m{self.tipoTranf}\033[0m, com potência total de \033[31m{self.potenciaTotal:.3f}\033[0m [W]")

    def calcularProdutoAreas(self):
        self.Ap = ((self.potenciaTotal * 1e4) / 
                   (self.densiFluxo * self.frequencia * self.densiCorrente * self.usoJanela * self.fatorForma)) 
        print(f"\n► O Produto de Áreas calculado é \033[31m{self.Ap:.3f}\033[0m [cm4]")   
        
    def calcularDensiCorrente(self):
        self.densiCorrenteCalculada = ((self.potenciaTotal * 1e4) / 
                                       (self.fatorForma * self.usoJanela * self.densiFluxo * self.frequencia * self.ApTabelado))
        print(f"\n► A Densidade de Corrente calculada é \033[31m{self.densiCorrenteCalculada:.3f}\033[0m [J]")

    def calcularNumEspirasPri(self):
        self.numEspirasPri   = ceil(((self.tensaoEntrada * 1e4) / 
                                     (self.fatorForma * self.densiFluxo * self.frequencia * self.Ae)))
        print(f"\n► O Número de Espiras no Primário (Np) é \033[31m{self.numEspirasPri}\033[0m")

    def calcularNumEspirasSec(self):
        self.numEspirasSec = ceil(((self.numEspirasPri * self.tensaoSaida) / (self.tensaoEntrada)) * (1 + self.regulacao / 100))
        print(f"\n► O Número de Espiras para o Secundário é \033[31m{self.numEspirasSec}\033[0m")

    def calcularCorrenteEntrada(self):
        self.correnteEntrada = ((self.potenciaSaida) / 
                                (self.tensaoEntrada * self.rendimento))
        print(f"\n► A Corrente de Entrada é \033[31m{self.correnteEntrada:.3f}\033[0m [A] ")

    def calcularSecaoFioPri(self):
        self.secaoFioPriCalculada   = ((self.correnteEntrada / 
                                        self.densiCorrenteCalculada))
        print(f"\n► A seção do calculada do Primário é \033[31m{self.secaoFioPriCalculada:.4f}\033[0m [cm2]\n")
        self.definirAWGpri()
        self.definirBitolaFioPri()

    def calcularSecaoFioSec(self):
        self.secaoFioSecCalculada = ((self.correnteSaida / 
                                      self.densiCorrenteCalculada))
        print(f"\n► A Seção do Fio Secundário calculada é \033[31m{self.secaoFioSecCalculada:.4f}\033[0m [cm2]")
        self.definirAWGsec()
        self.definirBitolaFioSec()

    def calcularNumFiosParalelosPri(self):
        self.numFiosPriParalelos = ((self.secaoFioPriCalculada) /
                                    (self.areaFioPri_cm2))
        print(f"\n► O Número de Fios em Paralelo calculados para o Primário é \033[31m{round(self.numFiosPriParalelos,0)}\033[0m")

    def calcularNumFiosParalelosSec(self):
        self.numFiosSecParalelos = ((self.secaoFioSecCalculada) /
                                    (self.areaFioSec_cm2))
        print(f"\n► O Número de Fios em Paralelo calculados para o Secundário é \033[31m{round(self.numFiosSecParalelos,0)}\033[0m")

    def calcularResistenciaPri(self):
        self.resistenciaPri   = ((self.MLTfioPri * self.numEspirasPri * self.resistividadeCobre * 1e-6) / 
                                 (ceil(self.numFiosPriParalelos)))
        print(f"\n► A Resistência do Primário é \033[31m{self.resistenciaPri:.3f}\033[0m [Ω]")

    def calcularResistenciaSec(self):
        self.resistenciaSec = ((self.MLTfioSec * self.numEspirasSec * self.resistividadeCobre *1e-6) / 
                                (ceil(self.numFiosSecParalelos)))
        print(f"\n► A Resistência do Secundário é \033[31m{self.resistenciaPri:.3f}\033[0m [Ω]")

    def calcularPerdasCobrePri(self):
        self.perdaCobrePri = self.correnteEntrada**2 * self.resistenciaPri
        print(f"\n► As Perdas no Cobre do Primário são \033[31m{self.perdaCobrePri:.3f}\033[0m [W]")
         
    def calcularPerdasCobreSec(self):
        self.perdaCobreSec = self.correnteSaida**2 * self.resistenciaSec
        print(f"\n► As Perdas no Cobre do Secundário são \033[31m{self.perdaCobreSec:.3f}\033[0m [W]")

    def calcularPerdasTotaisCobre(self):
        self.perdasTotaisCobre = self.perdaCobrePri + self.perdaCobreSec
        print(f"\n► As Perdas no Totais no Cobre são \033[31m{self.perdasTotaisCobre:.3f}\033[0m [W]")
    
    def calcularRegulacaoTensao(self):
        self.regulacaoCalculada = (100 * (self.perdasTotaisCobre / 
                                          self.potenciaSaida))
        print(f"\n► A Regulação de Tensão calculada é \033[31m{self.regulacaoCalculada:.3f}\033[0m [%]\n")
    
    def calcularPerdasAcoSilicio(self):
        self.perdaFerro   = self.wattKiloAperam * self.pesoEstimado
        print(f"\n► As Perdas no Ferro são \033[31m{self.perdaFerro:.3f}\033[0m [W]")
    
    def calcularPerdasTotais(self):
        self.perdaTotal = self.perdasTotaisCobre + self.perdaFerro
        print(f"\n► As Perdas Totais são \033[31m{self.perdaTotal:.3f}\033[0m [W]")
    
    def calcularPerdasTotaisCobre(self):
        self.perdasTotaisCobre = self.perdaCobrePri + self.perdaCobreSec
        print(f"\n► As Perdas Totais no Cobre são \033[31m{self.perdasTotaisCobre:.3f}\033[0m [W]")
    
    def calcularWattArea(self):
        self.wattsPorArea = self.perdaTotal / self.areaSuperficie
        print(f"\n► A Perda por Área é \033[31m{self.wattsPorArea:.3f}\033[0m [W/cm2]")
    
    def calcularElevacaoTemp(self):
        self.elevTemp = 450 * pow(self.wattsPorArea, 0.826)
        print(f"\n► A Elevação de Temperatura calculada é \033[31m{self.elevTemp:.3f}\033[0m [°C]")

    def calcularFatorUtilizacaoJanela(self):
        self.usoJanelaPri = (self.numEspirasPri * self.secaoFioPriCalculada) / (self.Aw)
        print(f"\n► O Uso da Janela do Primário é \033[31m{self.usoJanelaPri:.4f}\033[0m")

        self.usoJanelaSec = (self.numEspirasSec * self.secaoFioSecCalculada) / (self.Aw)
        print(f"\n► O Uso da Janela do Secundário é \033[31m{self.usoJanelaSec:.4f}\033[0m")

        self.usoJanelaTotal = self.usoJanelaPri + self.usoJanelaSec
        print(f"\n► O Uso da Janela Total é \033[31m{self.usoJanelaTotal:.4f}\033[0m")




