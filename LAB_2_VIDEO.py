import os


# definim aquesta funció per cridar la cmd
def runBash(command):
    os.system(command)


# a partir d'ara treballare amb mp4
def ogg_to_mp4(input_file, output):
    command = "ffmpeg -i " + input_file + " " + output
    runBash(command)


# EX 1
# trobat a https://groups.google.com/g/ffmpeg-php/c/o3AXSahoLi0
def analysis(input_file, type):
    # -hide_banner per ocultar els detalls de FFmpeg i nomes sortin les dades del video
    command = "ffmpeg -i " + input_file + " -hide_banner 2> data.txt"
    runBash(command)
    with open("data.txt") as file:
        for line in file:
            if type in line:
                print(line)
                # volia printejar unicament el valor que es demana fins la coma o el salt de linia pero no funcionava
                # print(line[line.find(type):line.find(',').__or__(line.find('\n'))])


# EX 1 (2.0)
# trobat a https://superuser.com/questions/841235/how-do-i-use-ffmpeg-to-get-the-video-resolution
# https://www.npmjs.com/package/ffprobe
def analysis2(input_file, type1, type2, type3):
    # -v quiet sets the log level as quiet meaning show no logs
    # -of default=noprint_wrappers=1 format as default with don’t print section and header

    com1 = "ffprobe -v quiet -select_streams v:0 -show_entries stream=" + type1 + " -of default=noprint_wrappers=1 " + input_file
    runBash(com1)
    com2 = "ffprobe -v quiet -select_streams v:0 -show_entries stream=" + type2 + " -sexagesimal -of default=noprint_wrappers=1 " + input_file
    runBash(com2)
    com3 = "ffprobe -v quiet -select_streams v:0 -show_entries stream=" + type3 + " -of default=noprint_wrappers=1 " + input_file
    runBash(com3)


# EX 2
def new_container(input_file, output_1, output_2, output_3):
    # -ss es posicio d'inici del video
    # -t el temps que es vol tallar el video
    # -map 0:a selecciona les pistes d'audio

    # primer tallem el video a 1 minut
    command_1 = "ffmpeg -i " + input_file + " -ss 00:01:00 -t 00:01:00 -c copy " + output_1
    runBash(command_1)
    # passem el video de 1 min a mp3
    command_2 = "ffmpeg -i " + output_1 + " -map 0:a " + output_2
    runBash(command_2)
    # passem el video de 1 min a un bitrate menor i .acc
    command_3 = "ffmpeg -i " + output_1 + " -map 0:a -b:a 10k " + output_3
    runBash(command_3)
    # juntem tot primer amb el video i mp3
    command_4 = "ffmpeg -i " + output_1 + " -i " + output_2 + " -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 BBB_ex2_mp4.mp4"
    runBash(command_4)
    # i aqui amb el video i aac
    # -map opción hace que ffmpeg sólo utilice el primer flujo de vídeo de la primera entrada y el primer flujo de audio de la segunda entrada para el archivo de salida.
    # Fuente: https://www.enmimaquinafunciona.com/pregunta/27376/como-fusionar-archivos-de-audio-y-video-en-ffmpeg
    command_5 = "ffmpeg -i " + output_1 + " -i " + output_3 + " -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 BBB_ex2_aac.mp4"
    runBash(command_5)


# EX 3
# https://ottverse.com/change-resolution-resize-scale-video-using-ffmpeg/
def resize(width, height, input_file, output):
    com = "ffmpeg -i " + input_file + " -vf scale=" + width + ":" + height + " -preset slow -crf 18 " + output
    runBash(com)


# EX 4
def check_audio(input_file):
    # seleccionem la pista de audio amb -select_streams a:0
    com = "ffprobe -v quiet -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 " + input_file + '> output.txt 2>&1'
    runBash(com)
    with open("output.txt") as file:
        for line in file:
            if 'aac' in line:
                print('Audio codec: ', line)
                print('It can fit in DVB, ISDB or DTMB brodcasting standard')
            elif 'ac-3' in line:
                print('Audio codec: ', line)
                print('It can fit in DVB, ATSC or DTMB brodcasting standard')
            elif 'mp3' in line:
                print('Audio codec: ', line)
                print('It can fit in DVB or DTMB brodcasting standard')
            elif 'mp2' in line:
                print('Audio codec: ', line)
                print('It can fit in DTMB brodcasting standard')
            elif 'dra' in line:
                print('Audio codec: ', line)
                print('It can fit in DTMB brodcasting standard')


if __name__ == '__main__':
    print('1) Parse the ffmpeg\n'
          '2) New container\n'
          '3) Resize video\n'
          '4) Check the audio tracks of the video and show the broadcasting standard video can fit')
    input = int(input('Select an option: '))

    # ogg_to_mp4("big_buck_bunny_1080p_stereo.ogg", "BBB.mp4")

    if input == 1:
        # he fet dos opcions
        print('OPCIÓ 1:')
        analysis("BBB.mp4", "Duration")
        print('OPCIÓ 2')
        analysis2("BBB.mp4", "width,height", "duration", "bit_rate")
    elif input == 2:
        new_container("BBB.mp4", "BBB_1_min.mp4", "BBB_audio.mp3", "BBB_audio_low_br.aac")
    elif input == 3:
        resize("1920", "1080", "BBB.mp4", "BBB_resize.mp4")
    elif input == 4:
        check_audio("BBB.mp4")
