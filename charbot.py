#Charbot

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import platform
import json
import pickle
from random import randint
from random import choice
from collections import OrderedDict
import os

bot = commands.Bot(command_prefix = "~")
contingency_points = None
hardcore = True
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print('Logged in as ' + str(bot.user.name) + ' (ID:' + str(bot.user.id) + ') | Connected to ' + str(len(bot.guilds))+' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?bot_id={}&scope=bot&permissions=8'.format(bot.user.id))

'''
#How to create a new command
@bot.command(pass_context = True)
async def ping(ctx):
    await bot       (":ping_pong: ping!!")
'''

@bot.command()
async def hybrid(bot_, *args):
    global contingency_points
    global hardcore

    if len(args) != 7:
        await bot_.send("Invalid command! Usage: ~hybrid [hard|soft]core \_ \_ \_ \_ \_ \_ (each _ is a formula letter [a|b|c|d])")
        return

    hardcore = args[0]
    formulas = args[1:7]

    if hardcore[0].lower() == "h":
        contingency_points = 7
        #If too many contingency points are used, quit function
        if not await valid(bot_, contingency_points, formulas):
            return
        hardcore = True
        stats = OrderedDict({'Strength':0, 'Dexterity':0, 'Constitution':0, 'Intelligence':0,
            'Wisdom':0, 'Charisma':0})
        for stat, formula in zip(stats, formulas):
            stats[stat] = await roll(bot_, formula.upper())
        json.dump(stats, open("character.json", "w"), indent=4)
    else:
        contingency_points = 6
        #If too many contingency points are used, quit function
        if not await valid(bot_, contingency_points, formulas):
            return
        hardcore = False
        stats = [0, 0, 0, 0, 0, 0]
        for i in range(0, 6):
            stats[i] = await roll(bot_, formulas[i].upper())
        pickle.dump(stats, open("character.txt", "wb"))
        

    

    '''
    print("Point buy hybrid (hardcore):")
    print("3 points: A - 15 + 1/2d6 (rounded down)")
    print("2 points: B - 10 + 2d4")
    print("1 point: C - 6 + 2d6")
    #print("0 ponts- \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\D - 3d6")
    print("0 points: D - 3d6")
    '''

    results = await generateResults(bot_, stats)

    await bot_.send(embed=results)
    
    
    await bot_.send("{} contingency points remaining.".format(contingency_points))
    
    if contingency_points != 0:
        await bot_.send("To spend contingency points, use command \"~contingency # # # # # #\"")

async def roll(bot_, formula):
    global contingency_points
    if formula == 'A' and contingency_points >= 3:
        contingency_points -= 3
        return 15 + randint(1,6)//2
    elif formula == 'B' and contingency_points >= 2:
        contingency_points -= 2
        return 10 + randint(1,4) + randint(1,4)
    elif formula == 'C' and contingency_points >=1:
        contingency_points -= 1
        return 6 + randint(1,6) + randint(1,6)
    elif formula == 'D':
        return randint(1,6) + randint(1,6) + randint(1,6)
    else:
        return None

async def generateResults(bot_, stats):
    global hardcore
    results = "\n======RESULTS======\n"

    embed = discord.Embed(color=int(hex(randint(0, 0xFFFFFF)), 16))

    if hardcore:
        for key in stats:
            embed.add_field(name=key, value=stats[key], inline=False)
            results += "{}: {}\n".format(key, stats[key])
    else:
        for stat in stats:
            embed.add_field(name="-----", value=stat, inline=False)
            results += "{}\n".format(stat)

    return embed

async def valid(bot_, contingency_points, formulas):
    for formula in formulas:

        if formula.upper() == 'A':
            contingency_points -= 3
        elif formula.upper() == 'B':
            contingency_points -= 2
        elif formula.upper() == 'C':
            contingency_points -= 1
        elif formula.upper() == 'D':
            contingency_points -= 0
        else:
            await bot_.send("Invalid formula entry!")
            return False

    if contingency_points >= 0:
        return True
    else:
        await bot_.send("Not enough contingency points!")
        return False

@bot.command()
async def contingency(bot_, *args):
    global contingency_points
    global hardcore

    contingency_spend = list(map(int, args))

    if sum(contingency_spend) > contingency_points:
        await bot_.send("Not enough contingency points!")
        return

    if hardcore:
        stats = OrderedDict(json.load(open("character.json", "r")))

        for stat, spend in zip(stats, contingency_spend):
            while spend > 0:
                if 3 <= stats[stat] <= 7:
                    stats[stat] += 3
                elif 8 <= stats[stat] <= 14:
                    stats[stat] += 2
                elif 15 <= stats[stat] < 18:
                    stats[stat] += 1
                else:
                    await bot_.send("No effect. Choose another stat.")
                    contingency_points += 1

                spend -= 1
                contingency_points -= 1
    else:
        stats = pickle.load(open("character.txt", "rb"))
        for i in range(0,6):
            while contingency_spend[i] > 0:
                if 3 <= stats[i] <= 7:
                    stats[i] += 3
                elif 8 <= stats[i] <= 14:
                    stats[i] += 2
                elif 15 <= stats[i] < 18:
                    stats[i] += 1
                else:
                    await bot_.send("No effect. Choose another stat.")
                    contingency_points += 1

                contingency_spend[i] -= 1
                contingency_points -= 1    

    results = await generateResults(bot_, stats)
    await bot_.send(embed=results)
    await bot_.send("To add racial bonuses, use command \"~race # # # # # #\"")

    if hardcore:
        json.dump(stats, open("character.json", "w"), indent=4)
    else:
        pickle.dump(stats, open("character.txt", "wb"))

@bot.command()
async def race(bot_, *args):
    global hardcore
    
    if hardcore:
        stats = OrderedDict(json.load(open("character.json", "r")))
        for stat, increase in zip(stats, args):
            stats[stat] += int(increase)
    else:
        stats = pickle.load(open("character.txt", "rb"))
        for i in range(0,6):
            stats[i] += int(args[i])

    results = await generateResults(bot_, stats)
    await bot_.send(embed=results)

    if hardcore:
        json.dump(stats, open("character.json", "w"), indent=4)
    else:
        pickle.dump(stats, open("character.txt", "wb"))

@bot.command()
async def standard(bot_, *args):
    global hardcore
    hardcore = True

    stats = OrderedDict({'Strength':0, 'Dexterity':0, 'Constitution':0, 'Intelligence':0,
            'Wisdom':0, 'Charisma':0})
    
    for stat in stats:
        rolls = []
        for i in range(0, 4):
            rolls.append(randint(1,6))

        await bot_.send(stat + ": " + str(rolls) + " drop " + str(min(rolls)))
        
        rolls.remove(min(rolls))
        stats[stat] = sum(rolls)

    results = await generateResults(bot_, stats)
    await bot_.send(embed=results)


bot.run(TOKEN)
