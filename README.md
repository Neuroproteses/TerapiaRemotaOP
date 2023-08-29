# TerapiaRemotaOP
Sistema para terapia remota focado nos membros superiores utilizando o OpenPose

# Instalação
Para utilizar o sistema é necessario instalar o OpenPose separadamente, para isto é recomendado seguir as isntruções na pagina do GitHub do proprio OpenPose.
Caso haja problemas muitas das soluções podem ser encontradas na pagina do OpenPose

# Calibração
O ângulo e posição da câmera afetam de grande forma a precisão do sistema e, portanto, para o uso é essencial que seja feita uma calibração individual para cada usuário ou computador.

Para ser feita esta calibração deve-se abrir o OpenPose no promp de comando utilizando a seguinte função: “in\OpenPoseDemo.exe --hand --write_json output_json_folder/”, isto abrirá o OpenPose e iniciará uma gravação das coordenadas em um arquivo JSON na pasta de nome “output_json_folder” que pode ser encontrada na mesma localização do OpenPose. Os arquivos gravados terão como nome o número do frame; portanto, uma pessoa sem comprometimento motor deve realizar o exercício e observar o frame que este foi realizado. Após selecionado o arquivo JSON com as coordenadas corretas este deve ser copiado para a pasta onde se encontra o código que faz a comparação e o nome do arquivo deve ser alterado para ser igual ao exercício correspondente que já está na pasta. É importante também lembrar de deletar todos os arquivos que não forem ser utilizados para evitar que estes interfiram no sistema.

# Exercícios
Os 4 exercícios são descritos abaixo:
1.	Um simples exercício de abrir a mão, com a palma apontada para a câmera. Este exercício por ser bem simples é perfeito para ser utilizado como forma de verificação se o jogo e o OpenPose estão lendo as coordenadas corretamente.
2.	Um exercício de pegar uma escova de dentes, este exercício consiste no movimento de fechar a mão completamente para pegar um objeto.
3.	Um exercício de pegar um pedaço de pão, este exercício consiste no movimento de pegar um objeto maior, porém fino precisando que a mão esteja um pouco mais aberta.
4.	Um exercício de pegar um copo, este exercício consiste no movimento de pegar um objeto tanto maior quanto mais largo precisando que a mão esteja ainda mais aberta.

# Pontuação
| Erro medio(%) | Avaliação | Pontuação |
| :---          |     :---:      |          ---: |
| 0-5           | Perfeito       | 91-100        |
| 6-10          | Otimo          | 71-90         |
| 11-20         | Bom            | 51-70         |
| 21-40         | Errado         | 11-50         |
| 41-60         | Muito errado   | 1-10          |
| 71-100        | Possivel erro  | 0             |

# Como jogar
Com a calibração feita o usuário pode abrir o jogo e selecionar qual exercício deseja realizar. É importante que o usuário foque na posição final demonstrada na animação e não no movimento em si. A pontuação será dada após o exercício ser completado e a avaliação da qualidade do exercício segue de acordo com o que foi visto na Tabela.
A pontuação é salva e pode ser verificada clicando no botão "Avaliação"

# Possiveis erros e soluções
