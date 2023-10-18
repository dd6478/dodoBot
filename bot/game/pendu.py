
import discord, random
from discord import app_commands
from __main__ import tree, dodoBot

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def getWord():
    with open('asset/data/wordList', 'r') as file:
        word=file.readlines()
        file.close()
    return word[random.randint(0,len(word)-1)].strip()

def printWord(word, letter):
        str=''
        for i in word:
            if i in letter:
                str+=i+' '
            else:
                str+='- '
        if str=='**':
            str=''
        return str

def printBadLetters(badLetters):
    str='*'
    for i in badLetters:
        str+=i+' '
    str+='*'
    return str

#@tree.command(name="pendu")
async def pendu(interaction: discord.Interaction):
    def check(m):
        return m.channel == interaction.channel and len(m.content) == 1 and m.content in alphabet

    word = getWord()
    life = 10
    letters = []
    badLetters = []
    await interaction.response.send_message(f':warning: {interaction.user.mention} a lancé une partie de pendu :warning:')
    await interaction.channel.send(f'''
        Le mot à trouver est : {printWord(word, letters)}, vous avez {life} vie bon courage :wink:
Entrez une lettre :''')
    while life > 0: 
        if '-' not in printWord(word, letters):
            await interaction.channel.send(f'Vous avez gagné :tada: le mot était bien **"{word}"**')
            return
        try:
            msg = await dodoBot.wait_for('message', check=check, timeout=60)
        except:
            await interaction.channel.send('Personne ne joue avec moi :sob:')
            return
        if msg.content.lower() in letters or msg.content.lower() in badLetters:
            await interaction.channel.send(f'{msg.author.mention} :rage: **"{msg.content}"** a deja été dit !')
        elif msg.content.lower() in word:
            letters.append(msg.content.lower())
            await interaction.channel.send(f'{msg.author.mention} bravo **"{msg.content}"** est dans le mot :white_check_mark:\nIl vous reste {life} vie\nLe mot : {printWord(word, letters)} | les mauvaise lettres : {printBadLetters(badLetters)}')
        elif msg.content.lower() not in word:
            badLetters.append(msg.content.lower())
            life-=1
            await interaction.channel.send(f'{msg.author.mention} **"{msg.content}"** n\'est pas dans le mot :x:\nIl vous reste {life} vie\nLe mot : {printWord(word, letters)} | les mauvaise lettres : {printBadLetters(badLetters)}')
    await interaction.channel.send(f'Vous avez perdu :cry: le mot était **"{word}"**')
