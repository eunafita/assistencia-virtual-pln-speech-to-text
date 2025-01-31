import speech_recognition as sr
import pyttsx3
import logging
import webbrowser  # Para abrir o navegador
import requests  # Para fazer requisições HTTP

# Configuração dos logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sua chave da API do Google
google_api_key = "AIzaSyB42ScQJRQU3F2vxwO-y7tM6UDXWbKL87w"

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

    # Log da resposta da API
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

        # Log da resposta do Places API
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

# Passo 3: Sistema principal
def main():
    while True:
        logging.info("Sistema iniciado, aguardando comando...")
        comando = ouvir_audio()

        # Verifica se o comando contém palavras-chave de pesquisa de lugares
        if 'procurar' in comando or 'encontrar' in comando or 'buscar' in comando or 'onde' in comando:
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

            # Converter a descrição do tipo de estabelecimento para tipo de lugar
            tipo_de_estabelecimento = tipo_de_estabelecimento.replace(" ", "").lower()  # Para aceitar o termo "mercado" ou "hospital"
            lugares = pesquisar_lugares(tipo_de_estabelecimento, cidade, estado)
            
            if lugares:
                resposta = f"Encontrei {len(lugares)} lugares relacionados na sua região."
                falar_resposta(resposta)
                logging.info(f"Lugares encontrados: {lugares}")

                # Mostrar os resultados para o usuário
                for i, lugar in enumerate(lugares, start=1):
                    print(f"{i}. {lugar}")
                
                # Abrir o primeiro resultado no navegador (opcional)
                primeiro_lugar = lugares[0]
                falar_resposta(f"Abrindo o estabelecimento: {primeiro_lugar}.")
                # Aqui você poderia abrir o Google Maps ou o link do estabelecimento no navegador
                webbrowser.open(f"https://www.google.com/maps?q={primeiro_lugar}")
            else:
                falar_resposta("Desculpe, não encontrei lugares na sua região.")
        else:
            logging.warning("Comando não reconhecido. Esperando novo comando.")
            falar_resposta("Comando não reconhecido. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
