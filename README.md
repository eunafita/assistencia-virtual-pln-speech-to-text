# **Sistema de Assistência Virtual com Processamento de Linguagem Natural**

Este projeto consiste em um sistema de assistência virtual que utiliza técnicas de Processamento de Linguagem Natural (PLN) para realizar diversas funções, como conversão de texto em áudio, reconhecimento de fala para texto e execução de ações automatizadas via comando de voz. O sistema é dividido em três módulos principais:

## Módulos do Sistema
## **1. Conversão de Texto em Áudio (Text-to-Speech)**
   
Este módulo é responsável por converter texto em áudio utilizando a tecnologia de **Text-to-Speech (TTS)**. O sistema usa a biblioteca gTTS para gerar arquivos de áudio a partir do texto fornecido. O áudio gerado pode ser reproduzido utilizando a biblioteca pygame.

* Funcionalidades:
  * Recebe uma string de texto e converte em um arquivo de áudio.
  * Suporta múltiplos idiomas, com a identificação automática do idioma se necessário.
    
## **2. Conversão de Áudio em Texto (Speech-to-Text)**

Este módulo permite que o sistema reconheça comandos de voz e execute ações baseadas nesses comandos. Utilizando a biblioteca SpeechRecognition, o sistema converte a fala em texto e responde com base em um conjunto de funcionalidades integradas.

* Funcionalidades:
  * Converte fala em texto utilizando o Google Speech API.
  * Comandos de voz para realizar pesquisas no YouTube, buscar informações na Wikipedia, obter a previsão do tempo e pesquisar estabelecimentos próximos.

## **3. Assistente de Pesquisa via Áudio**

O assistente permite realizar pesquisas utilizando comandos de voz. Após a conversão da fala em texto, o sistema executa ações como:

* Pesquisa no YouTube: Realiza buscas de vídeos no YouTube.
* Pesquisa na Wikipedia: Realiza buscas por artigos relacionados a um tópico na Wikipedia.
* Previsão do Tempo: Obtém informações sobre a previsão do tempo para uma cidade e estado específicos.
* Pesquisa de Estabelecimentos Próximos: Localiza farmácias, mercados, hospitais e outros estabelecimentos próximos à sua localização ou cidade informada.

## **Projetos do Repositório**

Este repositório contém os seguintes projetos:

### **1. speech_to_text.py**
   
Este projeto contém a implementação principal do assistente virtual com reconhecimento de fala para texto. Ele utiliza a API de reconhecimento de fala do Google para interpretar comandos de voz e acionar ações, como:

* Pesquisar vídeos no YouTube.
* Pesquisar artigos na Wikipedia.
* Consultar a previsão do tempo.
* Encontrar estabelecimentos próximos usando a Google Places API.

**Como funciona:**

* O sistema aguarda comandos de voz e, ao reconhecer o comando "buscar", solicita ao usuário o tipo de estabelecimento e a cidade/estado para realizar a pesquisa.
* Também executa pesquisas no YouTube e Wikipedia, permitindo ao usuário interagir com o sistema por voz.

### **2. text_to_speech.py**

Este projeto realiza a conversão de texto em áudio (Text-to-Speech). O código usa a biblioteca gTTS para gerar arquivos de áudio a partir de texto e pygame para reproduzi-los.

**Como funciona:**

* O texto fornecido é convertido em áudio e salvo como um arquivo MP3.
* O áudio gerado pode ser reproduzido para o usuário de forma fluída.
* Suporta múltiplos idiomas, incluindo inglês, português e francês, com possibilidade de ajustar a velocidade da fala.

### **3. text_to_speech_input.py**

Este módulo realiza a conversão de texto em áudio a partir de um prompt de entrada do usuário. O usuário digita o texto que deseja que seja transformado em áudio e, em seguida, o sistema executa a conversão automaticamente.

**Como funciona:**

* O sistema solicita ao usuário que insira o texto que deseja converter.
* O texto é transformado em áudio e reproduzido para o usuário.
* O sistema tenta identificar o idioma automaticamente, mas o usuário pode especificar o idioma manualmente se necessário.

## Requisitos

