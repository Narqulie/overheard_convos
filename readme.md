# Overheard Conversations Bot - README.md

## Overview

The Overheard Conversations Bot is a Python application that crafts short snippets of overheard conversations using OpenAI's GPT-4 model and posts them on Mastodon, a social networking platform. The bot provides a fascinating glimpse into random day-to-day chatter overheard at a café. Sometimes, the conversations might be interrupted by a random "distraction" event.

## Dependencies

- `openai` : To interface with OpenAI's GPT-4 model.
- `mastodon`: To interact with the Mastodon API.
- `logging`: To provide logging functionality.
- Other libraries for handling JSON, system, time, date, and random functions.

## Configuration

For the bot to function properly, you need to create a `config.json` file with the following parameters:

```json
{
    "mastodon_access_token": "<YOUR_MASTODON_ACCESS_TOKEN>",
    "mastodon_base_url": "<YOUR_MASTODON_BASE_URL>",
    "openai_api_key": "<YOUR_OPENAI_API_KEY>",
    "max_tokens": <MAX_TOKENS>,
    "temperature": <TEMPERATURE_VALUE>,
    "min_post_interval": <MIN_INTERVAL_IN_SECONDS>,
    "max_post_interval": <MAX_INTERVAL_IN_SECONDS>
}
```

Replace the placeholder values with appropriate values.

## Features

1. **Customizable Overheard Prompt**: The bot uses a prompt to craft conversations, simulating what you might overhear in a cafe setting.
2. **Distractions**: Sometimes, the bot will simulate being "distracted" by inserting a random event, like "A baby cries loudly" or "Someone spills their drink on your table".
3. **Logging**: The bot logs all its activities, including the messages it generates, to `overheard_convos.log` and to the console.
4. **Automated Posting**: The bot will automatically post the crafted conversations to Mastodon at random intervals.

## Functions

- `clear_screen()`: Clears the console.
- `print_banner()`: Prints a decorative banner on the console.
- `get_models()`: Lists available models from OpenAI.
- `openai_overhear()`: Crafts a conversation using OpenAI's GPT-4 model.
- `get_distracted(overheard)`: Adds a random distraction to the overheard conversation.
- `post_toot(text)`: Posts the generated text to Mastodon.

## Running the bot

Ensure you have the necessary dependencies installed and the configuration file set up.

To run the bot:

```
python <FILENAME>.py
```

Replace `<FILENAME>` with the name you saved the script as.

## Important Notes

1. Ensure that the `config.json` file is present in the same directory as the bot script.
2. Make sure you have a valid Mastodon access token and OpenAI API key to use the bot.

## Disclaimer

The bot crafts conversations using GPT-4's model, which means the conversations are entirely fictional and any resemblance to real-life conversations or events is purely coincidental.

---

Happy overhearing! 🗣👂