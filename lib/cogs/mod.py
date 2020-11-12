from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

from better_profanity import profanity
from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

from ..db import db

profanity.load_censor_words_from_file("./data/profanity.txt")


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def kick_members(self, message, targets, reason):
        for target in targets:
            if (message.guild.me.top_role.position > target.top_role.position
                    and not target.guild_permissions.administrator):
                await target.kick(reason=reason)

                embed = Embed(title='Member kicked',
                              colour=0xDD2222,
                              timestamp=datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [('Member', f'{target.display_name} a.k.a. {target.display_name}', False),
                          ('Done by', message.author.display_name, False),
                          ('Reason', reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)

    @command(name='kick',
             description='To kick naughty awies (Admin command)',
             brief='To kick naughty awies (Admin command)',
             help='Kicks the person/s you mention/tag out of the server',
             usage='`.kick @Lunch @Sorayana @Ashe`')
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'No reason provided'):
        if not len(targets):
            await ctx.send('One or more required arguments missing, idiot.')
        else:
            await self.kick_members(ctx.message, targets, reason)
            await ctx.send('It is done!')

    @kick_command.error
    async def kick_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send('Insufficient permissions to perform tasks.')

    async def ban_members(self, message, targets, reason):
        for target in targets:
            if (message.guild.me.top_role.position > target.top_role.position
                    and not target.guild_permissions.administrator):
                await target.ban(reason=reason)

                embed = Embed(title='Member banned',
                              colour=0xDD2222,
                              timestamp=datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [('Member', f'{target.display_name} a.k.a. {target.display_name}', False),
                          ('Done by', message.author.display_name, False),
                          ('Reason', reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)

    @command(name='ban',
             description='To ban REALLY naughty awies (Admin command)',
             brief='To ban REALLY naughty awies (Admin command)',
                         help='Bans the person/s you mention/tag from ther server',
                         usage='`.ban @Lunch @Ashe @Sorayana`')
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'No reason provided'):
        if not len(targets):
            await ctx.send('One or more required arguments missing, idiot.')
        else:
            await self.ban_members(ctx.message, targets, reason)
            await ctx.send('It is done!')

    @ban_command.error
    async def ban_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send('Insufficient permissions to perform tasks.')

    @command(name='clear',
             aliases=['purge'],
             description='Used to clear messages',
             brief='Used to clear messages - Can do selective message cleaning',
             help='You can bulk delete messages using this command',
             usage='`.clear 100` or `.clear @Sorayana 100`\nDo note that this command can only access messages in cache\nFrom the 2nd example above, Chimkin will look through the last 100 messages and delete all messages in those 100 that were from Sorayana')
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 250:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
                                                  check=_check)

                await ctx.send(f'Deleted {len(deleted):,} messages', delete_after=5)
        else:
            await ctx.send('Make sure your message limit is between 0~250')

    async def mute_members(self, message, targets, secs, reason):
        unmutes = []

        for target in targets:
            if not self.mute_role in target.roles:
                if message.guild.me.top_role.position > target.top_role.position:
                    role_ids = ','.join([str(r.id) for r in target.roles])
                    end_time = datetime.utcnow() + timedelta(seconds=secs) if secs else None

                    db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
                               target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())

                    await target.edit(roles=[self.mute_role])

                    embed = Embed(title='Awie Muted',
                                  colour=0xDD2222,
                                  timestamp=datetime.utcnow())

                    embed.set_thumbnail(url=target.avatar_url)

                    fields = [('Member', target.display_name, False),
                              ('Done by', message.author.display_name, False),
                              ('Duration',
                               f'{secs:,} seconds' if secs else 'Indefinite', False),
                              ('Reason', reason, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.log_channel.send(embed=embed)

                    if secs:
                        unmutes.append(target)

        return unmutes

    @command(name='mute',
             description='Used to mute people.',
             brief='Used to mute people.',
                         help='Mutes the mentioned/tagged person/s',
                         usage='`.mute @Lunch @Ashe 60 for being noisy`\nThis will mute Ashe and Lunch for 60 seconds')
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True, manage_guild=True)
    async def mute_command(self, ctx, targets: Greedy[Member], secs: Optional[int], *,
                           reason: Optional[str] = 'No reason provided'):
        if not len(targets):
            await ctx.send('One or more required arguments are missing, idiot.')

        else:
            unmutes = await self.mute_members(ctx.message, targets, secs, reason)
            await ctx.send('Mute Complete')

            if len(unmutes):
                await sleep(secs)
                await self.unmute_members(ctx.guild, targets)

    @mute_command.error
    async def mute_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send('Insufficient permissions to perform that task.')

    async def unmute_members(self, guild, targets, *, reason='Mute time expired'):
        for target in targets:
            if self.mute_role in target.roles:
                role_ids = db.field(
                    "SELECT RoleIds FROM mutes WHERE UserID = ?", target.id)
                roles = [guild.get_role(int(id_))
                         for id_ in role_ids.split(',') if len(id_)]

                db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)

                await target.edit(roles=roles)

                embed = Embed(title='Awie unmuted',
                              colour=0xDD2222,
                              timestamp=datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [('Member', target.display_name, False),
                          ('Reason', reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)

    @command(name='unmute',
             description='This command will unmute tagged/mentioned person/s',
             brief='This command will unmute tagged/mentioned person/s',
             help='This command will unmute tagged/mentioned person/s',
             usage='`.unmute @Lunch @Ashe because they won\'t be noisy anymore`\nThis will unmute Ashe and Lunch')
    @bot_has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True, manage_guild=True)
    async def unmute_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'No reason provided.'):
        if not len(targets):
            await ctx.send('One or more required argument is missing.')

        else:
            await self.unmute_members(ctx.guild, targets, reason=reason)

    @unmute_command.error
    async def unmute_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send('Insufficient permissions to perform that task.')

    # @command(name='addbadword',
    #          aliases=['addswears', 'addcurses'],
    #          description='Provide a list of bad words for chimkin to get angy at',
    #          brief='Provide a list of bad words for chimkin to get angy at')
    # @has_permissions(manage_guild=True)
    # async def add_profanity(self, ctx, *words):
    #     with open('./data/profanity.txt', 'a', encoding='utf-8') as f:
    #         f.write(''.join([f'{w}\n' for w in words]))

    #     profanity.load_censor_words_from_file('./data/profanity.txt')
    #     await ctx.send('Words added to baddie file. Nyehehe! <:pepefeelsevil:679339391985909772>')

    # @add_profanity.error
    # async def add_profanity_error(self, ctx, exc):
    #     if isinstance(exc, CheckFailure):
    #         await ctx.send('Insufficient permissions to perform that task.')

    # @command(name='delswears',
    #          aliases=['delbadwords', 'delcurses'],
    #          description='Provide a list of bad words for chimkin to get angy at',
    #          brief='Provide a list of bad words for chimkin to get angy at')
    # @has_permissions(manage_guild=True)
    # async def remove_profanity(self, ctx, *words):
    #     with open('./data/profanity.txt', 'r', encoding='utf-8') as f:
    #         stored = [w.strip() for w in f.readlines()]

    #     with open('./data/profanity.txt', 'w', encoding='utf-8') as f:
    #         f.write(''.join([f'{w}\n' for w in stored if w not in words]))

    #     profanity.load_censor_words_from_file('./data/profanity.txt')
    #     await ctx.send('Words removed from baddie file <:sadkitty:633639713588379668>')

    # @remove_profanity.error
    # async def remove_profanity_error(self, ctx, exc):
    #     if isinstance(exc, CheckFailure):
    #         await ctx.send('Insufficient permissions to perform that task.')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(739388066048770118)
            self.mute_role = self.bot.butter.get_role(746577162273816636)
            self.bot.cogs_ready.ready_up("mod")

    @Cog.listener()
    async def on_message(self, message):
        def _check(m):
            return (m.author == message.author
                    and len(m.mentions)
                    and (datetime.utcnow()-m.created_at).seconds < 60)

        if not message.author.bot and message.guild.id == 228966491628765185:
            if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 9:
                await message.channel.send(f"Lol! {message.author.mention} got muted for 420s <:kekw:675005062938099722>", delete_after=60)
                unmutes = await self.mute_members(message, [message.author], 420, reason="Spam tagging people")

                if len(unmutes):
                    await sleep(420)
                    await self.unmute_members(message.guild, [message.author])

            # elif profanity.contains_profanity(message.content):
            # 	await message.add_reaction("🇸")
            # 	await message.add_reaction("🇹")
            # 	await message.add_reaction("🇴")
            # 	await message.add_reaction("🇵")
            # 	await message.add_reaction("<:pepeangry:599852722379816971>")
            # 	await sleep(30)
            # 	await message.clear_reactions()


def setup(bot):
    bot.add_cog(Mod(bot))
