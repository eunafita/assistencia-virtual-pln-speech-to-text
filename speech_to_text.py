import speech_recognition as sr
import pyttsx3
import logging
import webbrowser  # Para abrir o navegador
import requests  # Para fazer requisições HTTP
import wikipedia  # Para pesquisar na Wikipedia
from googleapiclient.discovery import build

# Configuração dos logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configura o idioma da Wikipedia para português
wikipedia.set_lang("pt")

# Sua chave da API do Google
google_api_key = "SUA_CHAVE_API_DO_GOOGLE"

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

# Função para falar a resposta em áudio
def falar_resposta(resposta):
    engine = pyttsx3.init()
    engine.say(resposta)
    engine.runAndWait()
    logging.info(f"Resposta falada: {resposta}")

# Função para pesquisar lugares no Google Places API
def pesquisar_lugares(tipo_de_estabelecimento, cidade, estado):
    # Buscando as coordenadas da cidade com a Geocoding API
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={cidade},{estado}&key={google_api_key}"
    response = requests.get(geocoding_url)
    location_data = response.json()

    logging.info(f"Resposta da API de Geocodificação: {location_data}")

    if location_data['status'] == 'OK':
        # Pegando a latitude e longitude da localização
        latitude = location_data['results'][0]['geometry']['location']['lat']
        longitude = location_data['results'][0]['geometry']['location']['lng']
        logging.info(f"Localização encontrada: Latitude = {latitude}, Longitude = {longitude}")
        
        # Agora, com a localização, vamos buscar lugares nas proximidades com o Places API
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type={tipo_de_estabelecimento}&key={google_api_key}"
        places_response = requests.get(places_url)
        places_data = places_response.json()

        logging.info(f"Resposta da API Places: {places_data}")

        if places_data['status'] == 'OK':
            lugares = []
            for place in places_data['results']:
                nome = place['name']
                endereco = place['vicinity']
                lugares.append(f"{nome} - {endereco}")
            return lugares
        else:
            return ["Não encontrei lugares próximos."]
    else:
        return ["Não consegui obter a sua localização."]

# Função para pesquisar na Wikipedia e listar páginas
def pesquisar_na_wikipedia(query):
    try:
        # Buscando páginas relacionadas
        results = wikipedia.search(query, results=5)  # Limitar a 5 resultados
        if results:
            return results
        else:
            return None
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ambiguidade encontrada: {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Desculpe, houve um problema ao acessar a Wikipedia. Tente novamente mais tarde."
    except wikipedia.exceptions.ConnectionError:
        return "Desculpe, não conseguimos se conectar à Wikipedia. Verifique sua conexão com a internet."
    except wikipedia.exceptions.PageError:
        return "Desculpe, não encontrei informações sobre este tópico na Wikipedia."

# Função para pesquisar no YouTube
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
                
        elif 'wikipedia' in comando or 'wikipédia' in comando:
            logging.info("Comando 'wikipedia' ou 'wikipédia' detectado.")
            falar_resposta("O que você quer pesquisar na Wikipedia?")
            print("O que você quer pesquisar na Wikipedia?")
            pesquisa = ouvir_audio()
            resultados = pesquisar_na_wikipedia(pesquisa)
            
            if resultados:
                resposta = f"Eu encontrei {len(resultados)} artigos relacionados ao seu pedido."
                falar_resposta(resposta)
                logging.info(f"Resultados encontrados: {resultados}")
                
                # Mostrar os resultados para o usuário
                for i, item in enumerate(resultados, start=1):
                    print(f"{i}. {item}")
                
                # Abrir a primeira página no navegador
                primeira_pagina = wikipedia.page(resultados[0])  # A primeira página da lista
                webbrowser.open(primeira_pagina.url)  # Abrir a URL da primeira página encontrada
                falar_resposta(f"Abrindo o artigo {resultados[0]}.")
            else:
                falar_resposta("Desculpe, não encontrei informações sobre esse tópico na Wikipedia.")
        elif 'procurar' in comando or 'encontrar' in comando or 'buscar' in comando or 'onde' in comando:
            logging.info("Comando de busca detectado.")
            falar_resposta("O que você gostaria de procurar? Mercado, hospital, restaurante ou outro tipo de estabelecimento?")
            print("O que você gostaria de procurar? Mercado, hospital, restaurante ou outro tipo de estabelecimento?")
            tipo_de_estabelecimento = ouvir_audio()

            # Perguntar ao usuário onde ele está (cidade e estado)
            falar_resposta("Em qual cidade e estado você está?")
            print("Em qual cidade e estado você está?")
            cidade_estado = ouvir_audio()

            # Dividir a entrada para cidade e estado
            cidade_estado_split = cidade_estado.split("em")
            if len(cidade_estado_split) == 2:
                cidade = cidade_estado_split[1].strip()
                estado = cidade_estado_split[0].strip()
            else:
                cidade = cidade_estado_split[0].strip()
                estado = ""  # Deixar vazio se o estado não for mencionado

            tipo_de_estabelecimento = tipo_de_estabelecimento.replace(" ", "").lower()  # Para aceitar o termo "mercado" ou "hospital"
            lugares = pesquisar_lugares(tipo_de_estabelecimento, cidade, estado)
            
            if lugares:
                resposta = f"Encontrei {len(lugares)} lugares relacionados na sua região."
                falar_resposta(resposta)
                logging.info(f"Lugares encontrados: {lugares}")

                # Mostrar os resultados para o usuário
                for i, lugar in enumerate(lugares, start=1):
                    print(f"{i}. {lugar}")
                
                # Abrir o primeiro resultado no navegador
                primeiro_lugar = lugares[0]
                falar_resposta(f"Abrindo o estabelecimento: {primeiro_lugar}.")
                webbrowser.open(f"https://www.google.com/maps?q={primeiro_lugar}")
            else:
                falar_resposta("Desculpe, não encontrei lugares na sua região.")
        else:
            logging.warning("Comando não reconhecido. Esperando novo comando.")
            falar_resposta("Comando não reconhecido. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
