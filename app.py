from sclib import SoundcloudAPI, Track, Playlist
import time
from subprocess import check_output
import urllib
import random

"""
api = SoundcloudAPI()
playlist = SoundcloudAPI().resolve('https://soundcloud.com/flechamagica/sets/musicas-medievais-de-rpg')
assert type(playlist) is Playlist
for track in playlist.tracks:
    #filename = f'./{track.artist} - {track.title}.mp3'
    print(track.permalink_url)
    tempo = int(track.duration * 0.001) + 1
    track2 = api.resolve(track.permalink_url)
    assert type(track2) is Track
    with open('musica.mp3', 'wb+') as fp:
        track2.write_mp3_to(fp)
        fp.close()

    check_output("start musica.mp3", shell=True)
    time.sleep(tempo)
    check_output("nircmd.exe mutesysvolume 1", shell=True)
    print('fim')
    break
"""



def download_musica(musica):
    try:
        track = SoundcloudAPI().resolve(musica['url'])
        assert type(track) is Track
        with open('musica.mp3', 'wb+') as fp:
            track.write_mp3_to(fp)
            fp.close()
    except Exception as e:
        print("Erro: " + str(e))

def tocar_musica(musica):
    try:
        print("Tocar musica: " + musica['nome'] + " de " + musica['artista'])
        check_output("start musica.mp3", shell=True)
        time.sleep(musica['duracao'])
    except Exception as e:
        print("Erro: " + str(e))

def volume_maximo():
    try:
        check_output("nircmd.exe mutesysvolume 0", shell=True)
        check_output("nircmd.exe setsysvolume 65535", shell=True)
    except Exception as e:
        print("Erro: " + str(e))

def abaixar_volume():
    try:
        max_volume = 65535
        i = max_volume
        while i > 2000:
            check_output("nircmd.exe changesysvolume -1000", shell=True)
            i -= 1000
        check_output("nircmd.exe mutesysvolume 1", shell=True)
    except Exception as e:
        print("Erro: " + str(e))

def obter_playlists():
    playlists = []
    try:
        file_name = "playlists.txt"
        urllib.request.urlretrieve("https://flechamagica.com.br/playlists.txt", file_name)
        file = open(file_name, "r")
        for line in file:
            playlists.append(line.strip())
        file.close()
    except Exception as e:
        print("Erro: " + str(e))
    return playlists

def obter_musicas():
    musicas = []
    try:
        playlists = obter_playlists()
        for playlist_url in playlists:
            playlist = SoundcloudAPI().resolve(playlist_url)
            assert type(playlist) is Playlist
            for track in playlist.tracks:
                if isinstance(track.permalink_url, str):
                    musica = {
                        'url': track.permalink_url,
                        'duracao': int(track.duration * 0.001) + 1,
                        'artista': track.artist,
                        'nome': track.title
                    }
                    musicas.append(musica)
    except Exception as e:
        print("Erro: " + str(e))
    return musicas

def escolher_musica(lista_para_tocar):
    try:
        musica = random.choice(lista_para_tocar)
        f1 = open("musica.txt", "w")
        f1.write(musica['nome'])
        f1.close()
        f2 = open("artista.txt", "w")
        f2.write(musica['artista'])
        f2.close()
        return musica
    except Exception as e:
        print("Erro: " + str(e))

def main():
    while True:
        try:
            lista_para_tocar = obter_musicas()
            lista_tocada = []
            while len(lista_para_tocar) > 0:
                try:
                    musica = escolher_musica(lista_para_tocar)
                    lista_tocada.append(musica)
                    lista_para_tocar = [m for m in lista_para_tocar if m['url'] != musica['url']]
                    download_musica(musica)
                    volume_maximo()
                    tocar_musica(musica)
                    abaixar_volume()
                except Exception as e:
                    print("Erro: " + str(e))
        except Exception as e:
            print("Erro: " + str(e))

main()
