import re
import asyncio
import aiofiles
import random  # Importar o módulo random para embaralhar a lista

from config import chats, chats_folder, outputs_folder

# Função para extrair palavras únicas de uma lista de mensagens
def extract_unique_words(messages):
    words_set = set()
    # Regex para capturar palavras que começam com uma letra padrão e podem conter letras estrangeiras posteriormente
    word_pattern = re.compile(r'\b[a-zA-Z][\wÀ-ÖØ-öø-ÿ]*\b', re.UNICODE)
    
    for message in messages:
        words = word_pattern.findall(message)
        words_set.update(words)
    
    return list(words_set)  # Retorna as palavras como uma lista (não ordenada)

# Função assíncrona para ler mensagens de um arquivo
async def read_messages(input_file):
    async with aiofiles.open(input_file, 'r', encoding='utf-8') as file:
        content = await file.read()
        return content.splitlines()

# Função assíncrona para escrever palavras únicas em um arquivo com embaralhamento adicional
async def write_unique_words(output_file, words):
    random.shuffle(words)  # Primeiro embaralhamento
    random.shuffle(words)  # Segundo embaralhamento para aumentar a aleatoriedade
    random.shuffle(words)  # Terceiro embaralhamento para garantir aleatoriedade extra

    async with aiofiles.open(output_file, 'w', encoding='utf-8') as file:
        for word in words:
            await file.write(word + '\n')

# Função principal assíncrona
async def extract_only_words():
    all_unique_words = set()  # Conjunto para armazenar todas as palavras únicas de todos os chats
    
    for chat in chats:
        input_file = chats_folder + chat + '.txt'  # Arquivo contendo as mensagens
        print(f"Lendo {input_file}")
        
        messages = await read_messages(input_file)
        unique_words = extract_unique_words(messages)
        all_unique_words.update(unique_words)  # Adiciona as palavras únicas ao conjunto total

    all_unique_words_list = list(all_unique_words)  # Converte o conjunto para uma lista
    output_file = outputs_folder + 'all_unique_words.txt'  # Arquivo único para salvar todas as palavras
    await write_unique_words(output_file, all_unique_words_list)

    # Descomente as linhas abaixo para salvar as palavras únicas em arquivos separados para cada chat
    # for chat in chats:
    #     input_file = chats_folder + chat + '.txt'  # Arquivo contendo as mensagens
    #     output_file = outputs_folder + 'only_words_' + chat + '.txt'  # Arquivo para salvar as palavras únicas
    #     print(output_file)
        
    #     messages = await read_messages(input_file)
    #     unique_words = extract_unique_words(messages)
    #     await write_unique_words(output_file, unique_words)
