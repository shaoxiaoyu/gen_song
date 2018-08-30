import os
import random
import shutil
import configparser as cp


def config_reader(result_path=None, output_song_name=None, num=None):
    """
    Parse model's parameter from configuration_file
    """
    config = {}
    conf = cp.ConfigParser()

    if num is None:
        num = random.randint(0, 4)

    config_path = './config/music' + str(num) + '_config.ini'
    conf.read(config_path)

    config['period'] = float(conf.get('CONFIG', 'PERIOD'))
    config['delay'] = float(conf.get('CONFIG', 'DELAY'))
    config['config_path'] = str(conf.get('CONFIG', 'CONFIG_PATH'))
    config['accompany_music'] = str(conf.get('CONFIG', 'ACCOMPANY_MUSIC'))
    config['accompany_path'] = config['config_path'] + os.sep + config['accompany_music']
    config['speaker'] = float(conf.get('CONFIG', 'SPEAKER'))
    config['pitch'] = float(conf.get('CONFIG', 'PITCH'))
    config['speed'] = float(conf.get('CONFIG', 'SPEED'))

    if result_path is None:
        config['result_path'] = str(conf.get('CONFIG', 'RESULT_PATH'))
    else:
        config['result_path'] = result_path

    if output_song_name is None:
        config['output_song'] = str(conf.get('CONFIG', 'OUTPUT_SONG'))
        config['output_lyric'] = str(conf.get('CONFIG', 'OUTPUT_LYRIC'))

    else:
        config['output_song'] = song_name + ".mp3"
        config['output_lyric'] = song_name + ".txt"

    config['output_song_path'] = config['result_path'] + os.sep + config['output_song']
    config['output_lyric_path'] = config['result_path'] + os.sep + config['output_lyric']

    # Empty previously saved content and recreate the folder where the results are saved
    if os.path.exists(config['result_path']):
        shutil.rmtree(config['result_path'])
        os.makedirs(config['result_path'])
    else:
        os.makedirs(config['result_path'])

    conf.clear()

    return config


def generate_voice(lyricId, speaker, speed, pitch, config, lyrics):
    voice_output_path = config['result_path'] + os.sep + "{}_{}_{}_{}.mp3".format(lyricId, speaker, speed, pitch)
    if os.path.basename(voice_output_path) in os.listdir(config['result_path']):
        os.remove(voice_output_path)
        cmd = "./generate.sh {} {} {} {} {}  ".format(lyrics[lyricId],
                                                      speaker, speed, pitch, voice_output_path)
        os.system(cmd)
    else:
        cmd = "./generate.sh {} {} {} {} {}  ".format(lyrics[lyricId],
                                                      speaker, speed, pitch, voice_output_path)
        os.system(cmd)


def append_cmd(time, lyricId, speaker, speed, pitch, config, cmd_1):
    cmd_1 += "-itsoffset {0} ".format(float(time)*config['period'] + config['delay'])  # 此步操作是在计算什么时候开始插入语音
    cmd_1 += "-i " + config['result_path'] + os.sep + "{}_{}_{}_{}.mp3 ".format(lyricId, speaker, speed, pitch)
    return cmd_1


def write_lyric(time, lyricId, config, lyrics):
    with open(config['output_lyric_path'], "a") as f:
        f.write("[%02d:%02.2f] %s\n" % ((float(time)*config['period']+config['delay']) / 60,
                                        (float(time)*config['period']+config['delay']) % 60,
                                        lyrics[lyricId]))


def generate_song(lyrics, song_path, song_name, num):
    # lyrics is dict
    config = config_reader(song_path, song_name, num)

    # 准备合成音乐的命令
    cmd_0 = "ffmpeg -y -i %s " % (config['accompany_path'])
    cmd_1 = ""
    cmd_2 = "-filter_complex \
        amix=inputs={cnt}:duration=first:dropout_transition=4\
        -f mp3 \
        -async 1 \
        {output} \
        ".format(cnt=len(lyrics) + 1, output=config['output_song_path'])

    time = 0
    lyricsID = 0
    speaker = config['speaker']
    pitch = config['pitch']
    for i in range(len(lyrics)):  # time, lyricId, speaker, speed, pitch
        speed = 1.6 / config['period'] * config['speed']
        speed = float('{:.1f}'.format(speed))
        lyric_len = len(lyrics[str(i)])
        if lyric_len > 8:
            if lyric_len % 2 != 0:
                speed = speed / 8 * (lyric_len + 1)
                speed = float('{:.1f}'.format(speed))
            else:
                speed = speed / 8 * lyric_len
                speed = float('{:.1f}'.format(speed))

        tuple_config = (str(time), str(lyricsID), str(speaker), str(speed), str(pitch))

        generate_voice(*tuple_config[1:], config, lyrics)
        cmd_1 = append_cmd(*tuple_config[0:], config, cmd_1)
        write_lyric(*tuple_config[0:2], config, lyrics)

        time += 1
        lyricsID += 1

    # 结束体
    cmd_end = cmd_0 + cmd_1 + cmd_2
    # print(cmd_end)
    os.system(cmd_end)

    # Delete voice file
    for file in os.listdir(config['result_path']):
        if file == config['output_song'] or file == config['output_lyric']:
            continue
        else:
            path = config['result_path'] + os.sep + file
            os.remove(path)


if __name__ == __name__:
    """
    1.User selection music or If the user does not choose,random selection of music
    2.Add the lyrics to './lyrics.txt'
    3.The generated result is saved in './result/'
    """
    lyrics = {"0": "当所有欲望被释放",
              "1": "告诉我已爱上你",
              "2": "一起摇晃身体变烫",
              "3": "金钱摧毁多少事情",
              "4": "熄灭手指间的烟",
              "5": "爱不用怀疑没人能代替",
              "6": "倘若触景动了情",
              }
    song_path = "./ret"
    song_name = "music"
    generate_song(lyrics, song_path, song_name, num=4)