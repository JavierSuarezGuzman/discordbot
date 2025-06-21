import os
import discord
import asyncio

from discord import FFmpegPCMAudio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="b!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    default_channel = discord.utils.get(bot.get_all_channels(), type=discord.ChannelType.text)
    if default_channel:
        await default_channel.send("Preparaos, listos... y fuera! Usa b!play una url que termine en .mp3 para reproducirlo!!")

@bot.command()
async def play(ctx, *, input_text: str):
    if not ctx.author.voice:
        await ctx.send("🤡 🤡 Debeis estar en un canal de voz 🤡 🤡")
        return
    if ".mp3" not in input_text:
        await ctx.send("No seais payaso, sabeis que debeis ingresar una URL que termine en .mp3")
        return
    
    try:
        voice_client = ctx.voice_client
        if not voice_client:
            voice_client = await ctx.author.voice.channel.connect()
        elif voice_client.channel != ctx.author.voice.channel:
            await voice_client.move_to(ctx.author.voice.channel)

        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(FFmpegPCMAudio(input_text))

        while voice_client.is_playing():
            await asyncio.sleep(1)

        await voice_client.disconnect()
        
    except Exception as e:
        print(f"Se produjo un error: {e}")
        
@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_connected():
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        #await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Detenida.")
    else:
        await ctx.send("❌ No estoy conectado a ningún canal de voz.")


bot.run(TOKEN)
