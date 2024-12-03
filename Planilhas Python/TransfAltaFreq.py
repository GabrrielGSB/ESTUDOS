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
                        dutyCicle      =1,
                        formaOnda      ="senoide",
                        tipoTransf     ="tipo 1" ):
        
        self.tensaoEntrada  = tensaoEntrada #[V]
        self.tensaoSaida    = tensaoSaida   #[V]
        self.potenciaSaida  = potenciaSaida #[W]
        self.frequencia     = frequencia    #[Hz]
        self.correnteSaida  = correnteSaida #[A]
        self.rendimento     = rendimento    #[η]
        self.regulacao      = regulacao     #[α]
        self.densiFluxo     = densiFluxo    #[T]
        self.deltaTemp      = deltaTemp     #[°C]
        self.densiCorrente  = densiCorrente #[A/cm2]
        self.usoJanela      = usoJanela     #[Ku]
        self.fatorForma     = 0             #[Kf]
        self.formaOnda      = formaOnda 
        self.dutyCicle      = dutyCicle

        self.tipoTransformador = tipoTransf
        self.resistividadeCobre = 68.5  #[μΩ/cm] p/ 100°C (constante)

    def calcularProjeto(self):
        #Considerações iniciais
        self.definirFormaOnda()
        self.calcularPotenciaTotal()
        self.calcularProdutoAreas()
        self.definicoesTabeladasTrasformador()

        #Calculos do Primário
        self.calcularNumEspirasPri()
        self.calcularCorrenteEntradaAltaFreq()
        self.calcularSkinEfect()
        self.calcularDiametroMaxFio()
        self.calcularSecaoFioPriAltaFreq()
        self.calcularNumFiosParalelosPri()

        #Calculos do Secundário
        self.calcularNumEspirasSecAltaFreq()
        self.calcularCorrenteSaidaAltaFreq()
        self.calcularSecaoFioSecAltaFreq()
        self.calcularNumFiosParalelosSec()
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

    def definicoesTabeladasTrasformador(self):
        print("\n● Defina algumas constantes tabeladas com base em Ap (Produto de Areas) calculado.")
        self.definirAw()
        self.definirAe()
        self.definirApTabelado()
        self.definirCaminhoMedioEspira()
        self.definirAreaSuperficie()
        self.definirDensidadeCorrente()

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

    def calcularNumEspirasPri(self):
        self.numEspirasPri   = ceil(((self.tensaoEntrada * 1e4) / 
                                     (self.fatorForma * self.densiFluxo * self.frequencia * self.Ae)))
        print(f"\n► O Número de Espiras no Primário (Np) é \033[31m{self.numEspirasPri}\033[0m")

    def calcularCorrenteEntradaAltaFreq(self):
        self.correnteEntrada = (self.potenciaSaida / self.tensaoEntrada) * ((sqrt(2*self.dutyCicle)) / 
                                                                            (2*self.dutyCicle))
        print(f"\n► A Corrente de Entrada (Ipri) é \033[31m{self.correnteEntrada:.3f}\033[0m [A]")

    def calcularSkinEfect(self):
        self.skinEfect = (6.62 /
                     sqrt(self.frequencia))
    
    def calcularDiametroMaxFio(self):
        self.diametroMaxFio = 2 * self.skinEfect
        print(f"\n► O diâmetro máximo que um fio pode ter é \033[31m{self.diametroMaxFio:.4f}\033[0m [cm] ou \033[31m{(self.diametroMaxFio*10):.4f}\033[0m [mm]\n")

    def calcularSecaoFioPriAltaFreq(self):
        self.secaoFioPriCalculada = ((self.correnteEntrada / 
                                      self.densiCorrenteEscolhida))
        print(f"► A Seção do Fio Primário (Awpri) calculada é \033[31m{self.secaoFioPriCalculada:.4f}\033[0m [cm2]\n")
        self.definirAWGpri()
        self.definirBitolaFioPri()

    def calcularNumFiosParalelosPri(self):
        self.numFiosPriParalelos = ((self.secaoFioPriCalculada) /
                                    (self.areaFioPri_cm2))
        print(f"\n► O Número de Fios em Paralelo calculados para o Primário é \033[31m{round(self.numFiosPriParalelos,0)}\033[0m")

    def calcularNumEspirasSecAltaFreq(self):
        self.numEspirasSec = ceil((self.tensaoSaida / self.tensaoEntrada) * (1 / (2*self.dutyCicle) * self.numEspirasPri))
        print(f"\n► O Número de Espiras no Secundário (Ns) é \033[31m{self.numEspirasSec}\033[0m")

    def calcularCorrenteSaidaAltaFreq(self):
        self.correnteSaida = (self.potenciaSaida / self.tensaoSaida) * sqrt(2 * self.dutyCicle)
        print(f"\n► A Corrente de Saída (Io) é \033[31m{self.correnteSaida:.3f}\033[0m [A]")

    def calcularSecaoFioSecAltaFreq(self):
        self.secaoFioSecCalculada = ((self.correnteSaida / 
                                      self.densiCorrenteEscolhida))
        print(f"\n► A Seção do Fio Secundário (Awsec) calculada é \033[31m{self.secaoFioSecCalculada:.4f}\033[0m [cm2]")
        self.definirAWGsec()
        self.definirBitolaFioSec()

    def calcularNumFiosParalelosSec(self):
        self.numFiosSecParalelos = ((self.secaoFioSecCalculada) /
                                    (self.areaFioSec_cm2))
        print(f"\n► O Número de Fios em Paralelo calculados para o Secundário é \033[31m{round(self.numFiosSecParalelos,0)}\033[0m")

    def calcularFatorUtilizacaoJanela(self):
        self.usoJanelaPri = (self.numEspirasPri * self.secaoFioPriCalculada) / (self.Aw)
        print(f"\n► O Uso da Janela do Primário é \033[31m{self.usoJanelaPri:.4f}\033[0m")

        self.usoJanelaSec = (self.numEspirasSec * self.secaoFioSecCalculada) / (self.Aw)
        print(f"\n► O Uso da Janela do Secundário é \033[31m{self.usoJanelaSec:.4f}\033[0m")

        self.usoJanelaTotal = self.usoJanelaPri + self.usoJanelaSec
        print(f"\n► O Uso da Janela Total é \033[31m{self.usoJanelaTotal:.4f}\033[0m")















