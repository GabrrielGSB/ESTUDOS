A fundamentação do funcionamento do transformador pode ser obtida a partir da lei de Faraday:

$$
e_{ind} = \frac{d\lambda}{dt}
$$
em que $\lambda$ é o fluxo concatenado na bobina na qual a tensão está sendo induzida. O fluxo concatenado $\lambda$ é a soma do fluxo que passa através de cada espira da bobina adicionado ao de todas as demais espiras da bobina:

$$
\lambda = \sum^{N}_{i=1}{\phi_i}
$$
![[Pasted image 20240804172847.png]]
O fluxo concatenado total através de uma bobina **não é simplesmente $N\cdot \phi$**, em que N é o número de espiras da bobina, **porque o fluxo que passa através de cada espira de uma bobina é ligeiramente diferente do fluxo que atravessa as outras espiras**, dependendo da posição da espira dentro da bobina.

Entretanto, é possível definir um fluxo médio por espira em uma bobina. Se o fluxo concatenado de todas as espiras da bobina for $\lambda$ e se houver N espiras, o fluxo médio por espira será dado por:
$$
\overline{\phi} = \frac{\lambda}{N}
$$
e a lei de Faraday poderá ser escrita como:
$$
e_{ind} = N \cdot \frac{d\overline{\phi}}{dt}
$$