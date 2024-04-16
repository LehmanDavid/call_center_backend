# #!/usr/bin/python3.6
# #coding=utf8
# import argparse
# from asterisk.agi import *

# import requests
# import grpc
# import os
# import yandex.cloud.ai.stt.v2.stt_service_pb2 as stt_service_pb2
# import yandex.cloud.ai.stt.v2.stt_service_pb2_grpc as stt_service_pb2_grpc
# agi = AGI()
# CHUNK_SIZE = 4000
# folder = "берете в яндексе"
# token = "берете в яндексе"
# text = ""


# def gen(folder_id):
#     # Задать настройки распознавания.
#     specification = stt_service_pb2.RecognitionSpec(
#         language_code='ru-RU',
#         profanity_filter=True,
#         model='general',
#         partial_results=True,
#         audio_encoding='LINEAR16_PCM',
#         sample_rate_hertz=8000
#     )

#     streaming_config = stt_service_pb2.RecognitionConfig(specification=specification, folder_id=folder_id)

#     # Отправить сообщение с настройками распознавания.
#     yield stt_service_pb2.StreamingRecognitionRequest(config=streaming_config)

#     # Прочитать аудиофайл и отправить его содержимое порциями.
#     with os.fdopen(3, 'rb') as f:
#         data = f.read(CHUNK_SIZE)
#         while data != b'':
#             yield stt_service_pb2.StreamingRecognitionRequest(audio_content=data)
#             data = f.read(CHUNK_SIZE)


# def run(folder_id, iam_token):
#     # Установить соединение с сервером.
#     cred = grpc.ssl_channel_credentials()
#     channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
#     stub = stt_service_pb2_grpc.SttServiceStub(channel)

#     # Отправить данные для распознавания.
#     it = stub.StreamingRecognize(gen(folder_id), metadata=(('authorization', 'Bearer %s' % iam_token),))

#     # Обработать ответы сервера и вывести результат в консоль.
#     try:
#         cont = True
#         while cont:
#                 agi.verbose('START START START')
#                 for r in it:
#                     try:
#                         agi.verbose('Start chunk: ')
#                         for alternative in r.chunks[0].alternatives:
#                             agi.verbose(alternative.text)
#                             if(alternative.text == "привет"):
#                                 cont = true
#                                 break
#                         if r.chunks[0].final:
#                             agi.verbose("FINAL")
#                             with open("/var/lib/asterisk/agi-bin/cloudapi/output/echo123.raw", "wb") as f:
#                                 for audio_content in synthesize(alternative.text):
#                                     f.write(audio_content)
#                             agi.stream_file("/var/lib/asterisk/agi-bin/cloudapi/output/echo123")
#                     except LookupError:
#                         agi.verbose('Not available chunks')
#     except grpc._channel._Rendezvous as err:
#         agi.verbose('Error code %s, message: %s' % (err._state.code, err._state.details))


# def synthesize(text):
#     url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
#     headers = {
#         'Authorization': 'Bearer '+token
#     }

#     data = {
#         'text': text,
#         'lang': 'ru-RU',
#         'folderId': folder,
#         'sampleRateHertz': '8000',
#         'format': 'lpcm'
#     }

#     with requests.post(url, headers=headers, data=data, stream=True) as resp:
#         if resp.status_code != 200:
#             raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

#         for chunk in resp.iter_content(chunk_size=None):
#             yield chunk



# if __name__ == '__main__':
#     run(folder,token)