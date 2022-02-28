import time
import random as rand
from async_timeout import timeout
import discord
import asyncio
import re

from matplotlib.pyplot import text

async def send_text(bot, channel, my_text: str):
    ch_cmd = bot.get_channel(channel)
    await ch_cmd.send(my_text)
    return

async def dep_money(bot, channel_to_dep):
    try:
        ch_cmd = bot.get_channel(channel_to_dep)
        await ch_cmd.send("pls dep all")
        await asyncio.sleep(rand.randint(3,5))
        await ch_cmd.send("pls with 2k")
        await asyncio.sleep(rand.randint(3,5))
        
    except discord.errors.InvalidData:
        print('problems found')
        return
    
async def wait_for_msg(bot, ch, check_func = None, timeout=20):
    if check_func is None:
        check_func = lambda m: m.author.id == bot.dank_memer_id and m.channel == ch
    try:
        return await bot.wait_for('message', check = check_func, timeout=timeout)
    except asyncio.TimeoutError:
        print("wait for msg timed out")
        return None
# Use alcohol

# buy lifesaver
# 1. Check how many life we got
# 2. Check how many balance we got.
# 3. Buy life saver Based on balance

async def check_use_cases(bot, ch, msg):
    ch_cmd = bot.get_channel(ch)
    if msg.content.startswith(">use alc"):
        await ch_cmd.send("pls use alc")

async def check_buy_cases(bot, ch, msg):
    ch_cmd = bot.get_channel(ch)
    if msg.content.startswith(">buy life"):
        await ch_cmd.send("pls with all")
        await asyncio.sleep(rand.randint(2,3))
        await ch_cmd.send("pls buy life max")
    elif msg.content.startswith(">buy alc"):
        await ch_cmd.send("pls with all")
        await asyncio.sleep(rand.randint(2,4))
        await ch_cmd.send("pls buy alc max")

"""<@443143329191034890> **__memePhone__** -- What do you want to do?"""
async def use_phone(bot, ch):
    try:
        ch_cmd = bot.get_channel(ch)
        await ch_cmd.send("pls use phone")
        msg = await wait_for_msg(
            bot,
            ch_cmd,
            check_func = lambda m:
                m.author.id == bot.dank_memer_id and m.channel == ch_cmd 
                and (str(m.content).startswith(f"<@{bot.user.id}>") or str(m.content).lower().startswith("you don't"))
            )
        await asyncio.sleep(rand.uniform(0.2,1.0))
        
        if len(msg.embeds) > 0 and str(msg.embeds[0].title).lower().startswith("woah slow"):
            await ch_cmd.send("pls settings passive true")
            await asyncio.sleep(rand.uniform(0.2,1.0))
            return await use_phone(bot, ch)
        some_dict = {0:"fok me", 1: "Not like this", 2: "mtherfker lemme buy my phone"}
        if msg is not None and str(msg.content).lower().startswith("you don't own"):
            await ch_cmd.send("pls with 10k")
            await wait_for_msg(bot, ch_cmd)
            await ch_cmd.send(some_dict[rand.randint(0,2)])
            await asyncio.sleep(60)
            await ch_cmd.send("pls with 10k")
            await wait_for_msg(bot, ch_cmd)
            await asyncio.sleep(rand.uniform(0.2,1.0))
            await ch_cmd.send("pls buy phone")
            await wait_for_msg(bot, ch_cmd)
            await asyncio.sleep(rand.uniform(0.2,1.0))
            return await use_phone(bot, ch)
        else:
            await ch_cmd.send("p")
            await bot.wait_for('message', check = lambda m: m.author.id == bot.dank_memer_id and m.channel == ch_cmd,timeout=20)
        return True
    except discord.errors.Forbidden:
        return False



def check_description(m):
    #m.components[0].children[1].click()
    return m.channel == 935840270157754370 and m.author.id == 270904126974590976
   
       

async def check_life(bot, ch):
    try:
        ch_cmd = bot.get_channel(ch)
        await ch_cmd.send("pls item life")
        
    except discord.errors.InvalidData:
        print('problems found while checking life')
        return

async def check_check_cases(bot, ch, msg):
    ch_cmd = bot.get_channel(ch)
    if msg.content.startswith(">check life"):
        await ch_cmd.send("pls item life")
    elif msg.content.startswith(">check alc"):
        await ch_cmd.send("pls item alc")
        
async def get_channel_link(bot, ch_link, ch):
    ch_cmd = bot.get_channel(ch)
    await ch_cmd.send(ch_link)
    
async def with_dep_msg(bot, ch, message, n=0):
    if n>=4:
        print(n)
        return
    ch_cmd = bot.get_channel(ch)
    await ch_cmd.send(message)
    msg = await wait_for_msg(bot, ch_cmd, timeout=2.0)
    if msg is not None:
        if len(msg.embeds)>0:
            embed = msg.embeds[0]
            if embed.description:
                string = re.sub(r'[^a-zA-Z.\d\s]', '', str(embed.description))
                text_lst = string.split(" ")
                index = text_lst.index("in")
                await asyncio.sleep(float(text_lst[index + 2]))
                return await with_dep_msg(bot, ch, message, n+1)
            else:
                return None
        else: return None
    else: return await with_dep_msg(bot, ch, message, n+1)


def in_dms(message):
    return not message.guild

async def pls_rob(bot, ch_cmd, alt_id):
    await ch_cmd.send(f"pls rob {alt_id}")
    heist_msg = await wait_for_msg(bot, ch_cmd, timeout=2)
    if heist_msg is not None:
        if str(heist_msg.content).lower().startswith("lol"):
            return await pls_rob(bot, ch_cmd, alt_id)
        else:
            return heist_msg


async def rob_my_alt(bot, ch, alt_aut, n=0):
    sleep_time = 31
    if n >= 5:
        return
    ch_cmd = bot.get_channel(ch)
    await ch_cmd.send("pls with 100k")
    await wait_for_msg(bot, ch_cmd, timeout=5)
    await ch_cmd.send(">withdraw")
    await wait_for_msg(bot, ch_cmd, check_func=lambda m: m.author == alt_aut and m.channel == ch_cmd and m.content.startswith(">steal me"), timeout=50)
    await asyncio.sleep(0.5)
    heist_msg = await pls_rob(bot, ch_cmd, alt_aut)
    await ch_cmd.send(">deposit")
    await ch_cmd.send("pls dep all")
    if heist_msg is not None and str(heist_msg.content).lower().startswith("you stole"):
        await ch_cmd.send(">toggle heist")
        return
    else:
        await asyncio.sleep(sleep_time)
        await rob_my_alt(bot, ch, alt_aut, n+1)
    