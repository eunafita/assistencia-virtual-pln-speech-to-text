import pygame
from gtts import gTTS
from langdetect import detect  # Detectar idioma do texto
import logging

# Configuração dos logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para converter texto para áudio
def texto_para_audio(texto, idioma):
    try:
        # Criar objeto gTTS
        gtts_object = gTTS(text=texto, lang=idioma, slow=False)
        audio_file = f"{idioma}.mp3"
        gtts_object.save(audio_file)
        
        # Inicializar o mixer de áudio
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Esperar até o áudio terminar
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        logging.info(f"Áudio gerado com sucesso para o idioma {idioma}")
    except Exception as e:
        logging.error(f"Erro ao gerar áudio: {e}")

# Função principal
def main():
    while True:
        texto = input("Qual texto você quer que eu passe para áudio? (Digite 'sair' para encerrar): ")

        if texto.lower() == 'sair':
            break

        try:
            idioma_detectado = detect(texto)  # Detectar idioma do texto
            print(f"Texto detectado no idioma: {idioma_detectado}")

            # Se necessário, permitir que o usuário escolha outro idioma (opcional)
            idioma_destino = input("Qual idioma você deseja para o áudio? (Pressione Enter para usar o idioma detectado): ")

            if idioma_destino.strip() == '':
                idioma_destino = idioma_detectado  # Se o usuário não digitar, usa o idioma detectado

            print(f"Gerando áudio em {idioma_destino}...")
            texto_para_audio(texto, idioma_destino)

        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()
