[[Explicação com análise de circuitos com transformadores.canvas|link do canva]]

![[Pasted image 20240803141215.png]]

(a) Se o sistema de potência for exatamente como o recém descrito, qual será a tensão sobre a carga? Quais serão as perdas na linha de transmissão? 

(b) Suponha que um transformador elevador de tensão 1:10 seja colocado na extremidade da linha de transmissão que está junto ao gerador. Um outro transformador abaixador 10:1 é colocado na extremidade da linha de transmissão que está junto à carga. Agora, qual será a tensão sobre a carga? Quais serão as perdas na linha de transmissão?

SOLUÇÃO--------------------------------------------------------------------------------------------------

(**a**) Para a Figura (a) a $I_{fonte} = I_{linha} = I_{carga}$, logo essas corrente podem ser calculadas por:

$$
I_{linha} = \frac{V}{Z_{linha} + Z_{carga}} = \frac{480\angle0°}{(0.18 + j0.24) + (4+j3)} = \frac{480\angle0°}{5,29\angle37.8°} = 90.8\angle-37.8° A
$$
Portanto a tensão na **carga** é:

$$
	V_{linha} = I_{linha}\cdot Z_{carga} = 90.8\angle-37.8° \cdot (4+j3) = 454\angle-0.9° \space V
$$
As perdas na linha são:

$$
P_{perdas} = (I_{linha})^2 \cdot R_{linha} = 90.8^2 \cdot 0.18 = 1484\space W
$$

(**b**) Na figura (b) há a presença de dois transformadores, assim a fim de poder trabalhar com o circuito é preciso converter ele à um nível de tensão comum. Portanto, é necessário:

1. Eliminar o transformador T2 referindo a carga ao nível de tensão da linha de transmissão.
2. Eliminar o transformador T1 referindo os elementos da linha de transmissão e a carga equivalente, no nível de tensão de transmissão, ao lado da fonte.

O valor da impedância de carga quando refletida ao nível da tensão do sistema de transmissão é:

$$
Z^{'}_{carga} = a^2\cdot Z_{carga} = \Bigg(\frac{10}{1}\Bigg)^2 \cdot (4+j3) = 400 + 300j 
$$

A impedância total na linha agora é: 

$$
Z_{eq} = Z_{linha} + Z^{'}_{carga}
= 400.18 + j300.24 = 500.3\angle36.88° \ohm
$$
Agora fazendo a mesma coisa, mas agora para $T_{1}$

$$
Z^{'}_{eq} = a^2 \cdot Z_{eq} = \Bigg(\frac{1}{10}\Bigg)^2 \cdot Z_{eq} = 5.003\angle36.88° \ohm
$$
Logo a corrente do gerador já pode ser calculada:

$$
I_{fonte} =\frac{480\angle0°}{5.003\angle36.88°} = 95.94\angle-36.88° A
$$
Com $I_{fonte}$ em mão é possível descobrir o resto das correntes apenas utilizando a relação de transformação dos transformadores ($\frac{1}{10}$).

$$
N_{P1} \cdot I_{fonte} = N_{S1}\cdot I_{linha} 
$$
$$
I_{linha} = \frac{N_{P1}}{N_{S1}}\cdot I_{fonte} = 9.594\angle-36.88° A
$$
$$
	I_{carga} = a_{2}\cdot I_{linha} = 95.94\angle-36.88° A
$$
Agora é possível descobrir a tensão na carga  e a potência perdida.

$$
V_{carga} = I_{carga} \cdot Z_{carga} = 479.7\angle-0.01° \space V
$$
$$
P_{perdas} = (I_{linha})^2\cdot R_{linha} = 16.7\space W
$$
Observe que a elevação da tensão de transmissão do sistema de potência reduziu as perdas de transmissão em aproximadamente 90 vezes! Além disso, a tensão na carga caiu muito menos no sistema com transformadores do que no sistema sem transformadores. Esse exemplo simples ilustra dramaticamente as vantagens do uso de linhas de transmissão que operam com tensão mais elevada, assim como a extrema importância dos transformadores nos sistemas modernos de potência.