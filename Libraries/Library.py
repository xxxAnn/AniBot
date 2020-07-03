import json


def get_guild_language(guild_id: str):
    with open('data/settings.json', 'r') as file:
        content = file.read()
        settings = json.loads(content)
        if guild_id in settings:
            return settings[str(guild_id)]['Language']
        else:
            return settings[str(guild_id)]['Language']
