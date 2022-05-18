import json
import random
from discord.ext import commands
from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

from marsbots_core.resources.discord_utils import get_discord_messages


class ViperCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.data = self.load_data()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = np.load("embeddings.npy")

    def load_data(self) -> dict:
        with open("albums.json", "r") as f:
            data = json.load(f)
        return data

    def get_largest_image(self, images):
        return images[np.argmax([d["height"] for d in images])]

    def get_image_url_for_query(self, query):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=1)
        idx = top_results[1][0].item()
        album = self.data[idx]
        image = self.get_largest_image(album["images"])
        image_url = image["url"]
        name = album["name"]
        return image_url, name

    @commands.command()
    async def viper(
        self,
        ctx: commands.context,
        n_messages: int = 5,
    ) -> None:
        n_messages = int(n_messages)
        messages = await get_discord_messages(ctx.channel, n_messages)
        query = " ".join([m.content for m in messages])
        image_url, name = self.get_image_url_for_query(query)
        await ctx.send(f"**{name}**\n\n{image_url}")

    @commands.command()
    async def viper_ask(self, ctx: commands.context, *prompt) -> None:
        query = " ".join(prompt)
        image_url, name = self.get_image_url_for_query(query)
        await ctx.send(f"**{name}**\n\n{image_url}")

    @commands.command()
    async def viper_random(self, ctx):
        r = random.choice(self.data)
        image = self.get_largest_image(r["images"])
        image_url, name = image["url"], r["name"]
        await ctx.send(f"**{name}**\n\n{image_url}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ViperCog(bot))
