from dotenv import load_dotenv
import os
import speech_recognition as sr
import pyttsx3
import logging
import webbrowser  # Para abrir o navegador
import requests  # Para fazer requisições HTTP
import wikipedia  # Para pesquisar na Wikipedia
from googleapiclient.discovery import build

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração dos logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configura o idioma da Wikipedia para português
wikipedia.set_lang("pt")

# Carregar as chaves de API do .env
google_api_key = os.getenv("GOOGLE_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")

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

# Função para escolher o artigo da Wikipedia
def escolher_artigo_wikipedia(resultados):
    if len(resultados) == 1:
        # Se há apenas um resultado, abrir diretamente
        return resultados[0]
    else:
        # Caso haja mais de um, perguntar ao usuário qual artigo ele quer
        falar_resposta(f"Eu encontrei {len(resultados)} artigos relacionados ao seu pedido.")
        for i, item in enumerate(resultados, start=1):
            print(f"{i}. {item}")  # Exibe os números e os títulos dos artigos

        # Aguardar a escolha do usuário
        falar_resposta("Diga o número do artigo que você quer abrir.")
        escolha = ouvir_audio()

        try:
            escolha_numero = int(escolha)
            if 1 <= escolha_numero <= len(resultados):
                return resultados[escolha_numero - 1]  # Retorna o artigo escolhido
            else:
                falar_resposta(f"Escolha inválida. Eu encontrei {len(resultados)} artigos. Por favor, diga um número entre 1 e {len(resultados)}.")
                return escolher_artigo_wikipedia(resultados)  # Chama novamente para a escolha
        except ValueError:
            falar_resposta("Desculpe, não entendi o número. Por favor, diga um número entre 1 e 5.")
            return escolher_artigo_wikipedia(resultados)  # Chama novamente para a escolha

# Função para pesquisar no YouTube
def pesquisar_no_youtube(query):
    youtube = build("youtube", "v3", developerKey=youtube_api_key)  # Coloque sua chave de API aqui
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=10  # Limitar a 10 resultados
    )
    response = request.execute()
    
    # Verificar se há resultados
    if 'items' in response:
        videos = []
        for i, item in enumerate(response['items']):
            # Verificar se o resultado é um vídeo (pode ser playlist, canal, etc.)
            if item['id']['kind'] == 'youtube#video':
                title = item['snippet']['title']
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append((i + 1, title, video_url))  # Armazenar o índice, título e URL do vídeo
        
        # Verificar se encontramos vídeos
        if videos:
            return videos
        else:
            return None
    else:
        return None


# Função para escolher o vídeo
def escolher_video(videos):
    while True:
        # Exibir os resultados para o usuário
        falar_resposta("Eu encontrei os seguintes vídeos. Por favor, diga o número do vídeo que você quer assistir:")
        for i, video in enumerate(videos, start=1):
            print(f"{i}. {video[1]}")  # Exibe o número e o título do vídeo
        
        # Aguardar a fala do usuário com o número escolhido
        escolha = ouvir_audio()
        print(f"Escolha reconhecida: {escolha}")
        
        # Verificar se o número está na lista de vídeos
        try:
            escolha_numero = int(escolha)
            if 1 <= escolha_numero <= len(videos):
                return videos[escolha_numero - 1][2]  # Retorna o URL do vídeo escolhido
            else:
                falar_resposta(f"Escolha inválida. Eu encontrei {len(videos)} vídeos, por favor, diga um número entre 1 e {len(videos)}.")
        except ValueError:
            falar_resposta("Desculpe, não entendi o número. Por favor, diga um número entre 1 e 10.")
    
# Função para obter o clima usando a API do OpenWeatherMap
def obter_clima_por_cidade(cidade, estado):
    # Usando a chave de API do OpenWeatherMap do .env
    chave_api = openweathermap_api_key
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
            videos = pesquisar_no_youtube(pesquisa)

            if videos:
                falar_resposta(f"Eu encontrei {len(videos)} resultados relacionados ao seu pedido.")
                logging.info(f"Resultados encontrados: {videos}")

                # Permitir que o usuário escolha um vídeo
                url_video = escolher_video(videos)
                falar_resposta(f"Abrindo o vídeo: {url_video}")
                webbrowser.open(url_video)  # Abrir o link do vídeo no navegador
            else:
                falar_resposta("Desculpe, não encontrei vídeos relacionados ao seu pedido.")

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
                # Escolher qual artigo abrir
                artigo = escolher_artigo_wikipedia(resultados)
                if artigo:
                    # Abrir o artigo na Wikipedia
                    pagina = wikipedia.page(artigo)
                    url = pagina.url
                    falar_resposta(f"Abrindo o artigo: {artigo}")
                    logging.info(f"Abrindo o artigo: {url}")
                    webbrowser.open(url)
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
