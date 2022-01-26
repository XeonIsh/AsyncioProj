from urllib.parse import urlparse
import asyncio
import json
import os.path
import signal
import subprocess
import sys
import aiohttp

with open('links.txt') as links_file:
    links = links_file.readlines()
    links = [link.strip() for link in links]

async def download_mp3 (link: str): #funcao vai baixar o link, coverter para ogg e testar. Args: link que vc gostaria de fazer download
    filename = urlparse(link).path.split('/')[-1]

    if not os.path.exists(filename):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response: #async with aqui garante que a conexao anterior com o servidor (leitura e puxada de dados) seja encerrada assim evitamos o flood do script (nao pararia de ler)
                print('Fazendo Download: {}.'.format(link))

                with open(filename, 'wb') as the_file:
                    the_file.write(await response.read())

            print('\tSalvo como:"{}"'.format(filename))
            if response.status != 200:
                print(await response.text())
                raise Exception(
                    'Non-200 status code: {} ({})'.format(response.status, link))

            print('Download bem sucedido {}'.format(link))

    await process_mp3(filename)

async def process_mp3(mp3_filename):
            print('Processando {}'.format(mp3_filename))
            name, extension = os.path.splitext(mp3_filename)
            ogg_filename = '{}.ogg'.format(name)
            command = ['ffmpeg', '-nostats', '-loglevel', '8', '-1', mpe_filename, ogg_filename]
            print('Rodando {}'.format(' '.join(command)))
            process = await asyncio.create_subprocess_exec(*command)

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception('Non-0 exit code: {}'.format(mp3_filename))

async def main():
    tasks =[download_mp3(link) for link in links]

    await asyncio.gather(*tasks)

asyncio.run(main(), debug=True)