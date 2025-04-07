# Trabalho 1
## Modularização
Para trabalhar com o OpenGL, preferimos manter uma modularização que fosse capaz de trabalhar em cima de um conjunto de vértices. Dessa forma, fizemos arquivos responsáveis por controle de shaders, matemática e inicializações do OpenGL e os deixamos na pasta ```utils```. 

Depois, para conseguir o controle das estruturas, fizemos uma classe base chamada ```Area```, sendo responsável por conseguir ter um conjunto de vértices, atuar sobre uma matriz de transformação própria, etc. Além disso, também há, dois métodos de classe chamados ```get_world_vertices``` e ```draw_objects```. Ambos atuam sobre todas as Areas, sendo que o primeiro as descreve guardando posições de ínicio e tamanho do vetor e retorna o global dos vértices (na main, ele é guardado e colocado em gpu). O segundo método utiliza o que foi gerado na primeira, junto com os shaders de cor e matriz de posição, para desenhar de fato os objetos na tela (é feito um loop que itera sobre cada objeto).

Por uma questão de modularização, preferimos criar uma extensão dessa classe ao herdá-la para várias outras contidas em ```actor.py```. Essas classes servem para detalhar como é feita a geração dos objetos. Por exemplo, a estrela é feita ao calcular N pontos em um círculo interno e N pontos em um círculo interno e depois fazendo um GL_TRIANGLES para juntar eles. Confira mais detalhes no método ```__init__``` de cada um. 

Por fim, colocamos como convenção essas classes terem um método chamado ```animate```, que serve para conseguir descrever como funciona a iteração da animação do objeto. Por exemplo, a estrela possui um contador interno que varia de 0 a N (parâmetro passado durante a instância do objeto). Quando inicia, começa a crescer o número. Ao chegar em N, começa a voltar e ir pra 0 e recomeçar o ciclo. Nesse processo, ele utiliza o método ```modify```, próprio da classe Area para poder fazer uma escala no eixo x e no eixo y. É dessa forma que é feita a animação da estrela piscar.

Para controlar quais objetos devem ser animados, existe dentro da main o método ```key_event``` que captura os eventos de teclado. Quando uma tecla é detectada, ela altera uma variável global que é verificada no ciclo principal da main que chama as funções de desenhar e animar cada grupo de objetos.

## Cena e comandos
Para o trabalho, preferimos fazer tipo um tema do espaço. Nossos atores/objetos são:
- Estrela: as estrelas começam a piscar quando é clicado 'N'.
- Meteoro: os meteoros se deslocam para baixo e giram quando é clicado 'M'.
- Nave: pode se deslocar para a direita e para a esquerda ao apertar 'A' e 'D'.
- Tiro: ativado/desativado ao clicar no 'espaço'
- Escudo: ativado/desativado ao clicar na tecla 'E'

Outros comandos:
- 'q': sai do programa
- 'p': mostra os triangulos da cena