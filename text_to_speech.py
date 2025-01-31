import pygame
from gtts import gTTS

# Gerar áudio
text_to_say = "How are you doing?."
language = "en"
gtts_object = gTTS(text=text_to_say, lang=language, slow=False)
gtts_object.save("gtts.mp3")

# Inicializar o mixer de áudio
pygame.mixer.init()

# Tocar o áudio
pygame.mixer.music.load("gtts.mp3")
pygame.mixer.music.play()

# Esperar até terminar de tocar
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

french_text = "Je vais au supermarché"

french_language = "fr"

french_gtts_object = gTTS(text = french_text,
                          lang = french_language,
                          slow = True)

french_gtts_object.save("french.mp3")

# Inicializar o mixer de áudio
pygame.mixer.init()

# Tocar o áudio
pygame.mixer.music.load("french.mp3")
pygame.mixer.music.play()

# Esperar até terminar de tocar
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# Frase em português
portuguese_text = "Vamos jogar bola na quadra"

# Idioma do português brasileiro
portuguese_language = "pt"

# Criar o objeto gTTS para a frase
portuguese_gtts_object = gTTS(text=portuguese_text, lang=portuguese_language, slow=False)

# Salvar o áudio em mp3
portuguese_gtts_object.save("portuguese.mp3")

# Inicializar o mixer de áudio
pygame.mixer.init()

# Tocar o áudio
pygame.mixer.music.load("portuguese.mp3")
pygame.mixer.music.play()

# Esperar até terminar de tocar
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)