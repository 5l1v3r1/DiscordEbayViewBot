import discord
from discord.ext import commands
import datetime
import yaml
import os
import sys
import random

with open("./Config.yml", 'r') as file:
    config = yaml.load(file, Loader = yaml.Loader)

bot = commands.AutoShardedBot(command_prefix=config['Prefix'], description="Heroicos_HM's Custom Bot", case_insensitive = True)
bot.remove_command('help')

# Main Config
bot.TOKEN = config['TOKEN']
bot.prefix = config['Prefix']
bot.logs_channels = config['Log Channels']
bot.embed_colors = config['Embed Colors']
bot.footer_icon = config['Footer Icon URL']
bot.footer_text = config['Footer Text']
bot.online_message = config['Online Message']

# Options
bot.use_timestamp = config['Options']['Embed Timestamp']
bot.delete_commands = config['Options']['Delete Commands']
bot.show_command_author = config['Options']['Show Author']
bot.show_game_status = config['Options']['Game Status']['Active']
bot.game_to_show = config['Options']['Game Status']['Game']

# Ebay View Settings
bot.view_limit = config['Ebay Settings']['View Limit']
bot.rate_limit_type = config['Ebay Settings']['Rate Limit']['Rate Limit Type']
if bot.rate_limit_type.lower() == 'request':
    bot.rate_limit_type = 'Request'
    bot.rate_limit = config['Ebay Settings']['Rate Limit']['Hourly Request Limit']
else:
    bot.rate_limit_type = 'View'
    bot.rate_limit = config['Ebay Settings']['Rate Limit']['Hourly View Limit']

extensions = [
    'Cogs.General',
    'Cogs.EbayView'
]

for extension in extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print('Logged in as {0} and connected to Discord! (ID: {0.id})'.format(bot.user))
    if bot.show_game_status:
        game = discord.Game(name = bot.game_to_show.format(prefix = bot.prefix))
        await bot.change_presence(activity = game)
    if bot.use_timestamp:
        embed = discord.Embed(
            title = bot.online_message.format(username = bot.user.name),
            description = 'Rate Limit Type: {limit_type}\nLimit: {limit}\nView Limit per Command: {view_limit}'.format(limit_type = bot.rate_limit_type, limit = bot.rate_limit, view_limit = bot.view_limit),
            color = random.choice(bot.embed_colors),
            timestamp = datetime.datetime.now(datetime.timezone.utc)
        )
    else:
        embed = discord.Embed(
            title = bot.online_message.format(username = bot.user.name),
            description = '*Rate Limit Type:* {limit_type}\n*Limit:* {limit}\n*View Limit per Command:* {view_limit}'.format(limit_type = bot.rate_limit_type, limit = bot.rate_limit, view_limit = bot.view_limit),
            color = random.choice(bot.embed_colors)
        )
    embed.set_footer(
        text = bot.footer_text,
        icon_url = bot.footer_icon
    )
    for log in bot.logs_channels:
        channel = bot.get_channel(log)
        await channel.send(content = None, embed = embed)

    bot.start_time = datetime.datetime.now(datetime.timezone.utc)

@bot.command(name='help')
@commands.guild_only()
async def dfs_help(ctx):
    if bot.delete_commands:
        await ctx.message.delete()
    if bot.use_timestamp:
        embed = discord.Embed(
            title = ":newspaper: Help",
            color = random.choice(bot.embed_colors),
            timestamp = datetime.datetime.now(datetime.timezone.utc)
        )
    else:
        embed = discord.Embed(
            title = ":newspaper: Help",
            color = random.choice(bot.embed_colors)
        )
    if bot.show_command_author:
        embed.set_author(
            name = ctx.author.name,
            icon_url = ctx.author.avatar_url
        )
    embed.add_field(
        name = bot.prefix + "view <Link> <Number>",
        value = "Adds views on an Ebay link. Maximum of " + str(bot.view_limit) + ".",
        inline = False
    )
    embed.add_field(
        name = bot.prefix + 'ratelimit',
        value = 'Shows information on rate limits for commands.',
        inline = False
    )
    embed.add_field(
        name = bot.prefix + "uptime",
        value = "Returns the amount of time that the bot has been online.",
        inline = False
    )
    embed.add_field(
        name = bot.prefix + "ping",
        value = "Gets the ping times from the bot to the discord servers and back.",
        inline = False
    )
    embed.set_footer(
        text = bot.footer_text,
        icon_url = bot.footer_icon
    )

    await ctx.send(embed = embed)

bot.run(bot.TOKEN, bot = True, reconnect = True)
