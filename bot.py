import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.messages = True  # Mesajları dinlemek için bu intent'i ekleyin

bot = commands.Bot(command_prefix='!', intents=intents)

# Kullanıcıların giriş/çıkış bilgilerini saklamak için bir sözlük
entry_exit_log = {}

# Sürekli girip çıkan kullanıcıların banlanması için sınır ve süre
ENTRY_EXIT_LIMIT = 3
BAN_DURATION = 1440 # dakika

# Kullanıcı giriş yaptığında tetiklenen olay
@bot.event
async def on_member_join(member):
    now = datetime.now()
    user_id = member.id

    if user_id not in entry_exit_log:
        entry_exit_log[user_id] = []

    entry_exit_log[user_id].append(now)

    # Kullanıcının giriş çıkışlarını kontrol et
    check_entry_exit(member)

# Kullanıcı çıkış yaptığında tetiklenen olay
@bot.event
async def on_member_remove(member):
    now = datetime.now()
    user_id = member.id

    if user_id not in entry_exit_log:
        entry_exit_log[user_id] = []

    entry_exit_log[user_id].append(now)

# Giriş çıkışları kontrol eden fonksiyon
def check_entry_exit(member):
    now = datetime.now()
    user_id = member.id
    logs = entry_exit_log[user_id]

    # Sadece son 10 dakika içindeki giriş çıkışları say
    recent_logs = [log for log in logs if now - log <= timedelta(minutes=10)]
    entry_exit_log[user_id] = recent_logs

    if len(recent_logs) >= ENTRY_EXIT_LIMIT:
        asyncio.create_task(temp_ban(member))

# Kullanıcıyı süreli banlayan fonksiyon
async def temp_ban(member):
    try:
        await member.ban(reason="Sürekli giriş çıkış yaptığı için süreli banlandı.")
        await asyncio.sleep(BAN_DURATION * 60)
        await member.unban(reason="Süreli ban kaldırıldı.")
    except discord.errors.NotFound:
        # Kullanıcı sunucuda değilse hata verir
        pass

# Bot hazır olduğunda tetiklenen olay
@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} olarak giriş yaptı!')

# !selam komutu
@bot.command()
async def selam(ctx):
    await ctx.send('Selam!')

# Mesajları dinlemek ve loglamak için on_message olayını ekleyin
@bot.event
async def on_message(message):
    print(f'Mesaj alındı: {message.content}')
    await bot.process_commands(message)

# Bot token'inizi burada girin
bot.run('MTI1MjI3MTIyNTI1ODkwMTYyNg.GlOY86.ET675A2FMY34ew30zoHfMtprW016RBncWsyp2w')