Antes de executar o projeto, instale as dependências necessárias:

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```
2. Navegue até o diretório do projeto:

```bash
cd nome-do-repositorio
```
3. Instale as dependências utilizando o requirements.txt:

```bash
pip install -r requirements.txt
```

As bibliotecas necessárias incluem:

* speechrecognition
* pyttsx3
* google-api-python-client
* requests
* geocoder
* pyaudio
* wikipedia
* python-dotenv
* pygame
* gTTS
* langdetect

## Configuração das APIs

Este projeto utiliza chaves de API para acessar serviços externos como o YouTube, Google Maps e OpenWeatherMap. Para garantir a segurança e evitar a exposição das credenciais diretamente no código, as chaves de API são armazenadas em um arquivo .env, que é carregado automaticamente.

### Onde conseguir suas chaves de API
1. **Chave API do Google Maps**(para Google Maps, Geocoding API e Places API)
    * Acesse o [Console de APIs do Google](https://console.cloud.google.com/apis/dashboard)
    * Crie um novo projeto ou selecione um existente.
    * Ative as APIs necessárias:
    * **Geocoding API** (para obter a localização a partir de um endereço).
    * **Places API** (para pesquisar lugares próximos).
    * Após ativar as APIs, gere a chave de API do **Google Maps Platform API Key** que já engloba as API's `Places` e `Geocoding`.
    * Adicione a chave gerada do **Google Maps Platform API Key** no arquivo `.env` com a variável `GOOGLE_API_KEY`.

2. **Chave API do YouTube** (necessária dentro do projeto do Google)

    * Ative a **YouTube Data API v3**
    * Ativar a **YouTube Data API v3** no console de APIs do Google para poder realizar pesquisas de vídeos.
    * Adicione a chave gerada do **YouTube Data API v3** no arquivo `.env` com a variável `YOUTUBE_API_KEY`.

3. **Chave API para o OpenWeatherMap** (para previsão do tempo)
    * Cadastre-se no [OpenWeatherMap](https://home.openweathermap.org/api_keys).
    * Crie um cadastro simples e gere sua chave da API para acessar a previsão do tempo.
    * Coloque a chave gerada [AQUI](https://home.openweathermap.org/api_keys) no arquivo .env com a variável `OPENWEATHERMAP_API_KEY`.
  
### Exemplo de Arquivo `.env`

O arquivo `.env` deve estar na raiz do seu projeto, contendo as chaves de API que você obteve dos serviços mencionados. O formato do arquivo será o seguinte:

```env
GOOGLE_API_KEY=Sua_chave_do_Google_API
YOUTUBE_API_KEY=Sua_chave_do_YouTube_API
OPENWEATHERMAP_API_KEY=Sua_chave_do_OpenWeatherMap_API
```
### Observações Importantes

  * **Cartão de Crédito:** Tanto as **APIs do Google** (incluindo YouTube, Geocoding e Places) quanto a **API do OpenWeatherMap** exigem o preenchimento de um cartão de crédito válido durante o cadastro. No entanto, para fins de teste, o uso gratuito fornecido pelas APIs é mais do que suficiente, e você não será cobrado se ficar dentro do limite gratuito.
  * Após configurar suas chaves de API, não se esqueça de garantir que o arquivo `.env` não seja compartilhado publicamente, adicionando-o ao seu `.gitignore`.

## Como Usar
### Para o `speech_to_text.py`:
1. Execute o arquivo:
```bash
python speech_to_text.py
```

2. Fale um comando, como:
    * "Pesquisar no YouTube sobre Galinha Pintadinha"
    * "Qual a previsão do tempo para São Paulo?"
    * "Onde posso encontrar um hospital em Maringá?"

### Para o `text_to_speech.py`:
1. Execute o arquivo:
```bash
python text_to_speech.py
```

2. O sistema converterá o texto em áudio e o reproduzirá. Você pode adicionar novas frases no código para testá-las.

### Para o `text_to_speech_input.py`:
1. Execute o arquivo:
```bash
python text_to_speech_input.py
```
2. Digite o texto que deseja converter em áudio e ele será falado de volta.

## Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

## Contribuições
Sinta-se à vontade para contribuir com melhorias, sugestões ou correções de bugs. Basta criar um fork do repositório, fazer suas alterações e enviar um pull request!

## Contato
Para dúvidas ou contribuições, você pode entrar em contato comigo:
* Rafael Bortoluzzi
* E-mail: rafaeldnbr@hotmail.com
  
Fique à vontade para entrar em contato se precisar de ajuda ou quiser colaborar com melhorias neste projeto.
