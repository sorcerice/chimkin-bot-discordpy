from datetime import datetime
from typing import Optional

from discord import Embed, Member, File
from discord.ext.commands import Cog
from discord.ext.commands import command

currentTags = ''


class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='userinfo',
             aliases=['memberinfo', 'ui'],
             description='Provides info about your discord account or the tagged persons discord account',
             brief='Provides info about your discord account or the tagged persons discord account',
             help='Provides info about your discord account or the tagged persons discord account')
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(title='User Information',
                      colour=target.colour,
                      timestamp=datetime.utcnow())

        fields = [('Name', str(target), True),
                  ('ID', target.id, False),
                  ('Bot?', target.bot, True),
                  ('Top Role', target.top_role.mention, True),
                  ('Status', str(target.status).title(), True),
                  ('Activity',
                   f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else 'N/A'}", True),
                  ('Created at', target.created_at.strftime(
                      "%d/%m/%Y %H:%M:%S"), True),
                  ('Joined at', target.joined_at.strftime(
                      "%d/%m/%Y %H:%M:%S"), True),
                  ('Boosted', bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=target.avatar_url)

        await ctx.send(embed=embed)

    @command(name='serverinfo',
             aliases=['guildinfo', 'si', 'gi'],
             brief='Provides information about the server',
             description='Provides information about the server',
             help='Provides information about the server')
    async def server_info(self, ctx):
        embed = Embed(title='Server Information',
                      colour=ctx.guild.owner.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status)
                                    == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [('ID', ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Region", ctx.guild.region, True),
                  ("Created at", ctx.guild.created_at.strftime(
                      "%d/%m/%Y %H:%M:%S"), True),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Banned members", len(await ctx.guild.bans()), True),
                  ("Statuses",
                   f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name='guides',
             alias=['guide'],
             brief='Provides useful forum links to the mentioned person',
             description='You can either use the command by itself or mention a person to tag with the response')
    async def helper_command(self, ctx, member: Optional[Member]):
        if member:
            await ctx.send(f'Heya {member.mention}! \nForum Guides Section: https://www.shining-moon.com/ipb/index.php?/forum/45-guides/ \nHelheim Guide Section: https://www.shining-moon.com/ipb/index.php?/forum/82-helheim/ \nNiflheim Guide Section: https://www.shining-moon.com/ipb/index.php?/forum/58-niflheim/ \n\nFor build, equipment or any other guides check out the forum! \nNote: To access a major chunk of the forum you need a separate forum ID.')
        else:
            await ctx.send('Forum Guides Section: https://www.shining-moon.com/ipb/index.php?/forum/45-guides/ \nHelheim Guide Section: https://www.shining-moon.com/ipb/index.php?/forum/82-helheim/ \nNiflheim Guide Section: https://www.shining-moon.com/ipb/index.php?/forum/58-niflheim/ \n\nFor build, equipment or any other guides check out the forum! \nNote: To access a major chunk of the forum you need a separate forum ID.')

    @command(name='faq',
             brief='To help out with support questions',
             description='You need to have a valid faq tag\nCurrent FAQ tags are: ip, init, replay, shadow, helnif, aspd, enchants, resolution, boostermaps, 4th alt ticket, power dim essence, class rebalance')
    async def faq_command(self, ctx, *, faq_tag: str = 'list'):
        if faq_tag.lower() == 'ip':
            embed = Embed(title='FAQ',
                          description='SMRO Server Host Information',
                          colour=0x4dfc32)

            embed.add_field(name='Server Location',
                            value='Beauharnois,Quebec,Canada', inline=False)
            embed.add_field(name='Helheim IP:',
                            value='51.161.117.101', inline=False)
            embed.add_field(name='Niflheim IP:',
                            value='192.99.66.84', inline=False)

            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(
                url='https://www.shining-moon.com/hel/themes/default/img/logo.gif')
            embed.set_footer(
                text='This FAQ was stolen from SMRO discord', icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif faq_tag.lower() == 'init':
            embed = Embed(title='ERROR : Cannot init d3d OR grf file has problem.',
                          description='''```a) can be cause of resolution - try starting at lowest\nb) can be cause of graphic device\nc) can be cause of access violation - restart sometimes solves it\nd) can be cause of outdated direct x\ne) can be cause of outdated graphic card driver\nf) Install the latest c++ / framework might  help as well\ng) Try running shining.exe straight as admin, have fixed it for some people previously\nh) If previous don't work, restart your PC.```''',
                          colour=0x4dfc32)

            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)
            embed.set_footer(
                text='This FAQ was stolen from SMRO discord', icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif faq_tag.lower() == 'replay':
            await ctx.send(f'{ctx.author.mention}\n**How To Play Replays:**\nhttps://cdn.discordapp.com/attachments/546255961992724481/673116241526915072/replay.mp4')

        elif faq_tag.lower() == 'shadow':
            await ctx.send(f'{ctx.author.mention}\nShadow Equipment List:\nhttps://www.shining-moon.com/helheim/index.php/Shadow_Equipment')

        elif faq_tag.lower() == 'helnif' or faq_tag.lower() == 'nifhel':
            embed = Embed(title='Difference between Helheim and Niflheim',
                          description='''**TL;DR:**\n```**Helheim** = kRO only balance and progressions, newer server, more players.\n*``````*Niflheim** = A mix of kRO, jRO and iRO balance and progressions, older server, less players, more build possibilities, more competitively viable endgame builds, better endgame damage potentials due to gears and easier refines.```''',
                          colour=0x4dfc32)
            embed.set_image(
                url='https://cdn.discordapp.com/attachments/605132888265981962/605135987890192393/unknown.png')

            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)
            embed.set_footer(
                text='This FAQ was stolen from SMRO discord', icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif faq_tag.lower() == 'aspd':
            embed = Embed(title='ASPD Golden Numbers',
                          description='```193 ASPD = up to 7 attacks/sec\n192 ASPD = up to 6 attacks/sec\n190 ASPD = up to 5 attacks/sec\n188 ASPD = up to 4 attacks/sec```',
                          colour=0x4dfc32)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)
            embed.set_footer(
                text='This FAQ was stolen from SMRO discord', icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif faq_tag.lower() == 'enchants':
            embed = Embed(title='Lapine Enchants - Click Me',
                          url='https://www.shining-moon.com/helheim/index.php/Lapine_Enchanting',
                          colour=0x4dfc32)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)
            embed.set_footer(
                text='This FAQ was stolen from SMRO discord', icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif faq_tag.lower() == 'resolution':
            await ctx.send(f'{ctx.author.mention}\n**Having resolution problems?**\nCheck this link out:\nhttps://www.shining-moon.com/w/index.php/Resolution')

        elif faq_tag.lower() == 'booster maps' or faq_tag.lower() == 'boostermaps':
            embed = Embed(title='Maps used for booster quests',
                          description='''```@warp prt_fild06 Fabre\n@warp pay_fild06 Snake, Spore Wormtail\n@warp mjolnir_06 Poison Spore\n@warp mjo_dun02 Martin, Giearth\n@warp mjo_dun03 Skeleton Worker\n@warp iz_dun03 Swordfish\n@warp iz_dun04 Swordfish (less), Merman, Strouf\n@warp pay_dun02 Munak, Bongun\n@warp pay_dun03 Sohee\n@warp c_tower1 Rideword\n@warp c_tower3 Alarm\n@warp c_tower4 Clock\n@warp tur_dun02 Permeter, Freezer\n@warp tur_dun03 Permeter, Freezer, Heater\n@warp tur_dun04 Permeter, Freezer, Heater \n@warp ice_dun03 Gazeti, Ice Titan, Snowier, Iceicle\n@warp ma_fild02 Bungisngis\n@warp dic_dun01 Scaraba (Small Insect 130-145)\n@warp abbey01 Banshee (Dark 130-145)\n@warp lasa_dun03 Combat Basilisk, Fruits Pom Spider (Earth Medium 145-160)\n@warp c_tower2_ Neo Punk (Small 145-160)\n@warp c_tower3_ Big Bell, Owl Viscount, Owl Marquis```''',
                          color=ctx.author.color)
            embed.set_footer(
                text='Credits to @Tom#3331 and @Melon Bun#1508', icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif faq_tag.lower() == '4th alt ticket' or faq_tag.lower() == '4th' or faq_tag.lower() == '4th alt':
            embed = Embed(title='4th Class Outfit Ticket',
                          description='```15x Darkgreen Dyestuff ID: 979\n15x Orange Dyestuff ID: 980\n5x Costume Treasure ID: 51010\n1x Alternate Outfit Ticket ID: 51022\n50x Frozen Rose ID: 749\n50x Ancient Hero Souls ID: 1900000008\n100x Greater Fortessa Emblem ID: 1900000003```',
                          colour=ctx.author.color)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)
            embed.set_footer(text='Have fun farming!',
                             icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif faq_tag.lower() == 'pde' or faq_tag.lower() == 'power dim essence':
            embed = Embed(title='Powerful Dimensional Essence',
                          description='```5x Temporal Metal ID: 190000011\n10x Temporal Crystal ID: 6607\n250x Chivalry Emblem ID: 1004\n5x Will of Red Darkness ID: 7566\n25x Blade Lost in Darkness ID: 7023```',
                          colour=ctx.author.color)
            embed.set_thumbnail(
                url='https://www.divine-pride.net/img/items/item/kROM/7925')
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)
            embed.set_footer(text='Have fun farming!',
                             icon_url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        elif(faq_tag.lower() == 'class rebalance'):
            await ctx.send('https://www.divine-pride.net/forum/index.php?/topic/4203-kro-skill-adjustment-timeline/')

        elif(faq_tag.lower() == any(['booster char', 'boosterchar'])):
            await ctx.send('`When you create a booster character, if you delete the  created  booster character or  if you cancel the booster NPC, **YOU WILL NOT BE ABLE TO CREATE A NEW BOOSTER CHARACTER** !`\nPlease pay attention and be careful when you are making your choices.')

        elif(faq_tag.lower() == any(['element table', 'element tables', 'elements'])):
            await ctx.send('https://cdn.discordapp.com/attachments/772453956810571829/874278146092982322/image0.png')

        else:
            await ctx.send('You need to have a valid faq tag\nCurrent FAQ tags are: ip, init, replay, shadow, helnif, aspd, enchants, resolution, boostermaps, 4th alt ticket, power dim essence, class rebalance, booster char, elements')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("info")


def setup(bot):
    bot.add_cog(Info(bot))
