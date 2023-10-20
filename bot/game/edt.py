
import discord, requests, datetime, json, locale, calendar
from discord import app_commands
from __main__ import tree

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
promos = ["E3a","E4a-A","E4a-B"]
color = {"COU":0xF09300, "TD":0x00ABC0, "TP":0x378D3B}
with open('asset/apiKey/eseoID.json', 'r') as file:
    ID = json.loads(file.read())
    file.close()
with open('asset/apiKey/admin.json', 'r') as file:
    admin = json.loads(file.read())
    file.close()

def get_day_difference(target_day):
    days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    today = datetime.datetime.now().weekday()  # 0 = lundi, 1 = mardi, ..., 6 = dimanche
    target_day_index = days.index(target_day.lower())

    # Calculer la différence entre aujourd'hui et le jour cible
    difference = target_day_index - today

    # Ajuster la différence si le jour cible est dans la semaine précédente
    if difference > 3:
        difference -= 7
    elif difference < -3:
        difference += 7

    return difference


@tree.command(name="edt")
@app_commands.describe(name = "Name of your promotion")
@app_commands.choices(name=[
    app_commands.Choice(name="E3a", value="E3a"),
    app_commands.Choice(name="E4a-A", value="E4a-A"),
    app_commands.Choice(name="E4a-B", value="E4a-B")
])
@app_commands.describe(jour = "day of the week")
@app_commands.choices(jour=[
    app_commands.Choice(name="lundi", value="lundi"),
    app_commands.Choice(name="mardi", value="mardi"),
    app_commands.Choice(name="mercredi", value="mercredi"),
    app_commands.Choice(name="jeudi", value="jeudi"),
    app_commands.Choice(name="vendredi", value="vendredi"),
    app_commands.Choice(name="samedi", value="samedi"),
    app_commands.Choice(name="dimanche", value="dimanche"),
    app_commands.Choice(name="none", value="none")
])
async def edt(interaction: discord.Interaction, name: str, jour: str = "none"):
    if jour == "none":
        jour = datetime.datetime.now().strftime('%A')
    difference = get_day_difference(jour)

    if (interaction.user.id == admin["ID"]):
        await interaction.response.send_message(f"Une bonne journée a l'eseo pour la {name} pour {jour}:")
    elif (name not in promos):
        await interaction.response.send_message("Mauvaise promo")
        return
    else:
        await interaction.response.send_message(f"Une bonne journée a l'eseo pour la {name} pour {jour}: ")
    calendar = getCalendar(name, jour) #JSON
    if (calendar == []):
        embed = discord.Embed(title="Pas de cours", description=":tada::tada::tada:", color=0x0000FF)
        await interaction.channel.send(embed=embed) 
        return
    for classs in calendar:
        embed = discord.Embed(title=classs["Libelle"].split("-")[0], description=classs["Emplacement"], color=color[classs["Code"]])
        embed.add_field(name="Prof", value=classs["Professeur"], inline=True)
        start=[int(classs["Debut"].split("T")[1].split(":")[0]),int(classs["Debut"].split("T")[1].split(":")[1])]
        end=[int(classs["Fin"].split("T")[1].split(":")[0]),int(classs["Fin"].split("T")[1].split(":")[1])]
        embed.add_field(name="Début/Fin", value=f'{start[0]}h{start[1]}-{end[0]}h{end[1]}', inline=True)
        duree=[int((end[0]*60+end[1]-(start[0]*60+start[1]))/60)]
        duree.append(int(((end[0]*60+end[1]-(start[0]*60+start[1]))/60-duree[0])*60))
        embed.add_field(name="durée", value=f"{duree[0]}h{duree[1]}", inline=True)
        await interaction.channel.send(embed=embed) 
    return

def getCalendar(promo, jour):
    url = ID["URL"]
    day = getDay(jour) #"20231021T210000"
    response = requests.get(f"https://reverse-proxy.eseo.fr/API-SP/API/agenda/user/{day[0]}/{day[1]}/{ID[promo]}")
    myResponse = json.loads(response.text)
    return myResponse

def getDay(jour):
    diff = get_day_difference(jour)
    today = datetime.datetime.now()
    if today.day + diff < 0:
        today = datetime.datetime(today.year, today.month - 1, today.day + diff)
    elif today.day + diff > calendar.monthrange(today.year, today.month)[1]:
        today = datetime.datetime(today.year, today.month + 1, today.day + diff)
    else:
        today = datetime.datetime(today.year, today.month, today.day + diff)
    today = today.strftime('%Y%m%d')
    return(today+"T060000", today+"T210000")



