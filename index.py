import discord
import datetime
import youtube_dl
import os

client = discord.Client()


@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game("test bot")
    await client.change_presence(status=discord.Status.online, activity=game)




@client.event
async def on_message(message):
    if message.content.startswith("hi"):
        await message.channel.send("hello")

@client.event
async def on_message(message):
    if message.content.startswith("내정보"):
        date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name="이름", value=message.author.name, inline=True)
        embed.add_field(name="서버 별명", value=message.author.display_name, inline=True)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=True)
        embed.add_field(name="아이디", value=message.author.id, inline=True)
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(message.channel, embed=embed)

@client.event
async def on_message(message):
    if message.content.startswith("connect"):
        await message.author.voice.channel.connect()
        await message.channel.send("보이스 채널에 입장합니다.")

    if message.content.startswith("play"):
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc

            url = message.content.split(" ")[1]
            option = {
                'outtmpl' : "file/" + url.split('=')[1] + ".mp3"
            }

            with youtube_dl.YoutubeDL(option) as ydl:
                ydl.download(url)
                info = ydl.extract_info(url, download=False)
                title = info["title"]

            voice.play(discord.FFmpegAudio("file/" + url.split('=')[1] + ".mp3"))
            await message.channel.send(title + "을 재생합니다.")

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
