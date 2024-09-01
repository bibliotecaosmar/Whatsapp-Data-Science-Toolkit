import asyncio

from view import menu
from select_messages.select import select_messages_by_user

def main():
    options = [
        'Load Word Database', 
        'Select Messages By User',
        ]

    menu(options)
    selection = input("Selecione uma opção: ")

    if selection == '1' or options[0]:
        asyncio.run(exec())

    if selection == '2' or options[1]:
        user        = input('Qual o usuário deseja extrair mensagens?\n')
        context     = int(input('Qual o número de contexto de mensagens?\n'))
        lower_limit = int(input('Qual o limite mínimo de caracteres de cada mensagem?\n'))

        asyncio.run(select_messages_by_user(user, context, lower_limit))