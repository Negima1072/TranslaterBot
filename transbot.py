import discord, requests, os, random

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') #DiscordBotAccessToken
TRANSAPI_URL = os.environ.get('TRANSAPI_URL') #GoogleTransApiUrl

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)

helpmes = """**-t [lang] [text]**
lang... ja en zh-CN
lang... Japanese Chinese
lang... :flag_jp: :flag_us: :flag_cn: (only)
**-t help**
Send help message
**-t author**
Send author information
"""

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Translater | -t help'))
    print("On Login")

@client.event
async def on_message(mes):
    if mes.author.bot:
        return
    if "-t" in mes.content:
        try:
            t1 = mes.content.find("-t")+mes.content.find(" ")+1
            param = mes.content[t1:mes.content.find(" ", t1) if " " in mes.content[t1:] else len(mes.content)]
            text = mes.content[mes.content.find(param,t1)+len(param)+1:]
            if param == "help":
                embed = discord.Embed(title="**Howto/使い方/使用规则**", description=helpmes)
                member = mes.guild.get_member(int(mes.author.id))
                embed.set_footer(text="Requeted by "+member.display_name)
                await mes.channel.send(embed=embed)
                return
            if param == "author":
                embed = discord.Embed(description="**Made by Negima1072**\n[Twitter](https://twitter.com/Negima1072)")
                await mes.channel.send(embed=embed)
                return
            if param == "" or text == "":
                return
            target = param[0:2].lower() if param[0].isupper() else (["cn","us","jp"][["🇨🇳","🇺🇸","🇯🇵"].index(param)] if param in ["🇨🇳","🇺🇸","🇯🇵"] else param)
            if target == "ch" or target == "cn": target = "zh-CN"
            if target == "jp": target = "ja"
            if target == "us": target = "en"
            res = requests.get(TRANSAPI_URL+"?target="+target+"&text="+text)
            trans = res.json()
            if trans["code"] == 400:
                errorno = random.randint(100000,999999)
                print("["+str(errorno)+"]"+str(trans["text"]))
                await mes.channel.send("Something occurred error. **["+str(errorno)+"]**")
                return
            if trans["code"] == 200:
                ntext = trans["text"]
                member = mes.guild.get_member(int(mes.author.id))
                embed = discord.Embed(description=ntext, color=member.top_role.color.value)
                embed.set_author(name=mes.author.display_name, icon_url=mes.author.avatar_url)
                await mes.channel.send(embed=embed)
                return
        except Exception as e:
            errorno = random.randint(10000,99999)
            print("["+str(errorno)+"]"+str(e))
            await mes.channel.send("Something occurred error. **["+str(errorno)+"]**")
            return

@client.event
async def on_raw_reaction_add(p):
    if str(p.emoji) not in ["🇨🇳","🇺🇸","🇯🇵"]:
        return
    ch = client.get_channel(p.channel_id)
    try:
        mes = await ch.fetch_message(p.message_id)
        if [r.count for r in mes.reactions if str(r) == str(p.emoji)][0] != 1:
            return
        text = mes.content
        target = ["zh-CN","en","ja"][["🇨🇳","🇺🇸","🇯🇵"].index(str(p.emoji))]
        res = requests.get(TRANSAPI_URL+"?target="+target+"&text="+text)
        trans = res.json()
        if trans["code"] == 400:
            errorno = random.randint(100000,999999)
            print("[R"+str(errorno)+"]"+str(trans["text"]))
            await ch.send("Something occurred error. **[R"+str(errorno)+"]**")
            return
        if trans["code"] == 200:
            ntext = trans["text"]
            member = mes.guild.get_member(int(mes.author.id))
            embed = discord.Embed(description=ntext, color=member.top_role.color.value)
            embed.set_author(name=mes.author.display_name, icon_url=mes.author.avatar_url)
            embed.set_footer(text="Requeted by "+p.member.display_name)
            await ch.send(embed=embed)
            return
    except Exception as e:
        errorno = random.randint(10000,99999)
        print("[R"+str(errorno)+"]"+str(e))
        await ch.send("Something occurred error. **[R"+str(errorno)+"]**")
        return

client.run(ACCESS_TOKEN)