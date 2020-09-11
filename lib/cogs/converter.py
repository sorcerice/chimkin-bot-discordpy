from typing import Optional

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command

from aiohttp import request
from libneko import pag

supportedUnits = '\n1)celcius-fahrenheit\n2)fahrenheit-celcius'

with open("./lib/bot/currencyconvertapikey.0", "r", encoding="utf-8") as f:
	APIKEY = f.read()

class Converter(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name='unitconvert',
			 aliases=['uconvert'],
			 description=f'Converts units, currently supports:{supportedUnits}',
			 brief=f'Converts units, currently supports:{supportedUnits}')
	async def convert_units(self, ctx, value : float, fromUnit : str, toStr : Optional [str], toUnit: str):
		def EmbedBuilder(fromUnit : str, toUnit : str, value, formula):
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
			 aliases=['cconvert'],
			 description='Converts X currency to Y currency',
			 brief='Converts X currency to Y currency')
	async def convert_currency(self, ctx, fromCurrency: str, toCurrency: str, amount:Optional [float] = 1):
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




	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("converter")

def setup(bot):
	bot.add_cog(Converter(bot))