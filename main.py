import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import MissingPermissions
from discord.ext.commands import CommandNotFound

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def ping(ctx):
    latency = discord.Embed(title='Latency', description=f'{round(client.latency * 1000)}ms',
                            color=discord.Color.purple())
    await ctx.send(embed=latency)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    bn = discord.Embed(title='User banned', description=f'{member.mention} has been banned for {reason}',
                       colour=discord.Colour.purple())
    if reason is None:
        reason = 'no reason provided'
    await ctx.guild.ban(member)
    await ctx.send(f'banned {member.mention} for {reason}')


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    kck = discord.Embed(title=f'User kicked', description=f'{member.mention} was kicked for {reason}',
                        colour=discord.Colour.purple())
    if reason is None:
        reason = 'no reason provided'
    await ctx.guild.kick(member)
    await ctx.send(embed=kck)


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amt):
    prg = discord.Embed(title='Purged', description=f'{amt} message(s)', colour=discord.Color.purple())
    await ctx.channel.purge(limit=int(amt) + 1)
    msg = await ctx.send(embed=prg)
    await asyncio.sleep(3)
    await msg.delete()


@client.command()
async def avatar(ctx, member: discord.Member):
    av = discord.Embed(title=f'{member.name}').set_image(url=member.avatar.url)
    await ctx.send(embed=av)


@client.command()
async def commands(ctx):
    cmds = discord.Embed(
        title=" park commands",
        description=" purge \n"
                    " ban \n"
                    " kick \n"
                    " avatar \n"
                    "ping \n"
                    "commands",
        colour=discord.Color.purple()

    )
    await ctx.send(embed=cmds)


#@client.command()
#async def suggest(ctx, *, suggestion):
#   user = await client.fetch_user("your user id")
#  await DMChannel.send(park, f"{suggestion}, ***sent by {ctx.author}***")
# await ctx.send('Suggestion was sent :white_check_mark: ')

#i don't reccomend using, bc dm floods or trolls

@kick.error
async def kick_error(ctx, error):
    perms = discord.Embed(title='Lacking permissions', colour=discord.Color.red())
    if isinstance(error, MissingPermissions):
        await ctx.send(embed=perms)


@ban.error
async def ban_error(ctx, error):
    perms = discord.Embed(title='Lacking permissions', colour=discord.Color.red())
    if isinstance(error, MissingPermissions):
        await ctx.send(embed=perms)


@purge.error
async def purge_error(ctx, error):
    perms = discord.Embed(title='Lacking permissions', colour=discord.Color.red())
    if isinstance(error, MissingPermissions):
        await ctx.send(embed=perms)


@client.event
async def on_command_error(ctx, error):
    perms = discord.Embed(title='Unknown command', colour=discord.Color.red())
    if isinstance(error, CommandNotFound):
        await ctx.send(embed=perms)


client.run('token')
