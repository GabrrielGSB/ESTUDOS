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
        self.definirFormaOnda
        self.calcularPotenciaTotal
        self.calcularProdutoAreas
        self.definicoesTabeladasTrasformador
        self.calcularDensiCorrente

        #Calculos do Primário
        self.calcularNumEspirasPri
        self.calcularCorrenteEntrada
        self.calcularSecaoFioPri
        self.calcularNumFiosParalelosPri
        self.calcularResistenciaPri
        self.calcularPerdasCobrePri

        #Calculos do Secundário
        self.calcularNumEspirasSec
        self.calcularSecaoFioSec
        self.calcularNumFiosParalelosSec
        self.calcularResistenciaSec
        self.calcularPerdasCobreSec

        #Calculos Gerais
        self.calcularPerdasTotaisCobre
        self.calcularRegulacaoTensao
        self.definirPerdaWattKilo
        self.definirDimensoesNucleo
        self.calcularPerdasAcoSilicio
        self.calcularPerdasTotais
        self.calcularWattArea
        self.calcularElevacaoTemp
        self.calcularFatorUtilizacaoJanela

    def definirFormaOnda(self):
        if   self.formaOnda == 'senoide':
            self.fatorForma = 4.44
        elif self.formaOnda == 'quadrada':
            self.fatorForma = 4

        print(f"\n► A forma de onda escolhida é uma \033[31m{self.formaOnda}\033[0m, ")
        print(f"com fator de forma de \033[31m{self.fatorForma}\033[0m\n")

    def definicoesTabeladasTrasformador(self):
        print(f"► O produto das Áreas calculado é \033[31m{self.Ap:.2f}\033[0m [cm4]\n")
        print("● Defina algumas constantes tabeladas com base em Ap (Produto de Areas) calculado.")
        self.definirAw()
        self.definirAe()
        self.definirApTabelado()
        self.definirCaminhoMedioEspira()
        self.definirAreaSuperficie()
        self.definirDensidadeCorrente()

    def definirPerdaWattKilo(self):
        self.wattKiloAperam = float(input("A perda em W/Kg Tabelada para o núcleo escolhido é: "))

    def definirDimensoesNucleo(self, pesoTabelado=True):
        if pesoTabelado != True:
            self.areaLamina_cm2    = int(input("Definir Área da Lámina do transformador [cm^2]: "))
            self.empilhamento_cm   = int(input("Definir Empilhamento de Láminas do transformador [cm]: "))
            self.areaLamina_inch2  = self.areaLamina_cm2 * 0.155
            self.empilhamento_inch = self.empilhamento_cm / 2.54
            self.pesoEstimado      = self.areaLamina_inch2 * self.empilhamento_inch * 0.125
        else:
            self.pesoEstimado = float(input("O peso estimado tabelado do núcleo é: "))

        self.definirAreaSuperficie()

    def calcularPotenciaTotal(self):
        if self.tipoTransformador == "tipo 3":
            self.potenciaTotal = self.potenciaSaida * (2 * sqrt(2))
        elif self.tipoTransformador == "tipo 1":
            self.potenciaTotal = self.potenciaSaida * ((1/self.rendimento) + 1)

        print(f"► O tipo de transformador escolhido é o \033[31m{self.tipoTransformador}\033[0m, ")
        print(f"com potência total de \033[31m{self.potenciaTotal:.3f}\033[0m [W]\n")

    def calcularProdutoAreas(self):
        self.Ap = ((self.potenciaTotal * 1e4) / 
                   (self.densiFluxo * self.frequencia * self.densiCorrente * self.usoJanela * self.fatorForma))    
        
    def calcularDensiCorrente(self):
        self.densiCorrenteCalculada = ((self.potenciaTotal * 1e4) / 
                                       (self.fatorForma * self.usoJanela * self.densiFluxo * self.frequencia * self.ApTabelado))

    def calcularNumEspirasPri(self):
        self.numEspirasPri   = ceil(((self.tensaoEntrada * 1e4) / 
                                     (self.fatorForma * self.densiFluxo * self.frequencia * self.Ae)))
        print(f"\n► O Número de Espiras no Primário (Np) é \033[31m{self.numEspirasPri}\033[0m")

    def calcularNumEspirasSec(self):
        self.numEspirasSec = ceil(((self.numEspirasPri * self.tensaoSaida) / (self.tensaoEntrada)) * (1 + self.regulacao / 100))

    def calcularCorrenteEntrada(self):
        self.correnteEntrada = ((self.potenciaSaida) / 
                                (self.tensaoEntrada * self.rendimento))

    def calcularSecaoFioPri(self):
            self.secaoFioPriCalculada   = ((self.correnteEntrada / 
                                            self.densiCorrenteCalculada))
            print(f"\nA seção do calculada é {self.secaoFioPriCalculada:.4f} [cm2]")
            self.definirAWGpri()
            self.definirBitolaFioPri()

    def calcularSecaoFioSec(self):
        self.secaoFioSecCalculada = ((self.correnteSaida / 
                                      self.densiCorrenteCalculada))
        print(f"\nA seção do calculada é {self.secaoFioSecCalculada:.4f} [cm2]")
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
                                 (self.numFiosPriParalelos))

    def calcularResistenciaSec(self):
            self.resistenciaSec = ((self.MLTfioSec * self.numEspirasSec * self.resistividadeCobre *1e-6) / 
                                (self.numFiosSecParalelos))

    def calcularPerdasCobrePri(self):
        self.perdaCobrePri = self.correnteEntrada**2 * self.resistenciaPri
         
    def calcularPerdasCobreSec(self):
        self.perdaCobreSec = self.correnteSaida**2 * self.resistenciaSec
    
    def calcularPerdasTotaisCobre(self):
        self.perdasTotaisCobre = self.perdaCobrePri + self.perdaCobreSec
    
    def calcularRegulacaoTensao(self):
        self.regulacaoCalculada = (100 * (self.perdasTotaisCobre / 
                                          self.potenciaSaida))
    
    def calcularPerdasAcoSilicio(self):
        self.perdaFerro   = self.wattKiloAperam * self.pesoEstimado
    
    def calcularPerdasTotais(self):
        self.perdaTotal = self.perdasTotaisCobre + self.perdaFerro
    
    def calcularPerdasTotaisCobre(self):
        self.perdasTotaisCobre = self.perdaCobrePri + self.perdaCobreSec
    
    def calcularWattArea(self):
        self.wattsPorArea = self.perdaTotal / self.areaSuperficie
    
    def calcularElevacaoTemp(self):
        self.elevTemp = 450 * pow(self.wattsPorArea, 0.826)

    def calcularFatorUtilizacaoJanela(self):
        self.usoJanelaPri = (self.numEspirasPri * self.secaoFioPriCalculada) / (self.Aw)
        print(f"\n► O Uso da Janela do Primário é \033[31m{self.usoJanelaPri:.4f}\033[0m")

        self.usoJanelaSec = (self.numEspirasSec * self.secaoFioSecCalculada) / (self.Aw)
        print(f"\n► O Uso da Janela do Secundário é \033[31m{self.usoJanelaSec:.4f}\033[0m")

        self.usoJanelaTotal = self.usoJanelaPri + self.usoJanelaSec
        print(f"\n► O Uso da Janela Total é \033[31m{self.usoJanelaTotal:.4f}\033[0m")




