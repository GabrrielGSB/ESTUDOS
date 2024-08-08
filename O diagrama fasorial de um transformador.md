A maneira mais fácil de determinar o efeito das impedâncias e dos ângulos de fase da corrente sobre a regulação de tensão no transformador é examinar um diagrama fasorial, um gráfico das tensões e correntes fasoriais presentes no transformador.

Em todos os diagramas fasoriais seguintes, assume-se que a tensão fasorial VS está no ângulo 0° e que todas as demais tensões e correntes adotam essa tensão fasorial como referência. Aplicando a lei das tensões de Kirchhoff ao circuito equivalente, a tensão primária pode ser encontrada como:

$$
\frac{V_P}{a} = V_S + R_{eq}\cdot I_S + jX_{eq} \cdot I_S
$$
A Figura abaixo mostra um diagrama fasorial de um transformador funcionando com um fator de potência atrasado. Pode-se ver facilmente que VP/a > VS para cargas atrasadas, de modo que a regulação de tensão de um transformador com cargas atrasadas deve ser maior do que zero.
![[Pasted image 20240807102740.png]]
Essas equações aplicam-se a motores e geradores e também a transformadores. Os circuitos equivalentes facilitam os cálculos de eficiência. Há três tipos de perdas presentes nos transformadores:
1. Perdas no cobre ($I^2 \cdot R$). Essas perdas são representadas pela resistência em série no circuito equivalente. 
2. Perdas por histerese. Essas perdas foram explicadas no Capítulo 1. Elas estão incluídas no resistor $R_C$. 
3. Perdas por corrente parasita. Essas perdas foram explicadas no Capítulo 1. Elas estão incluídas no resistor $R_C$. Para calcular a eficiência de um transformador, que está operando com uma dada carga, simplesmente some as perdas de cada resistor e aplique a Equação abaixo. Como a potência de saída é dada por:
$$
P_{saida} = V_S \cdot I_S \cdot cos\theta_S
$$
A eficiência do transformador pode ser expressa por
$$
n = \frac{V_S \cdot I_S \cdot cos \theta}{P_{Cu} + P_{nucleo} + V_S \cdot I_S \cdot cos \theta} \cdot 100\%
$$
