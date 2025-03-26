import discord
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Price list
prices = {
    "ssk": 15,
    "aizen": 100,
    "elbs": (60, 80)  # Elbs has a price range
}

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def trade(ctx, *items):
    items = [item.lower() for item in items]

    if "for" not in items:
        await ctx.send("❌ Incorrect format! Use: `!trade ssk aizen for elbs`")
        return

    index_for = items.index("for")
    offer_items = items[:index_for]  # Items being offered
    target_item = items[index_for + 1]  # Item the user wants

    total_offer_value = sum(prices.get(item, 0) for item in offer_items)

    if isinstance(prices.get(target_item, 0), tuple):
        min_value, max_value = prices[target_item]
        target_value = (min_value + max_value) / 2
    else:
        target_value = prices.get(target_item, 0)

    response = "**Trade Breakdown:**\n"
    for item in offer_items:
        response += f"- {item.capitalize()}: {prices.get(item, 0)} Lbs\n"

    response += f"**Total offered: {total_offer_value} Lbs**\n"
    response += f"**{target_item.capitalize()} value: {target_value} Lbs**\n"

    if total_offer_value > target_value:
        ratio = round(total_offer_value / target_value, 2)
        response += f"🚀 **You are overpaying!** {total_offer_value}:{target_value} ≈ **{ratio}x**\n"
    elif total_offer_value < target_value:
        ratio = round(target_value / total_offer_value, 2)
        response += f"📉 **You are underpaying!** {total_offer_value}:{target_value} ≈ **{ratio}x**\n"
    else:
        response += "✅ **Fair trade!**\n"

    await ctx.send(response)

# Run bot (Replace with your token)
bot.run("TOKEN")
