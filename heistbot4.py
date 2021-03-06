import argparse
import asyncio
import datetime
import json
import random as rand
import re
import time
import discord
import yaml
import discord.ext.commands as commands
from library import *

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('get_config', type=str,
                    help='A filename')
args = parser.parse_args()
get_str = args.get_config

with open("config/"+get_str+".yaml") as file:
    variabless = yaml.load(file, Loader=yaml.FullLoader)

TOKEN, CH_DEP , MAIN_CH_DEP, LOG_CH = variabless['token'], variabless['channel_to_dep'] , variabless['main_account_channel'], variabless['log_channel']
DANKMEMER_ID , NO_HEIST_SERVERS= 270904126974590976 , [682809584985178135, 935840269692194817]
HEISTLABEL, CONFIRMLABEL , BEING_HEISTED= "JOIN HEIST", "Confirm", "Your bank is being heisted!"

# --- Constants --- #
class DiscordBot(commands.Bot):
    def __init__(self, ch_cmd:int) -> None:
        super().__init__(command_prefix="")
        self.ch_cmd = ch_cmd
        self.unheisted = True
        self.dank_memer_id = DANKMEMER_ID
        self.robbing = False
        # Self.robbing parameter is used to prevent joining heist when self.robbing
        return


    # --- Self-Made --- #
    # --- Commands --- #
    async def toggle_heist(self, input_value = None) -> None:
        if self.robbing: 
            return
        if input_value is not None:
            self.unheisted = input_value
        else:
            self.unheisted = not self.unheisted
        ready = "ready" if self.unheisted else "not ready"
        await send_text(self,self.ch_cmd,f"Heist is {ready}.")
        return

    async def rob_myself(self)-> None:
        dep_msg = await with_dep_msg(self, CH_DEP, "pls dep all")
        if CH_DEP == MAIN_CH_DEP:
            # Return if this is main account.
            return None
        else:
            if dep_msg is not None :
                if len(dep_msg.embeds) > 0:
                    if len(dep_msg.embeds[0].fields) > 0:
                        embed = dep_msg.embeds[0].to_dict()
                        bank_amount = re.sub(r'\W+','', embed['fields'][2]['value'])
                        if int(bank_amount) >= int(5e6):
                            print(f"rob myself initiated with bank [{bank_amount}]")
                            await send_text(self, LOG_CH, f"Gained 5MIL from {self.user}")
                            await self.toggle_heist(input_value =False)
                            self.robbing = True
                            await send_text(self, CH_DEP, f"self robbing is now {self.robbing}")
                            # Sleep for 5 seconds and begin operation
                            await asyncio.sleep(5.0)
                            await send_text(self, MAIN_CH_DEP, f">mina_rob {CH_DEP}")
                        else: await send_text(self, CH_DEP, f"not robbing self, bank amount {bank_amount} < {int(5e6)}")
            else:
                await with_dep_msg(self, CH_DEP, "pls with 2k")
                return await self.rob_myself()

    async def heist(self, 
                    compo_index:discord.components.Button, 
                    message:discord.Message, 
                    n:int = 0 
                    ) -> bool:
        if n < 59:
            try:
                await compo_index.click()
                try:
                    dank_msg= await self.wait_for('message', check= lambda m: m.author.id == DANKMEMER_ID and m.channel == message.channel, timeout=2.5)
                except (asyncio.TimeoutError,asyncio.CancelledError) as error:
                    print('error',error, n)
                    return await self.heist(compo_index, message, n+1)
                
                if len(dank_msg.embeds) > 0: 
                    print(f"Tried clicking [n={n}], embed")
                    await asyncio.sleep(1.0)
                    return await self.heist(compo_index, message, n+1)
                content = str(dank_msg.content).lower()
                if content.startswith("you successfully") or "joined" in content:
                    print(dank_msg.content)
                    return True
                if content.startswith("this bankrob already failed"):
                    print("this bankrob already failed")
                    return False
                if content.startswith("the police are"):
                    print(f"Tried clicking [n={n}]")
                    await asyncio.sleep(1.0)
                    return await self.heist(compo_index, message, n+1)
                if content.startswith("you need at"):
                    await send_text(self, CH_DEP, "pls with 2k")
                    await asyncio.sleep(0.8)
                    return await self.heist(compo_index, message, n+1)
                else:
                    print(content)
                    return False
            except (discord.errors.Forbidden, discord.errors.HTTPException) as error:
                await get_channel_link(self, message.channel.mention, CH_DEP)
                return False
        else:
            return False


    # --- Discord ---#
    # --- Events --- #
    async def on_ready(self) -> None:
        print(f"Bot {self.user} is connected to server. at [{datetime.datetime.now().strftime('%H:%M')}]")
        return
    
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            if message.channel.id == CH_DEP:
                if message.content.startswith(">toggle heist"):
                    await self.toggle_heist()
                if message.content.startswith(">rob"):
                    await self.rob_myself()
            return

        if not in_dms(message):
            # if it is not in dank memer community server
            if message.guild.id == NO_HEIST_SERVERS[0]: 
                return
        
        if message.author.id == DANKMEMER_ID:

            ## RECEIVED MONEY FROM HEIST
            if message.content.startswith("Amazing job everybody"):
                await self.rob_myself()
            
            
            embeds = message.embeds
            compos = message.components
            if in_dms(message):
                if len(embeds) != 0:
                    embed_desc = str(embeds[0].description)
                    embed_title = str(embeds[0].title)
                    
                    ## GETTING HEISTED
                    if embed_title == BEING_HEISTED:
                        print("\nYou're being heisted right now")
                        text = embed_desc.split("channels/")[1]
                        
                        # Search Using reges
                        channel_search = re.search('/(.+?)/', text)
                        name_search = re.search(r'[\w]+#+\d{1,9}', embed_desc)
                        channel_to_phone = int(channel_search.group(1)) if channel_search is not None else CH_DEP
                        user_that_heist_me = name_search.group(0) if name_search is not None else "None"
                        slap_spank_dict = {0: "nice", 1: "sweet", 2: "ez", 3: "what chu want", 4: " Thank you for your patrionage", 5:":eyes:", 6:"pls use chill"}
                        # We Block all threads and wait.
                        await asyncio.sleep(rand.randint(10,40))
                        if await use_phone(self, channel_to_phone):
                            print(f"You used your phone when being heisted by {user_that_heist_me}\n at Time: [{datetime.datetime.now().strftime('%H:%M')}]\n")
                            await with_dep_msg(self,channel_to_phone,"pls dep all")
                            await asyncio.sleep(rand.uniform(0.6, 2.0))
                            if rand.randint(0,1): await send_text(self, channel_to_phone, f"{slap_spank_dict[rand.randint(0,6)]}")
                        else:
                            print("Failed to use phone, trying again in custom server")
                            await use_phone(self, CH_DEP)
                            await with_dep_msg(self,CH_DEP, "pls dep all")
                    
                    if embed_title.lower().startswith("you have been given"):
                        await send_text(self, CH_DEP, "pls dep all")
            ## HEISTING OPERATION
            # Not in dms
            elif len(compos)>0:
                try:
                    if not any(hasattr(compo, 'label') for compo in compos[0].children):
                        return
                    labels = [compo.label for compo in compos[0].children]
                    
                    if message.channel.id == CH_DEP:
                        if CONFIRMLABEL in labels:
                            index = labels.index(CONFIRMLABEL)
                            await message.components[0].children[index].click()
                    else:
                        if self.unheisted and message.guild.id not in NO_HEIST_SERVERS:
                            if HEISTLABEL in labels:
                                # Find index
                                index = labels.index(HEISTLABEL)
                                await dep_money(self, CH_DEP)
                                print("Heist Found")
                                if await self.heist(message.components[0].children[index], message):
                                    print(f"{self.user} clicked on label - {HEISTLABEL}, \nJOINED HEIST at [{datetime.datetime.now().strftime('%H:%M')}]")
                                    
                                    # Toggle heist only if heist is activated
                                    await self.toggle_heist(False)
                                    await asyncio.sleep(300)
                                    
                                    # Toggle Heist only if heist is not active 
                                    await self.toggle_heist(True)
                                else:
                                    print(f"Failed to join the heist at [{datetime.datetime.now().strftime('%H:%M')}]")
                        else:
                            return
                except discord.errors.InvalidData: return
            else: return

        elif message.channel.id == CH_DEP:
            if message.content is not None:
                if message.content.startswith(">use"):
                    await check_use_cases(self, CH_DEP, message)
                if message.content.startswith(">buy"):
                    await check_buy_cases(self, CH_DEP, message)
                if message.content.startswith(">check"):
                    await check_check_cases(self, CH_DEP, message)
                if message.content.startswith(">selfrob false"):
                    self.robbing = False
                    await send_text(self, CH_DEP, f"Self robbing is now {self.robbing}")
                if message.content.startswith(">toggle heist"):
                    lst_content = message.content.split(" ")
                    if len(lst_content) > 2:
                        t_or_false = lst_content[2].lower() in ("yes", "true", "t", "1")
                        await self.toggle_heist(t_or_false)
                    else:
                        await self.toggle_heist()
                if message.content.startswith(">deposit"):
                    await with_dep_msg(self, CH_DEP, "pls dep all")
                if message.content.startswith(">withdraw"):
                    await with_dep_msg(self, CH_DEP, "pls with all")
                    await with_dep_msg(self, CH_DEP, "pls dep 50k")
                    await send_text(self, CH_DEP, ">steal me")
                
                # We're always going to be BananaJuic3, when this command is sent.
                if message.content.startswith(">mina_rob"):
                    print("robbing")
                    await self.toggle_heist(False)
                    self.robbing = True
                    rob_channel = int(str(message.content).split(" ")[1])
                    await rob_my_alt(self, rob_channel, alt_aut = message.author)
                    self.robbing = False
                    await self.toggle_heist(True)
                    
        else:
            return


if __name__ == '__main__':
    bot = DiscordBot(ch_cmd=CH_DEP)
    bot.run(TOKEN)
