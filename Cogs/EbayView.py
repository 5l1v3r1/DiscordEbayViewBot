import discord
from discord.ext import commands
import datetime
import random
from urllib.parse import urlparse
import time
import requests
import json

class EbayView(commands.Cog, name = "EbayView"):
    def __init__(self, bot):
        self.bot = bot
        self.bot.view_data = {}
        print("Loaded EbayView Cog.")

    @commands.command(name = 'ratelimit', aliases = ['rate', 'limit', 'rl'])
    @commands.guild_only()
    async def ratelimit(self, ctx):
        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = 'Rate Limit Information',
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = 'Rate Limit Information',
                color = random.choice(self.bot.embed_colors)
            )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.add_field(
            name = 'Ebay Views',
            value = '*Rate Limit Type:* **{limit_type}**\n*Limit:* **{limit} {limit_type}s/hour**\n*View Limit per Command:* **{view_limit}**'.format(limit_type = self.bot.rate_limit_type, limit = self.bot.rate_limit, view_limit = self.bot.view_limit)
        )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )
        await ctx.send(embed = embed)

    @commands.command(name = 'view')
    @commands.guild_only()
    async def add_views(self, ctx, link = None, num_views: int = None):
        if self.bot.rate_limit_type == 'Request' and self.bot.rate_limit > 0 and str(ctx.author.id) in self.bot.view_data.keys() and 'last_view_time' in self.bot.view_data[str(ctx.author.id)].keys() and self.bot.view_data[str(ctx.author.id)]['last_view_time'] + (3600 / self.bot.rate_limit) > time.time() and 'num_views' in self.bot.view_data[str(ctx.author.id)].keys() and self.bot.view_data[str(ctx.author.id)]['num_views'] >= self.bot.rate_limit:
            seconds_left = int(self.bot.view_data[str(ctx.author.id)]['last_view_time'] + (3600 / self.bot.rate_limit) - time.time())
            minutes_left = int(seconds_left / 60)
            seconds_left = seconds_left - (minutes_left * 60)
            if self.bot.use_timestamp:
                embed = discord.Embed(
                    title = 'Rate Limit Hit',
                    description = 'You have reached the maximum number of requests per hour. Please wait {mins} minutes and {secs} seconds.'.format(mins = minutes_left, secs = seconds_left),
                    color = random.choice(self.bot.embed_colors),
                    timestamp = datetime.datetime.now(datetime.timezone.utc)
                )
            else:
                embed = discord.Embed(
                    title = 'Rate Limit Hit',
                    description = 'You have reached the maximum number of requests per hour. Please wait {mins} minutes and {secs} seconds.'.format(mins = minutes_left, secs = seconds_left),
                    color = random.choice(self.bot.embed_colors)
                )
            if self.bot.show_command_author:
                embed.set_author(
                    name = ctx.author.name,
                    icon_url = ctx.author.avatar_url
                )
            embed.add_field(
                name = 'Limit',
                value = '{} requests/hour'.format(self.bot.rate_limit)
            )
            embed.set_footer(
                text = self.bot.footer_text,
                icon_url = self.bot.footer_icon
            )
            await ctx.send(embed = embed)
        elif self.bot.rate_limit_type == 'View' and self.bot.rate_limit > 0 and str(ctx.author.id) in self.bot.view_data.keys() and 'last_view_time' in self.bot.view_data[str(ctx.author.id)].keys() and self.bot.view_data[str(ctx.author.id)]['last_view_time'] + 3600 > time.time() and 'num_views' in self.bot.view_data[str(ctx.author.id)].keys() and self.bot.view_data[str(ctx.author.id)]['num_views'] >= self.bot.rate_limit:
            seconds_left = int(self.bot.view_data[str(ctx.author.id)]['last_view_time'] + (3600 / self.bot.rate_limit) - time.time())
            minutes_left = int(seconds_left / 60)
            seconds_left = seconds_left - (minutes_left * 60)
            if self.bot.use_timestamp:
                embed = discord.Embed(
                    title = 'Rate Limit Hit',
                    description = 'You have reached the maximum number of views per hour. Please wait {mins} minutes and {secs} seconds.'.format(mins = minutes_left, secs = seconds_left),
                    color = random.choice(self.bot.embed_colors),
                    timestamp = datetime.datetime.now(datetime.timezone.utc)
                )
            else:
                embed = discord.Embed(
                    title = 'Rate Limit Hit',
                    description = 'You have reached the maximum number of views per hour. Please wait {mins} minutes and {secs} seconds.'.format(mins = minutes_left, secs = seconds_left),
                    color = random.choice(self.bot.embed_colors)
                )
            if self.bot.show_command_author:
                embed.set_author(
                    name = ctx.author.name,
                    icon_url = ctx.author.avatar_url
                )
            embed.add_field(
                name = 'Limit',
                value = '{} views/hour'.format(self.bot.rate_limit)
            )
            embed.set_footer(
                text = self.bot.footer_text,
                icon_url = self.bot.footer_icon
            )
            await ctx.send(embed = embed)
        else:
            if link == None or not urlparse(link).netloc == 'www.ebay.com':
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = 'Must Include Valid Ebay Link',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = 'Must Include Valid Ebay Link',
                        color = random.choice(self.bot.embed_colors)
                    )
                if self.bot.show_command_author:
                    embed.set_author(
                        name = ctx.author.name,
                        icon_url = ctx.author.avatar_url
                    )
                embed.set_footer(
                    text = self.bot.footer_text,
                    icon_url = self.bot.footer_icon
                )
                await ctx.send(embed = embed)
            elif num_views == None or num_views < 0 or num_views > self.bot.view_limit:
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = 'Must Include Valid Number of Views',
                        description = '*The number must be between 1 and ' + str(self.bot.view_limit) + '.*',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = 'Must Include Valid Number of Views',
                        description = '*The number must be between 1 and ' + str(self.bot.view_limit) + '.*',
                        color = random.choice(self.bot.embed_colors)
                    )
                if self.bot.show_command_author:
                    embed.set_author(
                        name = ctx.author.name,
                        icon_url = ctx.author.avatar_url
                    )
                embed.set_footer(
                    text = self.bot.footer_text,
                    icon_url = self.bot.footer_icon
                )
                await ctx.send(embed = embed)
            else:
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = 'Adding Views...',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = 'Adding Views...',
                        color = random.choice(self.bot.embed_colors)
                    )
                if self.bot.show_command_author:
                    embed.set_author(
                        name = ctx.author.name,
                        icon_url = ctx.author.avatar_url
                    )
                embed.set_footer(
                    text = self.bot.footer_text,
                    icon_url = self.bot.footer_icon
                )
                msg = await ctx.send(embed = embed)

                limited = False
                if self.bot.rate_limit > 0:
                    if not str(ctx.author.id) in self.bot.view_data.keys():
                        self.bot.view_data[str(ctx.author.id)] = {}
                    if not 'last_view_time' in self.bot.view_data[str(ctx.author.id)].keys():
                        self.bot.view_data[str(ctx.author.id)]['last_view_time'] = time.time()
                    elif 'last_view_time' in self.bot.view_data[str(ctx.author.id)].keys() and self.bot.view_data[str(ctx.author.id)]['last_view_time'] + 3600 < time.time():
                        self.bot.view_data[str(ctx.author.id)]['last_view_time'] = time.time()
                    if not 'num_views' in self.bot.view_data[str(ctx.author.id)].keys():
                        self.bot.view_data[str(ctx.author.id)]['num_views'] = 0
                    elif self.bot.rate_limit_type == 'View' and self.bot.view_data[str(ctx.author.id)]['num_views'] + num_views > self.bot.rate_limit and 'last_view_time' in self.bot.view_data[str(ctx.author.id)].keys() and self.bot.view_data[str(ctx.author.id)]['last_view_time'] + 3600 > time.time():
                        num_views = self.bot.rate_limit - self.bot.view_data[str(ctx.author.id)]['num_views']
                        limited = True
                    if self.bot.rate_limit_type == 'View':
                        self.bot.view_data[str(ctx.author.id)]['num_views'] = self.bot.view_data[str(ctx.author.id)]['num_views'] + num_views
                    elif self.bot.rate_limit_type == 'Request':
                        self.bot.view_data[str(ctx.author.id)]['num_views'] = self.bot.view_data[str(ctx.author.id)]['num_views'] + 1

                print(json.dumps(self.bot.view_data, indent = 4))
                start = time.time()
                for i in range(num_views):
                    requests.get(link)
                tot_time = time.time() - start
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = 'Views Added',
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = 'Views Added',
                        color = random.choice(self.bot.embed_colors)
                    )
                if self.bot.show_command_author:
                    embed.set_author(
                        name = ctx.author.name,
                        icon_url = ctx.author.avatar_url
                    )
                if limited:
                    embed.add_field(
                        name = 'Number of Views',
                        value = '{}\n*Cut short by rate limits.*'.format(num_views)
                    )
                else:
                    embed.add_field(
                        name = 'Number of Views',
                        value = num_views
                    )
                embed.add_field(
                    name = 'Total View Time',
                    value = str(round(tot_time, 2)) + ' seconds'
                )
                embed.add_field(
                    name = 'Views per Second',
                    value = '{} views/second'.format(round(tot_time/num_views, 2))
                )
                embed.set_footer(
                    text = self.bot.footer_text,
                    icon_url = self.bot.footer_icon
                )
                msg = await msg.edit(embed = embed)


def setup(bot):
    bot.add_cog(EbayView(bot))
