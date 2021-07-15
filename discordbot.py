import discord
from discord.ext import commands
import re
from carousell import CarousellScraper

client = commands.Bot(command_prefix='.')


def get_listings(item):
    web_page = CarousellScraper(item)
    filtered_web_page = web_page.get_page().find('main', class_=re.compile("D_"))
    return filtered_web_page.select('a[href^="/p"]')


@client.event
async def on_ready():
    print('Bot started')


@client.command(aliases=['list', 'listing', 'ls'])
async def listings(context, *, item):
    results = get_listings(item)
    channel = client.get_channel(856871861110308867)
    for r in results:
        try:
            names = r.select("a > p:nth-of-type(1)")
            name_result = names[0].get_text()
            if len(name_result) >= 140:
                continue
        except IndexError:
            pass
        else:
            prices = r.select("a > p:nth-of-type(2)")
            price_raw = prices[0].get_text().split('S$')
            del price_raw[0]
            price_result = price_raw[0]

            link = r['href']
            hyperlink = f'https://www.carousell.sg{link}'
            embed = discord.Embed(
                title=name_result,
                description=f'Price: ${price_result}\n[Link]({hyperlink})'
            )
            try:
                await channel.send(embed=embed)
            except discord.errors.HTTPException:
                pass


client.run('ODU2ODYwMzAzNjk4Mjk2ODcy.YNHLWA.V4VS1lioAkDrJe24YRvSXBEXJV8')
