import speech_recognition as sr
import pyttsx3
from googleapiclient.discovery import build
import logging
import webbrowser  # Para abrir o navegador
import requests  # Para fazer requisições HTTP

# Configuração dos logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para ouvir e reconhecer o áudio
def ouvir_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Aguardando sua fala...")
        print("Aguardando sua fala...")
        audio = recognizer.listen(source)
        texto = recognizer.recognize_google(audio, language='pt-BR')
        logging.info(f"Áudio reconhecido: {texto}")
        return texto.lower()

# Função para realizar pesquisa no YouTube
def pesquisar_no_youtube(query):
    youtube = build("youtube", "v3", developerKey="SUA_CHAVE_API_DO_YOUTUBE")  # Coloque sua chave de API aqui
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=1
    )
    response = request.execute()
    video = response['items'][0]['snippet']
    logging.info(f"Resultado da pesquisa no YouTube: {video['title']}")
    video_url = f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"  # Cria a URL do vídeo
    return video['title'], video['description'], video_url  # Inclui a URL do vídeo

# Função para obter o clima usando a API do OpenWeatherMap
def obter_clima_por_cidade(cidade, estado):
    chave_api = "1d85ee02c30d68103bdbf25f8161a9a3"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},{estado}&appid={chave_api}&units=metric&lang=pt_br"
    
    response = requests.get(url)
    data = response.json()
    
    # Informações do clima
    if response.status_code == 200:
        clima = data['weather'][0]['description']
        temperatura = data['main']['temp']
        cidade = data['name']
        cidade_id = data['id']  # Obter o ID da cidade
        return clima, temperatura, cidade, cidade_id
    else:
        return None, None, None, None

# Função para falar a resposta em áudio
def falar_resposta(resposta):
    engine = pyttsx3.init()
    engine.say(resposta)
    engine.runAndWait()
    logging.info(f"Resposta falada: {resposta}")

# Passo 3: Sistema principal
def main():
    while True:
        logging.info("Sistema iniciado, aguardando comando...")
        comando = ouvir_audio()

        if 'youtube' in comando:
            logging.info("Comando 'youtube' detectado.")
            falar_resposta("O que você quer procurar no YouTube?")
            print("O que você quer procurar no YouTube?")
            pesquisa = ouvir_audio()
            titulo, descricao, url = pesquisar_no_youtube(pesquisa)
            resposta = f"Encontrei o vídeo: {titulo}. Descrição: {descricao}"
            falar_resposta(resposta)
            logging.info(f"Abrindo o vídeo no navegador: {url}")
            webbrowser.open(url)  # Abre o link do vídeo no navegador
        elif 'tempo' in comando:
            # Perguntar ao usuário qual cidade e estado
            falar_resposta("Em qual cidade e estado você gostaria de saber o clima?")
            print("Em qual cidade e estado você gostaria de saber o clima?")
            cidade_estado = ouvir_audio()

            # Dividir a entrada para cidade e estado
            cidade_estado_split = cidade_estado.split("em")
            if len(cidade_estado_split) == 2:
                cidade = cidade_estado_split[1].strip()
                estado = cidade_estado_split[0].strip()
            else:
                cidade = cidade_estado_split[0].strip()
                estado = ""  # Deixar vazio se o estado não for mencionado

            clima, temperatura, cidade, cidade_id = obter_clima_por_cidade(cidade, estado)
            if clima and temperatura:
                resposta = f"O tempo em {cidade} está {clima} com temperatura de {temperatura}°C."
                falar_resposta(resposta)
                logging.info(f"Clima: {resposta}")
                # Abrir o OpenWeatherMap com a cidade usando o ID
                url = f"https://openweathermap.org/city/{cidade_id}"
                webbrowser.open(url)  # Abre o site com as informações do clima
            else:
                falar_resposta("Desculpe, não consegui obter as informações do tempo.")
        else:
            logging.warning("Comando não reconhecido. Esperando novo comando.")
            falar_resposta("Comando não reconhecido. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
