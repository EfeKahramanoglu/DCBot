import asyncio
import discord
import os
import random
from discord.ext import commands
import requests

token = os.environ["TOKEN"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# ================= READY =================

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

# ================= HOŞGELDİN =================

@bot.event
async def on_member_join(member):
    try:
        await member.send(f"Sunucuya hoşgeldin {member.name} 🎉")
    except:
        pass

# ================= KICK =================

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member} atıldı 👢")
    except:
        await ctx.send("Atmaya yetkiniz yok ❌")

# ================= BAN =================

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member} banlandı 🔨")
    except:
        await ctx.send("Banlamaya yetkiniz yok ❌")

# ================= UNBAN =================

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send("Ban kaldırıldı 🔓")
    except:
        await ctx.send("Ban kaldırmaya yetkiniz yok ❌")

# ================= MUTE =================

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, süre: int):
    try:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)

        await member.add_roles(muted_role)
        await ctx.send(f"{member.mention} {süre} saniyeliğine susturuldu 🔇")

        await asyncio.sleep(süre)

        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"{member.mention} artık konuşabilir 🔊")

    except:
        await ctx.send("Mute işlemi yapılamadı ❌")

# ================= JAIL =================

@bot.command()
@commands.has_permissions(administrator=True)
async def jail(ctx, member: discord.Member):
    try:
        jail_role = discord.utils.get(ctx.guild.roles, name="Jail")

        if not jail_role:
            jail_role = await ctx.guild.create_role(name="Jail")

            for channel in ctx.guild.channels:
                await channel.set_permissions(
                    jail_role,
                    send_messages=False,
                    view_channel=False,
                    speak=False
                )

            ceza = discord.utils.get(ctx.guild.channels, name="ceza-kanali")
            if ceza:
                await ceza.set_permissions(
                    jail_role,
                    send_messages=True,
                    view_channel=True
                )

        await member.add_roles(jail_role)
        await ctx.send(f"{member.mention} hapse atıldı 🔒")

    except:
        await ctx.send("Jail işlemi yapılamadı ❌")

@bot.command()
@commands.has_permissions(administrator=True)
async def unjail(ctx, member: discord.Member):
    try:
        jail_role = discord.utils.get(ctx.guild.roles, name="Jail")
        if jail_role:
            await member.remove_roles(jail_role)
            await ctx.send(f"{member.mention} hapisten çıkarıldı 🔓")
    except:
        await ctx.send("Unjail yapılamadı ❌")

# ================= CLEAR =================

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"{amount} mesaj silindi 🧹")
        await msg.delete(delay=3)
    except:
        await ctx.send("Mesaj silmeye yetkiniz yok ❌")

# ================= DUCK =================

def get_duck():
    try:
        res = requests.get("https://random-d.uk/api/random", timeout=5)
        return res.json()['url']
    except:
        return None

@bot.command()
async def duck(ctx):
    try:
        url = get_duck()
        if url:
            await ctx.send(url)
        else:
            await ctx.send("Ördek bulunamadı 🦆")
    except:
        await ctx.send("Bir hata oluştu ❌")

# ================= MESAJ SİSTEMİ =================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    try:
        if message.content.lower() in ["sa", "selam", "s.a", "slm"]:
            await message.channel.send("Aleyküm selam 😎")

        if "bot" in message.content.lower():
            await message.channel.send("Buyrun? 👀")

        if message.guild:  # DM hatası engeli
            jail_role = discord.utils.get(message.guild.roles, name="Jail")

            if jail_role and jail_role in message.author.roles:
                if message.channel.name == "ceza-kanali":
                    if message.content.lower() == "özürdilerim":
                        await message.author.remove_roles(jail_role)
                        await message.channel.send("Özgür bırakıldın 🔓")

    except:
        pass

    await bot.process_commands(message)

# ================= RUN =================

bot.run(token)
