��    S      �  q   L        w     �   �  �  k  x   %
  �   �
  �   ,  a   �  �   a  M  X  �   �    (  2   D     w     �     �     �     �  
   �  	   �     �  9   �          %     +     7     C     P     a     n     �     �     �     �  (   �  +   �  E   �  9   3     m     �     �     �  !   �  	   �     �     �     �          0     7     G     V     s     �  0   �     �  
   �  
   �               (     <  
   K     V     ]  +   a     �     �     �     �  )   �     �       '        A  '   S     {     �     �     �  +   �     �     �  �  �  �   �  �     �    �     �   �  �   X  u   /  >  �  �  �  �   i   (  �   1   ""  '   T"     |"      �"     �"  
   �"     �"     �"     �"  5   �"     ##     )#     .#     >#     N#     `#     t#     �#     �#     �#     �#     �#  G   �#  G   $  C   T$  :   �$     �$  	   �$     �$     %  .   +%     Z%     g%     t%     z%  "   �%     �%     �%     �%  *   &  '   1&  *   Y&  @   �&     �&     �&     �&  	   �&      �&     '     ;'     S'     a'     h'  4   m'     �'     �'  	   �'     �'  &   �'     (     (  %   &(     L(  )   `(     �(     �(     �(     �(  0   �(     �(     �(        9                 =   M       #          8   &      2   >          6   +       "   N       D      %   3   0   S              .   (                      :      P   $   *      )   -             F       ?      ,          B      J   5   A                  1           !   C             H   	       7   
                 <      G   O          K   I      E   L      ;       R      '   Q         /           @           4    
                Harp Pedals is an application that returns the Harp's pedals settings and statistics.
                 
                This Webapp is part of a broader combinatorial and statistic study about the orchestral harp pedals,
                developed by Ricardo Bordini, Jamary Oliveira and Marcos da Silva Sampaio.
                 
            The orchestral harp has 7 pedals, one for each pitch class. Each pedal has three possible positions: flat, natural or sharp.
            We call each permutation of these 7 pedals in the three positions <b>pedal settings</b>.
            There are 2187 possible pedal settings in the harp. We create a harp pedal settings index in a base 3 numeric system:
            0, 1, 2, 10, 1, 12, 20, 21, 22, 100, 101, 102, etc.
         
            There are some statistics available, with sonority central tendency, chord type distribution, etc.
         
            This app provides a full list with all pedal 2187 settings, a table to download, and four ways to query pedal settings:
         
        Each pedal setting can have enarmonies such as C# and Db.
        A pedal setting without enarmonies will result in a heptachord, with one
        enarmony will resul in a hexachord and so on.
         
        Each pedal setting has a Interval-class vector, related to its pitch set class.
         
        Each pedal setting results in a specific pitch class set, belonged to a pitch set class, represented by a prime form.
        Some pitch set classes can be obtained from multiple pedal settings, in a "one to many" relation type.
         
        The histogram below contains the distribution of the pedal settings around the pitch set classes.
        Each square represents a pitch set class, each column represents a range of pedal settings.
        For instance, the first column contains all the set classes that can be obtained from 1 to 10 pedal settings.
         
        The table and pie chart below contain the number of pedal settings by chord type (tetrachord, pentacord, etc.).
         
        The table below contains the sum of the all pedal settings' the Interval-class vectors.
        The bar chart below contains the central tendency study, around intervals mean.
        Its Y axis contains the variation from the mean normalized by standard deviation.
         %s is not a number in base 3 between 0 and 2222222 %s is not in prime form format About All pedal settings All settings Amount Chord type Dashboard Developed by Distance from the mean (normalized by standard deviation) Enter Error Forte Class Forte class Get TXT file Get by accidents Get by index Get by prime form Harp Harp |  Home Index Insert a pcset prime form such as 02468A Insert a pcset prime form such as 02468A... Insert an index number in base 3 between 0 and 2222222, such as 20102 Insert an index number in base 3 between 0 and 2222222... Internal Server Error Interval Interval (semitones) Interval-class vector summation Intervals amount central tendency MIDI file MIT license Notes Number of Pitch Classes Number of pedal settings PC Set Page not found. Pedal settings Pedal settings by chord type Pedal settings by prime form Pedal settings by type of chord Pedal settings grouped by Prime Form - Histogram Pedals Settings Prime Form Proportion Queries Set the pedals settings: Settings Prime Form Settings index Statistics Submit Sum These queries are available in the sidebar. This page is under ^about/$ ^dashboard/$ ^dashboard/accidents$ ^dashboard/accidents/(?P<accidents>\w+)/$ ^dashboard/all/$ ^dashboard/index$ ^dashboard/index/(?P<pedal_index>\d+)/$ ^dashboard/prime$ ^dashboard/prime/(?P<pedal_prime>\w+)/$ ^dashboard/statistics/$ and by index by the pitch accidents by the resulting pitch set class prime form chord pedals settings Project-Id-Version: Harp
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2015-03-02 11:15-0300
PO-Revision-Date: 2015-03-02 11:18-0300
Last-Translator: Marcos da Silva Sampaio <marcos@sampaio.me>
Language-Team: Marcos da Silva Sampaio <marcos@sampaio.me>
Language: pt_BR
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 1.7.3
X-Poedit-SourceCharset: UTF-8
 
                Harp Pedals é uma aplicação que retorna as disposições de pedais da Harpa e estatísticas.
                 
                Este aplicativo web é parte de um estudo combinatorial e estatístico mais amplo sobre os pedais da harpa orquestral,
                desenvolvido por Ricardo Bordini, Jamary Oliveira e Marcos da Silva Sampaio.
                 
            A harpa orquestral tem 7 pedais, um para cada classe de altura. Cada pedal tem três posições possíveis: bemol, natural ou sustenido.
            Nós chamamos cada permutação desses 7 pedais nas três posições de <b>disposições de pedais</b>.
            Existem 2187 disposições de pedais possíveis na harpa. Nós criamos um índice para as disposições de pedais da harpa em um sistema numérico de base 3:
	     0, 1, 2, 10, 1, 12, 20, 21, 22, 100, 101, 102, etc.
         
            Há alguns estudos estatístico disponíveis, com o estudo de tendência central de sonoridade, distribuição de tipos de acordes, etc.
         
            Este aplicativo fornece uma lista completa das 2187 disposições de pedais, uma tabela para download, e quatro formas de consulta de disposições de pedais:
         
Cada disposição de pedais pode ter enarmonias tais como C# e Db.
Uma disposição de pedais sem enarmonias resultará em um heptacorde, com uma
enarmonia, resultará em um hexacorde, e assim por diante.
         
Cada disposição de pedais tem um vetor classe-intervalar, relacionado à sua classe de conjunto de notas.
         
Cada disposição de pedais resulta em um conjunto de classe de notas específico, pertencente a uma classe de conjunto de notas, representada por uma forma prima.
Algumas classes de conjunto de notas podem ser obtidas a partir de múltiplas disposições de pedais, em um tipo de relação "um para muitos".
         
O histograma abaixo contém a distribuição das disposições de pedais em torno de classes de conjuntos de notas.
Cada quadro representa uma classe de conjunto de notas, cada coluna representa uma faixa de número de disposições de pedais.
Por exemplo, a primeira coluna contém todas as classes de conjuntos de notas que podem ser obtidas de 1 a 10 disposições de pedais.
         
A tabela e o gráfico de torta abaixo contêm o número de disposições de pedais por tipo de acorde (tetracorde, pentacorde, etc.).
         
A tabela abaixo contém a soma dos vetores classe-intervalares de todas as disposições de pedais.
O gráfico de barras abaixo contém o estudo de tendência central, em torno da média de intervalos.
Seu eixo Y contém a variação a partir da média, normalizada pelo desvio padrão.
         %s não é um número em base 3 entre 0 e 2222222 %s não está no formato de forma prima Sobre Todas as disposições de pedais Todas as disposições Quantidade Tipo de acorde Painel Desenvolvido por  Distância da média (normalizada por desvio padrão) Entre Erro Classe de Forte Classe de Forte Obter arquivo TXT Obter por acidentes Obter por índice Obter por forma prima Harpa Harpa | Página Principal Índice Insira uma forma prima de conjunto de classes de notas, tal como 02468A Insira uma forma prima de conjunto de classes de notas, tal como 02468A Insira um índice numérico em base 3 entre 0 e 2222222, como 20102 Insira um índice numérico em base 3 entre 0 e 2222222... Erro Interno do Servidor Intervalo Intervalo (semitons) Soma de vetor classe-intervalar Tendência central de quantidade de intervalos Arquivo MIDI licença MIT Notas Número de classes de altura Número de disposições de pedais Conjunto de classe de notas Página não encontrada. Disposição de pedais Disposições de pedais por tipo de acorde Disposições de pedais por forma prima Disposições de pedais por tipo de acorde Disposições dos pedais agrupadas pela forma prima - Histograma Disposição de pedais Forma prima Proporção Consultas Defina as posições dos pedais: Forma prima da disposição Índice de disposição Estatísticas Enviar Soma Essas consultas estão disponíveis na guia lateral. Esta página está sob ^sobre/$ ^painel/$ ^painel/acidentes$ ^painel/acidentes/(?P<accidents>\w+)/$ ^painel/todas/$ ^painel/indice$ ^painel/indice/(?P<pedal_index>\d+)/$ ^painel/formaprima$ ^painel/formaprima/(?P<pedal_prime>\w+)/$ ^painel/estatisticas/$ e por índice pelos acidentes pela forma prima da classe de alturas resultante corde disposições de pedais 