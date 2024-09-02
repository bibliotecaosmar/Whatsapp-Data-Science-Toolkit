import asyncio

from view.main_menu import main_menu
from utils.select import select_messages_by_user
from utils.only_words import extract_only_words

def main():
    options = [
        'Load Word Database', 
        'Select Messages By User',
        ]

    main_menu(options)
    selection = input("Selecione uma opção: ")

    if selection == ('1' or options[0]):
        asyncio.run(extract_only_words())

    if selection == ('2' or options[1]):
        user        = input('Qual o usuário deseja extrair mensagens?\n')
        context     = int(input('Qual o número de contexto de mensagens?\n'))
        lower_limit = int(input('Qual o limite mínimo de caracteres de cada mensagem?\n'))

        asyncio.run(select_messages_by_user(user, context, lower_limit))