module.exports = {
  apps: [
    {
      name: "viper",
      script: "../../bot.py",
      interpreter: "python",
      args: "./viperbot.json --cog-path=bots.viperbot.viperbot --dotenv-path=.env",
      watch: ["."],
      ignore_watch: ["__pycache__", "*.pyc"],
      watch_delay: 1000
    },
  ],
};
