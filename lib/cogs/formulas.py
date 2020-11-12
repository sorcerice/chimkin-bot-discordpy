from typing import Optional
import os

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command

from aiohttp import request
from libneko import pag

supportedUnits = '\n1)celcius-fahrenheit\n2)fahrenheit-celcius'

# with open("./lib/bot/currencyconvertapikey.0", "r", encoding="utf-8") as f:
# 	APIKEY = f.read()
APIKEY = os.getenv('CCONV_APIKEY')


class Formulas(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='unitconvert',
             aliases=['uconvert'],
             description=f'Converts units, currently supports:{supportedUnits}',
             brief=f'Converts units, currently supports:{supportedUnits}',
             help=f'Converts units, currently supports:{supportedUnits}')
    async def convert_units(self, ctx, value: float, fromUnit: str, to: Optional[str], toUnit: str):
        def EmbedBuilder(fromUnit: str, toUnit: str, value, formula):
            embed = Embed(title='Chimkin Converter',
                          description=f'{value} {fromUnit} to {toUnit} = {formula}',
                          colour=ctx.author.colour)
            return embed

        if fromUnit == 'C' and toUnit == 'F':
            formula = f'{((value * 9/5) + 32):.2f}°F'
            await ctx.send(embed=EmbedBuilder(fromUnit=fromUnit, toUnit=toUnit, value=value, formula=formula))

        elif fromUnit == 'F' and toUnit == 'C':
            formula = f'{((value - 32)*5/9):.2f}°C'
            await ctx.send(embed=EmbedBuilder(fromUnit=fromUnit, toUnit=toUnit, value=value, formula=formula))

        else:
            embed = Embed(title='Chimkin Converter',
                          description=f'I currently only support:{supportedUnits}')
            await ctx.send(embed=embed)

    @command(name='currencyconvert',
             aliases=['cconvert', 'cconv'],
             description='Converts X currency to Y currency',
             brief='Converts X currency to Y currency',
             help='Converts X currency to Y currency',
             usage='`.currencyconvert XCurrency to YCurrency`')
    async def convert_currency(self, ctx, amount: float, fromCurrency: str, to: Optional[str], toCurrency: str):
        URL = f'https://free.currconv.com/api/v7/convert?q={fromCurrency}_{toCurrency}&compact=y&apiKey={APIKEY}'

        async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
            if response.status == 200:
                data = await response.json()

                try:
                    dataValue = data[f'{fromCurrency.upper()}_{toCurrency.upper()}']['val']
                    convertedValue = f'{(amount * dataValue):.2f} {toCurrency.upper()}'

                    embed = Embed(title='Chimkin Currency Converter',
                                  description=f'{amount} {fromCurrency.upper()} to {toCurrency.upper()} is {convertedValue}')
                    await ctx.send(embed=embed)
                except KeyError:
                    await ctx.send('Are you sure that is a currency?')

            else:
                await ctx.send(f'Error code:{response.status}')

    @command(name='mindslots',
             aliases=['ms'],
             description='Gives total amount of mindslots and castable warlock book spells',
             brief='Gives total amount of mindslots and castable warlock book spells',
             help='ves total amount of mindslots and castable warlock book spells',
             usage='`.ms <Freezing Spell Level> <Base Level> <Total Int>`\nEg: `.ms 10 200 150`\nInt shown ingame is INT XX+XX - Total int is the sum of that')
    async def mindSlots(self, ctx, freezingSpellLevel: int, baseLevel: int, totalInt: int):
        totalMindSlots = (freezingSpellLevel*8)+(baseLevel//10)+(totalInt//10)

        embed = Embed(title=f'You will have a total of {totalMindSlots} Mind Slots',
                      description='Below are the number of same skills you can store with Reading Spellbook:',
                      color=ctx.author.color)
        embed.add_field(name='Earth Spike, Drain Life',
                        value=f'{7 if (totalMindSlots//8) > 7 else totalMindSlots//8}', inline=True)
        embed.add_field(
            name='LoV, MS, SG', value=f'{7 if (totalMindSlots//10) > 7 else totalMindSlots//10}', inline=True)
        embed.add_field(
            name='CL, CR, ES', value=f'{7 if (totalMindSlots//12) > 7 else totalMindSlots//12}', inline=True)
        embed.add_field(name='Comet, Tetra Vortex',
                        value=f'{7 if (totalMindSlots//22) > 7 else totalMindSlots//22}', inline=True)
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text='Brought to you by Warlock Gang',
                         icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @command(name='acd',
             brief='Calculates how much ACD you need for spamming a skill',
             description='Calculates how much ACD you need for spamming a skill',
             help='Calculates how much ACD you need for spamming a skill',
             usage='`.acd <ASPD> <Skill Delay> <Skill Cooldown>`\nYou can get your ASPD from your stat info ingame pressing Alt+A\nFor the Skill Delay and Skill Cooldown hover over the skill ingame')
    async def get_acd(self, ctx, aspd: int, skillDelay: float, coolDown: Optional[float] = 0):
        try:
            if aspd <= 193:
                atkSpd = (200-aspd)/50

                acdReduction = round(
                    (1-((atkSpd if coolDown < atkSpd else coolDown)/skillDelay))*100)

                embed = Embed(title='Looks like you want to spam skills huh?',
                              description=f'You will need **{acdReduction:.0f}% ACD reduction** to spam a skill with **{skillDelay}s Skill Delay** and **{coolDown}s CD** at **{aspd} ASPD**\nTo see how many times you can spam the skill per second with **{aspd} ASPD**, type `.faq aspd`',
                              color=ctx.author.color)
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url)
                embed.set_footer(
                    text='Note: Skills with hard animation or non-reduceable cooldowns are not spammable', icon_url=ctx.guild.icon_url)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"The maximum ASPD is 193 on Shining Moon RO.\n{aspd} ASPD is not attainable *yet*")
        except ZeroDivisionError:
            await ctx.send('TO INFINITY AND BEYOND\nP.S: Please don\'t use zero.')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("formulas")


def setup(bot):
    bot.add_cog(Formulas(bot))
