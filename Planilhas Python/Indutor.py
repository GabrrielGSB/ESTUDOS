from imports import *
from funcoesAuxiliares import *

class Indutor():
    def __init__(self,  tensaoEficaz   =1,
                        correnteEficaz =1,
                        frequencia     =1,
                        rendimento     =1,
                        permeMagnetica =1,
                        densiFluxo     =1,
                        deltaTemp      =1,
                        densiCorrente  =1,
                        usoJanela      =1,
                        formaOnda      ="senoide"):
        
        self.tensaoEficaz    = tensaoEficaz
        self.correnteEficaz  = correnteEficaz
        self.frequencia      = frequencia
        self.rendimento      = rendimento
        self.permeMagnetica  = permeMagnetica
        self.densiFluxo      = densiFluxo
        self.deltaTemp       = deltaTemp
        self.densiCorrente   = densiCorrente
        self.usoJanela       = usoJanela
        self.formaOnda       = formaOnda
        self.pi              = np.pi

    def calcularProjeto(self):
        self.definirFormaOnda()
        self.calcularPotenciaAparente()
        self.calcularProdutoAreas()
        self.definicoesTabeladasTrasformador()
        





    def definirFormaOnda(self):
        if   self.formaOnda == "senoide":
            self.fatorForma = 4.44
        elif self.formaOnda == "quadrada":
            self.fatorForma = 4

        print(f"\n► A forma de onda escolhida é uma \033[31m{self.formaOnda}\033[0m, com fator de forma de \033[31m{self.fatorForma}\033[0m")    

    def definirAw(self):
        self.Aw = float(input(" ▻ Área da Janela (Aw) tabelada [cm2]: "))

    def definirAc(self):
        self.Ac = float(input(" ▻ Área da seção transversal do nucleo (Ac) tabelada [cm2]: "))

    def definirApTabelado(self):
        self.ApTabelado = self.Aw * self.Ac
        print(f"\n► O produto das áreas tabelado é \033[31m{self.ApTabelado:.3f}\033[0m [cm4]\n")

    def definirCaminhoMagnetico(self):
        self.compriCaminhoMagne = float(input(" ▻ O Comprimento do Caminho Magnético (MPL) tabelado [cm]: "))
        
    def definirCaminhoMedioEspira(self):
        self.MLT = float(input(" ▻ O comprimento da espira (MLT) tabelado [cm]: "))
        
    def definirAreaSuperficie(self):
        self.areaSuperficie = float(input(" ▻ A Área da Superfície (At) tabelada [cm2]: "))

    def definirDensidadeCorrente(self):
        self.densiCorrenteEscolhida = float(input(" ▻ A Densidade de Corrente (J) tabelada [A/cm2]: ")) 

    def definirComprimentoBobinagem(self):
        self.compriBobinagem = float(input(" ▻ O Comprimento da Bobinagem (G) tabelado [cm]: "))

    def definirAWG(self):
        self.AWG = input(" ▻ O AWG escolhido para o Primário é: ")

    def definirBitolaFio(self):
        self.areaFio_mm2 = float(input(" ▻ A Área do Fio Primário tabelada é [mm2]: "))
        self.areaFio_cm2 = self.areaFio_mm2 / 100
        print(f"\n► A Área do Fio Primário tabelada é \033[31m{self.areaFio_cm2:.4f}\033[0m [cm2]")

    def definirResistividade(self):
        self.resistividadeTabelada = float(input(" ▻ A Resistividade Tabelada é [μΩ/cm]: "))

    def definirConstantes_K_M_N(self):
        self.k = float(input(" ▻ A constante K é: "))
        self.m = float(input(" ▻ A constante M é: "))
        self.n = float(input(" ▻ A constante N é: "))

    def definirPesoNucleo(self):
        self.pesoNucleo = float(input(" ▻ O Peso do Núcleo (Wtfe) tabelado [kg]: "))

    def definirLinguaLaminacao(self):
        self.linguaLaminacao = float(input(" ▻ A língua de Lâminação (E) tabelada é: "))
    
    def definirCoeficientePerdaEntreferro(self):
        self.Ki = float(input(" ▻ O Coeficeinte de Perda do Entreferro (Ki) é: "))

    def definicoesTabeladasTrasformador(self):
        print("\n● Defina algumas constantes tabeladas com base em Ap (Produto de Areas) calculado.")
        self.definirAw()
        self.definirAc()
        self.definirApTabelado()
        self.definirCaminhoMagnetico()
        self.definirAreaSuperficie()
        self.definirDensidadeCorrente()
        self.definirComprimentoBobinagem()
        self.definirResistividade()
        self.definirPesoNucleo()
        self.definirLinguaLaminacao()
        self.definirCoeficientePerdaEntreferro()

    def calcularPotenciaAparente(self):
        self.potenciaAparente = self.tensaoEficaz * self.correnteEficaz
        print(f"\n► A Potência Aparente (VA) calculada é \033[31m{self.potenciaAparente:.4f}\033[0m")

    def calcularProdutoAreas(self):
        self.Ap = ((self.potenciaAparente * 1e4) /
                   (self.densiFluxo * self.frequencia * self.densiCorrente * self.usoJanela * self.fatorForma))
        print(f"\n► O Produto das Áreas (Ap) para o Indutor é \033[31m{self.Ap:.3f}\033[0m")

    def calcularNumEspirasIndutor(self):
        self.numEspiras = ((self.tensaoEficaz * 1e4)/
                                  (self.fatorForma * self.densiCorrente * self.frequencia * self.Ac))
        print(f"\n► O Número de Espiras (Nl) do indutor é \033[31m{self.numEspiras:.4f}\033[0m")

    def calcularReatanciaIndutiva(self):
        self.reatanciaIndutiva = self.tensaoEficaz / self.correnteEficaz   
        print(f"\n► A Reatância Indutiva (Xl) calculada é \033[31m{self.reatanciaIndutiva:.4f}\033[0m [Ω]")

    def calcularIndutancia(self):
        self.indutancia = (self.reatanciaIndutiva / 
                          (2 * self.pi * self.frequencia))
        print(f"\n► A Indutância (L) calculada é \033[31m{self.indutancia:.4f}\033[0m [H]")

    def calcularEntreferro(self):
        self.entreFerro = ((self.compriCaminhoMagne / self.permeMagnetica) * (0.4 * self.pi * self.numEspiras * self.Ac * 1e-8) / 
                                                                             (self.indutancia))
        print(f"\n► O Entreferro (lg) calculado é \033[31m{self.entreFerro:.4f}\033[0m [cm]")

    def calcularEspraiamento(self):
        self.espraiamento = (1 + (self.entreFerro / sqrt(self.Ac)) * log((2 * self.compriBobinagem) / 
                                                                          self.entreFerro))
        print(f"\n► O Espraiamento (F) calculado é \033[31m{self.espraiamento:.4f}\033[0m")
    
    def calcularNovoNumEspiras(self):
        self.numEspirasCorrigido = sqrt((self.entreFerro * self.indutancia) / 
                                        (0.4 * self.pi * self.Ac * self.espraiamento * 1e-8))
        print(f"\n► O Novo Numero de Espiras (Nnew) é \033[31m{self.numEspirasCorrigido:.4f}\033[0m")

    def calcularDensidadeFluxo(self):
        self.densiFluxoCalculada = ((self.tensaoEficaz * 1e4) / 
                                    (self.fatorForma * self.numEspirasCorrigido * self.Ac * self.frequencia))
        print(f"\n► A Densidade de Fluxo Magnético (B) calculada é \033[31m{self.densiFluxoCalculada:.4f}\033[0m [T]")

    def calcularSecaoFio(self):
        self.secaoFio = ((self.correnteEficaz / 
                          self.densiCorrente))
        print(f"\n► A Seção do Fio (Aw) calculada é \033[31m{self.secaoFio:.4f}\033[0m [cm2]\n")
        self.definirAWG()
        self.definirBitolaFio()

    def calcularResistenciaPri(self):
        self.resistenciaIndutor   = self.MLT * self.numEspirasCorrigido * self.resistividadeTabelada * 1e-6
        print(f"\n► A Resistência do Indutor (Rl) calculada é \033[31m{self.resistenciaIndutor:.3f}\033[0m [Ω]")
        
    def calcularPerdasCobre(self):
        self.perdaCobre = self.correnteEficaz**2 * self.resistenciaIndutor
        print(f"\n► As Perdas no Cobre (Pl) do são \033[31m{self.perdaCobre:.3f}\033[0m [W]")

    def calcularPerdaWattKilo(self):
        self.perdasWattKilo = self.k * self.frequencia**(self.m) * self.densiFluxo**(self.n)
        print(f"\n► As Perdas por Watt / Kg são \033[31m{self.perdasWattKilo:.3f}\033[0m [W/Kg]")

    def calcularPerdasNucleo(self):
        self.perdaNucleo = self.perdasWattKilo * self.pesoNucleo
        print(f"\n► As Perdas no Núcleo (Pfe) são \033[31m{self.perdaNucleo:.3f}\033[0m [W]")
    
    def calcularPerdasEntreferro(self):
        self.perdaEntreferro = self.Ki * self.linguaLaminacao * self.entreFerro * self.frequencia * self.densiFluxo**2
        print(f"\n► As Perdas no Entreferro (Pg) são \033[31m{self.perdaEntreferro:.3f}\033[0m [W]")

    def calcularPerdasTotais(self):
        self.perdaTotal = self.perdaCobre + self.perdaNucleo + self.perdaEntreferro
        print(f"\n► As Perdas Totais (Pt) são \033[31m{self.perdaTotal:.3f}\033[0m [W]")

    def calcularWattArea(self):
        self.wattsPorArea = self.perdaTotal / self.areaSuperficie
        print(f"\n► A Relação de perda por unidade de área (ψ) é \033[31m{self.wattsPorArea:.3f}\033[0m [W/cm2]")

    def calcularElevacaoTemp(self):
        self.elevTemp = 450 * pow(self.wattsPorArea, 0.826)
        print(f"\n► A elevação de temperatura calculada (Tr) é \033[31m{self.elevTemp:.3f}\033[0m [°C]")

    def calcularFatorUtilizacaoJanela(self):
        self.usoJanelaCalculado = ((self.numEspirasCorrigido * self.secaoFio) / 
                                    self.Aw)
        print(f"\n► O Uso da Janela Total é \033[31m{self.usoJanelaCalculado:.4f}\033[0m")
    


