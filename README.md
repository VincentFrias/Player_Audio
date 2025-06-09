🎵 Mini Player de Música com Controle via Mouse e Teclado
Este é um player de música simples feito em Python, usando Tkinter para a interface gráfica e Pygame para reprodução de áudio. O player permite tocar músicas de uma pasta local, com suporte para os formatos .mp3, .wav e .ogg.

Funcionalidades principais

->Reproduz músicas embaralhadas de uma pasta definida pelo usuário.
->Controles básicos via interface gráfica:
->Botão "Voltar" para música anterior.
->Botão "Pausar" para pausar ou retomar a música.
->Botão "Próxima" para avançar para a próxima música.
->Controle global por mouse (funciona mesmo com a janela fora de foco):
->Clique no botão do meio do mouse (scroll) pausa/despausa a música.
->Duplo clique rápido no botão do meio pula para a próxima música.
->Controle global por teclado:
->Pressionar Esc pausa/despausa a música.
->Duplo pressionamento rápido de Esc pula para a próxima música.
->Atalho Ctrl + Alt + Q fecha o player.
->Interface transparente e sempre no topo para acesso rápido.

#Requisitos
-Python 3.x

#Bibliotecas Python:
-pygame
-pynput

#Instale as dependências com:
->pip install pygame pynput

#Como usar

->Altere a variável PASTA_MUSICAS no código para o caminho da sua pasta de músicas.
->Execute o script Python.
->Use a interface gráfica ou os controles do mouse e teclado para controlar a reprodução.
