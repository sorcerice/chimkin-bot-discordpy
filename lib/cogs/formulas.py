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
             help='Gives total amount of mindslots and castable warlock book spells',
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
            # attacks per second
            if coolDown == 0:
                aps = round(50/(200-aspd))
            elif coolDown > 0.14:
                aps = round(1/coolDown)

            apsComment = f'You will be able to spam the skill at **{aps} attacks/second**'

            if aspd <= 193:
                atkSpd = (200-aspd)/50

                acdReduction = round(
                    (1-((atkSpd if coolDown < atkSpd else coolDown)/skillDelay))*100)

                if coolDown > skillDelay:
                    await ctx.send('The provided cooldown was greater than the skill delay\nYou won\'t be able to spam the skill even if you reduce ACD')
                else:
                    if acdReduction < 0:
                        acdReduction = 0
                    embed = Embed(
                        title='Looks like you want to spam skills huh?',
                        description=f'You will need **{acdReduction:.0f}% ACD reduction** to spam a skill with **{skillDelay}s Skill Delay** and **{coolDown}s CD** at **{aspd} ASPD**\n{apsComment}\n\n**Note:** *People usually target 7 attacks/s*\nFor 0s CD skill, people usually target 7 attacks/second',
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

    @command(name='vctstat',
             brief='Calculates VCT reduction based on total DEX and INT',
             description='Provide the total DEX followed by total INT to get VCT Reduction % and the remaining VCT %',
             help='When using the command please provide total DEX and then the total INT in that order only',
             usage='`.vctstat <TOTAL DEX> <TOTAL INT>\nTotal of any stat means the sum of the stat shown in your ALT+A window ingame\nEx: DEX 120+30 will be shown ingame so the Total DEX will be 150`')
    async def get_vctstat(self, ctx, totalDex: int, totalInt: int):
        vctReduction = ((totalDex*2 + totalInt)/530) * 100
        vctRemaining = 100 - vctReduction

        if vctReduction > 100:
            vctReduction = 100
        if vctRemaining < 0:
            vctRemaining = 0

        embed = Embed(title='VCT Calculation? But why? OK Fine I\'ll do it...',
                      description=f'\n\nYou have a total of **{vctReduction:.2f}% VCT Reduction** and **{vctRemaining:.2f}% VCT left**\n\n**Total Dex= {totalDex}** || **Total INT = {totalInt}**\n\n',
                      color=ctx.author.color)
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(
            text=f'Why would you make me do this {ctx.author.display_name}.... *sigh*', icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @command(name='vctcount',
             brief='Calculates how many seconds of VCT remains based on total DEX, INT and skill VCT',
             description='Provide the total DEX, total INT and skill VCT to get the VCT remaining in seconds',
             help='When using the command please provide total DEX, total INT and then skill VCT in that order only',
             usage='`.vctcount <TOTAL DEX> <TOTAL INT> <SKILL VCT>\nTotal of any stat means the sum of the stat shown in your ALT+A window ingame\nEx: DEX 120+30 will be shown ingame so the Total DEX will be 150`\nTo get the skill VCT count hover over the skill ingame')
    async def get_vctcount(self, ctx, totalDex: int, totalInt: int, skillVCT: int):
        vctRemainingSeconds = skillVCT * (1 - ((totalDex*2 + totalInt)/530))

        embed = Embed(title='VCT Calculation for the seconds of VCT remaining',
                      description=f'\n\nYou have a total of **{vctRemainingSeconds:.2f} seconds** of VCT remaining for a skill with **{skillVCT}s** VCT\n **Total DEX = {totalDex}** || **Total INT = {totalInt}**\n\n',
                      color=ctx.author.color)
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(
            text=f'My brain hurts after doing this... *sigh*', icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("formulas")


def setup(bot):
    bot.add_cog(Formulas(bot))
