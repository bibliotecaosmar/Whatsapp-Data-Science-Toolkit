import re
import aiofiles
import asyncio
from datetime import datetime

from config import chats, outputs_folder, chats_folder
from utils.patterns import messagePattern

# Pure functions with lambdas and partial
extractMessages         = lambda text, pattern: re.findall(pattern, text, re.DOTALL)
extractUserIndices      = lambda messages, user: [i for i, message in enumerate(messages) if user in message]
extractMessagesWithDate = lambda messages: [(datetime.strptime(date, "%d/%m/%Y %H:%M"), date + msg) for date, msg in messages]
filterMessagesContext   = lambda results, filteredIndices, context: set(
    msg for index in filteredIndices
    for start in [max(0, index - context)]
    for end in [min(len(results), index + context + 1)]
    for msg in results[start:end]
)
sortMessagesByDate = lambda messages: sorted(
    messages, key=lambda msg: datetime.strptime(msg[:16], "%d/%m/%Y %H:%M")
)

# Function to filter messages by minimum length
def filterMessagesByLength(messages, minLength):
    return [
        (date, msg) for date, msg in messages
        if len(msg) >= minLength
    ]

# Asynchronous functions
async def checkRepeatedMessage(message, cacheSet, outputFile):
    if message in cacheSet:
        return True
    async with aiofiles.open(outputFile, 'r', encoding='utf-8') as file:
        content = await file.read()
        cacheSet.update(content.splitlines())
        return message in cacheSet

async def processMessages(chat, pattern, user, context, minLength, outputFile, cacheSet):
    async with aiofiles.open(chat + '.txt', 'r', encoding='utf-8') as inputFile:
        text            = await inputFile.read()
        results         = extractMessagesWithDate(extractMessages(text, pattern))
        results         = filterMessagesByLength(results, minLength)
        filteredIndices = extractUserIndices([msg for _, msg in results], user)
        messagesToWrite = filterMessagesContext(results, filteredIndices, context)
        finalMessages   = [
            msg for _, msg in messagesToWrite 
            if not await checkRepeatedMessage(msg, cacheSet, outputFile)
        ]
        sortedMessages  = sortMessagesByDate(finalMessages)
        return sortedMessages

async def writeMessages(outputFile, messages):
    async with aiofiles.open(outputFile, 'a', encoding='utf-8') as file:
        for message in messages:
            await file.write(message + '\n')

async def processChat(chat, outputFile, pattern, user, context, minLength, cacheSet):
    try:
        sortedMessages = await processMessages(chat, pattern, user, context, minLength, outputFile, cacheSet)
        await writeMessages(outputFile, sortedMessages)
    except FileNotFoundError:
        print(f"File {chat}.txt not found.")
    except Exception as e:
        print(f"Error processing {chat}: {e}")

# Main function
async def select_messages_by_user(user, context, lowerLimit):
    outputFile = outputs_folder + user + '_chats.txt'
    cacheSet   = set()
    async with aiofiles.open(outputFile, 'w', encoding='utf-8') as file:
        await file.write('')
    tasks = [processChat((chats_folder + chat), outputFile, messagePattern, user, context, lowerLimit, cacheSet) for chat in chats]
    await asyncio.gather(*tasks)
