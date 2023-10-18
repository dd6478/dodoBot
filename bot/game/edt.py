
import discord, requests, datetime, json
from discord import app_commands
from __main__ import tree


promos = ["E3a","E4a-A","E4a-B"]
color = {"COU":0xF09300, "TD":0x00ABC0, "TP":0x378D3B}
with open('asset/apiKey/eseoID.json', 'r') as file:
    ID = json.loads(file.read())

@tree.command(name="edt")
@app_commands.describe(arg = "Name of your promotion ==> E3a, E4a-A, E4a-B")
async def edt(interaction: discord.Interaction, arg: str):
    if (arg not in promos):
        await interaction.response.send_message("Mauvaise promo")
        return
    await interaction.response.send_message(f"Une bonne journée a l'eseo pour la {arg} : ")
    calendar = getCalendar(arg) #JSON
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

def getCalendar(promo):
    url = ID["URL"]
    day = getDay() #"20231021T210000"
    response = requests.get(f"https://reverse-proxy.eseo.fr/API-SP/API/agenda/user/{day[0]}/{day[1]}/{ID[promo]}")
    myResponse = json.loads(response.text)
    return myResponse

def getDay():
    day = str(datetime.datetime.today())
    day = day.split(" ")[0].replace("-", "")
    return(day+"T060000", day+"T210000")



