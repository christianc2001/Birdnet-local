import requests
from requests. exceptions import RequestException

TOKEN = ""
chat_id = ""
url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage"

def send_message(message_data):
        '''
        Sends message to Telegram.

        Args: message_data -> Tupple. Includes species, confidence score and time it was heard.

        '''
        species, confidence, time = message_data

        try:
            text = u'🦜' + f'Especie identificada: {species}\n Confianza: {confidence}\n Hora: {time}'

            payload = {
                            "text":text,
                            "disable_web_page_preview": False,
                            "disable_notification": False,
                            "reply_to_message_id": None,
                            "chat_id":chat_id
            }

            headers = {
                                    "accept": "application/json",
                                    "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
                                    "content-type": "application/json"
                    }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

        except RequestException as e:
                print(e)

def send_audio(audio_filename):
        '''
        Sends audio to Telegram.

        Args: audio_filename -> string. Path to the audio file to be sent.

        '''

        try:

            with open('recordings/'+audio_filename+'.wav', 'rb') as audio:

                    payload = {
                        'chat_id': chat_id,
                        'title': audio_filename+'.wav',
                        'parse_mode': 'HTML'
                    }

                    files = {
                        'audio': audio.read(),
                    }

                    requests.post("https://api.telegram.org/bot{token}/sendAudio".format(token=TOKEN), data=payload, files=files).json()
                    #response.raise_for_status()

        except RequestException as e:
            print(e)