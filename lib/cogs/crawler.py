from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.errors import HTTPException

from bs4 import BeautifulSoup
from aiohttp import request
import pandas as pd


class Crawler(Cog):
	def __init__(self, bot):
		self.bot = bot


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("crawler")



	@command(name='monster',
			 aliases=['m', 'mi2', 'mob'],
			 brief='Provides monster info from SMRO',
			 description='Provides monster info from SMRO')
	async def monster_search(self, ctx, monsterID: int):
		spriteURL = f'https://www.shining-moon.com/data/monsters/{monsterID}.gif'
		URL = f'https://www.shining-moon.com/hel/?module=monster&action=view&id={monsterID}'
		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')

		soup = BeautifulSoup(page.decode('utf-8'), 'lxml')

		table = soup.find_all('table', class_='vertical-table')[0]

		name = table.find_all('tr')[1].find_all('td')[0]
		size = table.find_all('tr')[3].find_all('td')[0]
		race = table.find_all('tr')[4].find_all('td')[0]
		elem = table.find_all('tr')[5].find_all('td')[0]
		HP = table.find_all('tr')[2].find_all('td')[1]

		embed = Embed(title='Click here to go this page',
					  colour=ctx.author.colour,
					  url = URL)
		embed.add_field(name = f'{name.text.strip()}', value='Name', inline=False)
		embed.add_field(name = f'{HP.text.strip()}', value='HP', inline=False)
		embed.add_field(name = f'{size.text.strip()}', value='Size', inline=False)
		embed.add_field(name = f'{race.text.strip()}', value='Race', inline=False)
		embed.add_field(name = f'{elem.text.strip()}', value='Element', inline=False)
		embed.set_thumbnail(url=spriteURL)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)

		await ctx.send(embed=embed)



	@command(name='item',
			 aliases=['ii2', 'i'],
			 brief='Provides item info from SMRO',
			 description='Provides item info from SMRO')
	async def item_search(self, ctx, itemID: int):
		spriteURL = f'https://www.shining-moon.com/hel/data/items/images/{itemID}.png'
		URL = f'https://www.shining-moon.com/?module=item&action=view&id={itemID}'
		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')

		soup = BeautifulSoup(page.decode('utf-8'), 'lxml')

		table = soup.find_all('table', class_='vertical-table')[0]

		nameRow = table.find_all('tr')[2]
		name = nameRow.find_all('td')[0]

		dDiv = soup.find_all('div', class_='inner')[0]
		dTable = dDiv.find('table')

		embed = Embed(title='Click here to go this page',
					  colour=ctx.author.colour,
					  url=URL)
		embed.add_field(name = '----', value = f'**{name.text.strip()}**', inline=False)
		embed.add_field(name = '----', value = f'{dTable.text.strip()}', inline=False)
		embed.set_thumbnail(url=spriteURL)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)

		await ctx.send(embed=embed)



	@command(name='monsterid',
			 aliases=['mi','mid'],
			 brief='Looks for mob IDs',
			 description='Looks for mob IDs')
	async def mobID_search(self, ctx, *, mobName: str):
		URL = f'https://www.shining-moon.com/hel/?module=monster&action=index&monster_id=&name={mobName}&mvp=all&size=-1&race=-1&element=-1&card_id=&custom='

		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')
		try:
			dfs = pd.read_html(page)
			df1 = dfs[0][['Monster ID ▲', 'kRO Name']]

			embed = Embed(title='Click here to go this page',
						  description=f'```{df1}```',
						  colour=ctx.author.colour,
						  url=URL.replace(' ', '+'))
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)

			await ctx.send(embed=embed)
		except ValueError:
			await ctx.send("This monster doesn't seem to exist. Check for typos, stupid.")



	@command(name='itemid',
			  aliases=['iid','idi','ii'],
			  brief="Looks for item IDs",
			  description="Looks for item IDs")
	async def itemID_search(self, ctx, *, itemName: str):
		URL = f'https://www.shining-moon.com/hel/?module=item&action=index&item_id=&name={itemName}&script=&type=-1&equip_loc=-1&npc_buy_op=eq&npc_buy=&npc_sell_op=eq&npc_sell=&weight_op=eq&weight=&range_op=eq&range=&slots_op=eq&slots=&defense_op=eq&defense=&attack_op=eq&attack=&matk_op=eq&matk=&refineable=&for_sale=&custom='

		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')

		try:
			dfs = pd.read_html(page)
			df1 = dfs[0][['Item ID ▲', 'Name.1']]

			embed = Embed(title='Click here to go this page',
						  description=f'```{df1}```',
						  colour=ctx.author.colour,
						  url=URL.replace(' ', '+'))
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)

			await ctx.send(embed=embed)
		except ValueError:
			await ctx.send("This item doesn't seem to exist. Check for typos, stupid.")
			


	@command(name='market',
			 aliases=['shop', 'prices', 'ws'],
			 brief='Look for items in market',
			 description='Looks for items in market')
	async def market_search(self, ctx, itemID: int):
		URL = f'https://www.shining-moon.com/hel/?module=item&action=view&id={itemID}'
		
		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()
				try:
					dfs = pd.read_html(page)
					pd.set_option('display.max_colwidth', 20)
					try:
						if len(dfs[1].columns) == 6:
							df1 = dfs[2][['Price', 'Amount', 'Shop Name']].sort_values(by=['Price'], ascending=True)
						else:
							df1 = dfs[1][['Price', 'Amount', 'Shop Name']].sort_values(by=['Price'], ascending=True)
						embed = Embed(title='Awie Market(Click here to go this page)',
									  description=f"```{df1}```",
									  colour=ctx.author.colour,
									  url=f'https://www.shining-moon.com/hel/?module=item&action=view&id={itemID}')
						embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
						embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)
						await ctx.send(embed=embed)
					except (KeyError, IndexError):
						await ctx.send("Item is probably not on vend.")
				except ValueError:
					await ctx.send("Item doesn't exist or isn't up for sale. Check for typos, stupid.")
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')



	@command(name='marketenchants',
			 aliases=['wse', 'enchants', 'markete', 'ws2'],
			 brief='Looks for enchants on specified item number in vends',
			 description='Looks for enchants on specified item number in vends')
	async def market_enchants(self, ctx, itemID:int, index:int):
		URL = f'https://www.shining-moon.com/hel/?module=item&action=view&id={itemID}'
		
		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()
				soup = BeautifulSoup(page.decode('utf-8'), 'lxml')

				try:
					grabName = soup.find_all('table', class_='vertical-table')[1].find('tbody').find_all('tr')[index].find_all('td')[2]
					grabEnchants = soup.find_all('table', class_='vertical-table')[1].find('tbody').find_all('tr')[index].find('ul')
					grabCard1 = soup.find_all('table', class_='vertical-table')[1].find('tbody').find_all('tr')[index].find_all('td')[3]
					grabCard2 = soup.find_all('table', class_='vertical-table')[1].find('tbody').find_all('tr')[index].find_all('td')[4]
					grabCard3 = soup.find_all('table', class_='vertical-table')[1].find('tbody').find_all('tr')[index].find_all('td')[5]
					grabCard4 = soup.find_all('table', class_='vertical-table')[1].find('tbody').find_all('tr')[index].find_all('td')[6]

					try:
						i = 0
						strEnchants = ''
						for enchants in grabEnchants:
							enchant = grabEnchants.find_all('li')[i]
							enchants = enchant.text.strip()
							strEnchants += str(enchants) + '\n'
							i += 1
					except TypeError:
						strEnchants = 'No random enchants'

					embed = Embed(title='Cards and Enchants',
								  description=f'```{grabName.text.strip()}```',
								  colour=ctx.author.colour)
					embed.add_field(name='Enchants', value=f'```{strEnchants}```')
					embed.add_field(name='Card 1', value=f'```{grabCard1.text.strip()}```', inline=False)
					embed.add_field(name='Card 2', value=f'```{grabCard2.text.strip()}```', inline=False)
					embed.add_field(name='Card 3', value=f'```{grabCard3.text.strip()}```', inline=False)
					embed.add_field(name='Card 4', value=f'```{grabCard4.text.strip()}```', inline=False)
					embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
					embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)
					await ctx.send(embed=embed)
				
				except AttributeError:
					await ctx.send('There likely are no enchants for that')
				
			else:
				await ctx.send(f'Error {response.status}. Try Again.')


	@command(name='historyenchants',
			 aliases=['wshe', 'henchants', 'olde', 'wsh2'],
			 brief='Looks for enchants on specified item number in vend history',
			 description='Looks for enchants on specified item number in vend history')
	async def history_enchants(self, ctx, itemID:int, index:int):
		URL = f'https://www.shining-moon.com/hel/?module=item&action=view&id={itemID}'
		
		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()
				soup = BeautifulSoup(page.decode('utf-8'), 'lxml')

				try:
					grabName = soup.find_all('table', class_='vertical-table')[2].find('tbody').find_all('tr')[index].find_all('td')[1]
					grabEnchants = soup.find_all('table', class_='vertical-table')[2].find('tbody').find_all('tr')[index].find('ul')
					grabCard1 = soup.find_all('table', class_='vertical-table')[2].find('tbody').find_all('tr')[index].find_all('td')[2]
					grabCard2 = soup.find_all('table', class_='vertical-table')[2].find('tbody').find_all('tr')[index].find_all('td')[3]
					grabCard3 = soup.find_all('table', class_='vertical-table')[2].find('tbody').find_all('tr')[index].find_all('td')[4]
					grabCard4 = soup.find_all('table', class_='vertical-table')[2].find('tbody').find_all('tr')[index].find_all('td')[5]
	
					try:
						i = 0
						strEnchants = ''
						for enchants in grabEnchants:
							enchant = grabEnchants.find_all('li')[i]
							enchants = enchant.text.strip()
							strEnchants += str(enchants) + '\n'
							i += 1
					except TypeError:
						strEnchants = 'No random enchants'
				
					embed = Embed(title='Cards and Enchants from Vending History',
								  description=f'```{grabName.text.strip()}```',
								  colour=ctx.author.colour)
					embed.add_field(name='Enchants', value=f'```{strEnchants}```')
					embed.add_field(name='Card 1', value=f'```{grabCard1.text.strip()}```', inline=False)
					embed.add_field(name='Card 2', value=f'```{grabCard2.text.strip()}```', inline=False)
					embed.add_field(name='Card 3', value=f'```{grabCard3.text.strip()}```', inline=False)
					embed.add_field(name='Card 4', value=f'```{grabCard4.text.strip()}```', inline=False)
					embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
					embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)
					await ctx.send(embed=embed)
				except AttributeError:
					await ctx.send('There is likely no enchants for that item')
			else:
				await ctx.send(f'Error {response.status}. Try Again.')



	@command(name='vendhistory',
			 aliases=['wsh', 'shoph', 'oldprices'],
			 brief='Look for vend history',
			 description='Look for vend history')
	async def vend_history(self, ctx, itemID: int):
		URL = f'https://www.shining-moon.com/hel/?module=item&action=view&id={itemID}'
		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()

				pd.set_option('display.max_colwidth', 20)
				dfs = pd.read_html(page)

				try:
					df1 = dfs[3][['Date ▼', 'Price', 'Amount Sold']]
				except IndexError:
					try:
						df1 = dfs[2][['Date ▼', 'Price', 'Amount Sold']]
					except IndexError:
						await ctx.send('Item was probably never on sale.')
				try:
					embed = Embed(title='Awie Market(Click here to go this page)',
								  description=f"```{df1}```",
								  colour=ctx.author.colour,
								  url = f'https://www.shining-moon.com/hel/?module=item&action=view&id={itemID}')
					embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
					embed.set_footer(text="Taken from Lunar's basement", icon_url=ctx.guild.icon_url)
					await ctx.send(embed=embed)
				except UnboundLocalError:
					await ctx.send('Try again later.')
			else:
				await ctx.send(f'Beep Boop\n{response.status} status')



	@command(name='whereis',
			 aliases=['wi'],
			 brief='Look for mob location. Does not work with SMRO custom mobs',
			 description='Look for mob location Divine Pride API')
	async def mob_location(self, ctx, mobID: int):
		
		with open("./lib/bot/dpapikey.0", "r", encoding="utf-8") as dp:
			APIKEY = dp.read()

		URL = f'https://divine-pride.net/api/database/Monster/{mobID}?apiKey={APIKEY}'

		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				data = await response.json()

				mobName = data.get('name')

				embed = Embed(title = f'Where is {mobName}?',
							  colour = ctx.author.colour)

				mapname = ''
				amount = ''
				respawnTime = ''

				spawn_access = data['spawn']
				for spawn_data in spawn_access:
					mapname += spawn_data['mapname'] + '\n'

				spawn_access = data['spawn']
				for spawn_data in spawn_access:
					amount += str(spawn_data['amount']) + '\n'

				spawn_access = data['spawn']
				for spawn_data in spawn_access:
					respawnTime += str(spawn_data['respawnTime']//1000) + 's\n'

				embed.add_field(name = 'Map Name', value = f'{mapname}', inline = True)
				embed.add_field(name = 'Amount', value = f'{amount}', inline = True)
				embed.add_field(name = 'Respawn Time', value = f'{respawnTime}', inline = True)
				embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Provided by Divine Pride API", icon_url=ctx.guild.icon_url)

				await ctx.send(embed=embed)

			else:
				await ctx.send(f"Beep Boop\nError {response.status}. This doesn't exist in Divine Pride")


	@command(name='news',
			 description='Latest News from SMRO',
			 brief='Latest News from SMRO')
	async def get_news(self, ctx):
		URL = "https://www.shining-moon.com/"

		async with request("GET", URL, headers={'User-Agent': 'Mozilla/5.0'}) as response:
			if response.status == 200:
				page = await response.read()

				soup = BeautifulSoup(page.decode('utf-8'), 'lxml')

				links = []
				for a in soup.find_all('a', href=True):
					if a.text:
						links.append(a['href'])

				newsData0 = soup.find_all('div', class_='news-content')[0].text.strip()
				newsData1 = soup.find_all('div', class_='news-item', recursive=True)[1].text.strip()
				newsData2 = soup.find_all('div', class_='news-item', recursive=True)[2].text.strip()

				newsTitle0 = soup.find_all('div', class_='news-content')[0].find('a').text.strip()
				newsTitle1 = soup.find_all('div', class_='news-content')[1].find('a').text.strip()
				newsTitle2 = soup.find_all('div', class_='news-content')[2].find('a').text.strip()

				embed=Embed(title="SMRO News",
							colour=ctx.author.colour)

				fields=[(f"```{newsData0}```", f"[{newsTitle0}]({links[14]})<-Click to go to forum post", False),
						(f"```{newsData1}```", f"[{newsTitle1}]({links[15]})<-Click to go to forum post", False),
						(f"```{newsData2}```", f"[{newsTitle2}]({links[16]})<-Click to go to forum post", False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				embed.set_thumbnail(url='https://www.shining-moon.com/hel/themes/default/img/logo.gif')
				embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
				embed.set_footer(text='Buttery Buns in Butter', icon_url=ctx.guild.icon_url)

				await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(Crawler(bot))