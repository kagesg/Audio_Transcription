#Bibliotecas a serem utilizadas
from pydub import AudioSegment
import speech_recognition as sr
import time


# ========================================================================================================================== #
#IMPORTANTE!
#É necessário instalar FFmpeg no seu computador
#Procedimento para Windows: http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/
#
# ========================================================================================================================== #


#Marcar tempo incial do programa
tempo_ini = time.time()

#Lista com os nomes dos arquivos (Os arquivos devem estar no formato .wav)
#Exemplo: lista = ["Audio_1.wav","Audio_2.wav","Audio_3.wav"]
lista = ['Audio_1.wav']

#Caminho no qual se encontram os arquivos de audio a serem transcritos
#Exemplo: diretorio = 'C:\\Users\\gusta\\OneDrive\\MeusProjetos\\Transcription\\Teste'
diretorio = 'C:\\Users\\gusta\\OneDrive\\MeusProjetos\\Transcription\\Teste'

#Declarando a variavel que será inserido a transcrição
transcricao = str()

for nome_arquivo in lista:
    #Importando o audio
    audio = AudioSegment.from_wav(diretorio+'\\'+nome_arquivo)

    #Conversão do tempo total do audio de milissegundos para segundos
    t_seg = len(audio)/1000

    #Tempo de cada segmento do audio total
    #É necessário pois há um limite de tamanho do arquivo para a API Speech-to-text da Google. Ver mais em Referência [1]
    #Nos meus testes e pelos tamanhos dos audios transcritos, cada segmento de 55 seg = arquivo de +- 9 MB
    seg_por_div = 55

    #Teste para ver se terá um numero de quebras inteiro, caso contrário, irá arredondar o tempo total do arquivo para um multiplo de seg_por_div
    if (t_seg % seg_por_div) != 0:
        t_seg = round(t_seg/seg_por_div)*seg_por_div

    #Texto para validar qual arquivo foi carregado e sinalizar o inicio da transcrição
    print('='*50)
    print('\n\nArquivo {} lido com sucesso!\n\n'.format(nome_arquivo))
    print('\n\nIniciando transcricão...\n\n')

    #Laço para realizar a transcrição de cada sessão do audio
    for i in range(0, t_seg, seg_por_div):

        #Carrega o audio inteiro e depois recorta apenas um segmento dele na variável audio_div
        #Referência [2]
        r = sr.Recognizer()
        with sr.AudioFile(diretorio+'\\'+nome_arquivo) as source:
            audio_div = r.record(source, offset=i, duration=seg_por_div)  

        #Realiza a transcrição da sessão do audio selecionado anterioremente.
        #Configurado para a linguagem pt-BR. Referência [3]
        #Uso do try para em caso de erro, ele apontar no meio do arquivo transcrição.txt
        try:
            transcricao += ' ' + r.recognize_google(audio_div, language='pt-BR')
        except sr.UnknownValueError:
            transcricao += ' ' + '____#ERRO#____'
            print('____#ERRO#____')
        except sr.RequestError as e:
            transcricao += ' ' + '____#ERRO#____'
            print('____#ERRO#____')
    
    #Cria arquivo .txt com o resultado da transcrição total do audio 
    file = open('Transcricao_'+nome_arquivo[0:-4]+'.txt', 'w+')
    file.write(transcricao)
    file.close()

#Marcar tempo final do programa
tempo_fim = time.time()

#Mensagem sinalizando o final da transcrição e tempo de operação
print('\n\nTranscrição finalizada com sucesso!!')
print('Tempo de operação: {:.2f} segundos.\n\n'.format((tempo_fim-tempo_ini)))
print('='*50)


# ========================================================================================================================== #
# Referências para a construção do código:
#
# [1]Consultado de: https://cloud.google.com/speech-to-text/quotas#:~:text=for%20more%20information.-,Content%20Limits,the%20API%20using%20local%20files.
# [2]Retirado e editado de: https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
# [3]Consultado de: https://cloud.google.com/speech-to-text/docs/languages
#
# ========================================================================================================================== #