import openai
from mastodon import Mastodon
import logging
import time
import json
import sys
from datetime import datetime, timedelta
import os
import random

# Logging
logging.basicConfig(filename='overheard_convos.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
# Create a handler for stdout (standard output)
stdout_handler = logging.StreamHandler(sys.stdout)
# Add the stdout handler to the root logger
logging.getLogger().addHandler(stdout_handler)


# Read config
try:
    with open('config.json') as f:
        config = json.load(f)

        mastodon_access_token = config['mastodon_access_token']
        mastodon_base_url = config['mastodon_base_url']
        openai_api_key = config['openai_api_key']
        openai_max_tokens = config['max_tokens']
        openai_temperature = config['temperature']
        min_post_interval = config['min_post_interval']
        max_post_interval = config['post_interval']
except Exception as e:
    logging.error(e)
    exit()

openai_prompt = """
Overheard at a cafe:
Craft a short snippet of a conversation involving 2 to 4 individuals.
Describe each participant with simple, everyday characteristics rather
than names (e.g., "a young mother," "an elderly man reading a newspaper").
The dialogue can capture the essence of ordinary life: a casual remark,
a shared observation, or a common concern.
There's limited context, and while the tone can range from light to serious,
keep it grounded in day-to-day reality.
The conversation doesn't need a clear start or end.
Stay within a 500 character limit.
"""

# OpenAI setup
openai.api_key = openai_api_key
openai.prompt = openai_prompt
# openai.max_tokens = openai_max_tokens
openai.temperature = openai_temperature

# Mastodon API setup
m = Mastodon(access_token=mastodon_access_token,
             api_base_url=mastodon_base_url)

# Variables
post_count = 1

distractions = [
    "A glass shatters on the floor.",
    "A baby cries loudly.",
    "A barista drops a tray of drinks.",
    "Laughter erupts from a nearby table.",
    "Someone's phone alarm goes off loudly.",
    "The café's fire alarm sounds.",
    "A dog barks aggressively at a passerby.",
    "A street performer starts playing a loud instrument outside.",
    "A car alarm blares just outside the window.",
    "Someone spills their drink on your table.",
    "A group of teenagers yell in excitement.",
    "The power cuts out, plunging the cafe into darkness.",
    "A balloon pops.",
    "Someone sneezes loudly without covering their mouth.",
    "A chair scrapes loudly against the floor.",
    "Sirens wail from a passing emergency vehicle.",
    "A bird flies into the café, fluttering about.",
    "The café's music volume suddenly increases.",
    "A couple starts a heated argument nearby.",
    "A heavy bag thuds as someone drops it.",
    "A motorbike revs loudly just outside.",
    "A person trips, sending a tray of food flying.",
    "The clang of pots and pans resonates from the kitchen.",
    "An announcement comes over the café's PA system.",
    "Someone shouts your name unexpectedly.",
    "A cat jumps onto a table, knocking over a vase.",
    "A group starts singing 'Happy Birthday' loudly.",
    "A waiter slips, sending plates crashing.",
    "The sound of a distant thunderstorm grows closer.",
    "A blender whirs loudly, drowning out other noises.",
    "Someone starts playing a harmonica at the next table.",
    "A phone rings repeatedly without being answered.",
    "Children run past, playing tag.",
    "A loud beep indicates a low battery on someone's laptop.",
    "A coffee machine steams loudly.",
    "A door slams shut from a gust of wind.",
    "A patron loudly complains about their order.",
    "A musician begins tuning their guitar nearby.",
    "Someone drops a stack of magazines with a rustle.",
    "A coffee cup overflows, creating a small flood on the counter.",
    "A child's balloon escapes, floating to the ceiling.",
    "The smell of burnt toast fills the air.",
    "A loud crash comes from the kitchen.",
    "Someone's headphones leak music, playing a catchy tune.",
    "A person loudly exclaims as they find a lost item.",
    "The barista calls out a complex order repeatedly.",
    "A nearby laptop plays a movie trailer at full volume.",
    "A scooter skids and crashes outside the window.",
    "Someone nearby starts a video call without headphones.",
    "The café's Wi-Fi goes down, causing a collective groan."
]


# Functions
# --- Clear screen ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# --- Print banner ---
def print_banner():
    banner = """
   ___                          __                                  __
 .'   `.                       [  |                                |  ]
/  .-.  \ _   __  .---.  _ .--. | |--.  .---.  ,--.   _ .--.   .--.| |
| |   | |[ \ [  ]/ /__\\[ `/'`\]| .-. |/ /__\\`'_\ : [ `/'`\]/ /'`\' |
\  `-'  / \ \/ / | \__., | |    | | | || \__.,// | |, | |    | \__/  |
 `.___.'   \__/   '.__.'[___]  [___]|__]'.__.'\'-;__/[___]    '.__.;__]
   ______
 .' ___  |
/ .'   \_|  .--.   _ .--.  _   __   .--.   .--.
| |       / .'`\ \[ `.-. |[ \ [  ]/ .'`\ \( (`\]
\ `.___.'\| \__. | | | | | \ \/ / | \__. | `'.'.
 `.____ .' '.__.' [___||__] \__/   '.__.' [\__) )
    """
    print(banner)


def get_models():
    models = openai.Model.list()
    print(models)


# --- Get weather overheard from OpenAI ---
def openai_overhear():
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                  "content": openai_prompt}],
        max_tokens=int(openai_max_tokens))
    overheard = completion.choices[0].message.content
    logging.info(overheard)
    logging.info(len(overheard))
    print(len(overheard))
    return overheard


def get_distracted(overheard):
    # Get random distraction
    distraction = random.choice(distractions)
    logging.info(distraction)
    logging.info(len(distraction))
    # Get position in overhead to insert distraction; 500 - len of distraction.
    position = 495 - len(distraction)
    logging.info(position)
    # Insert distraction into overheard
    to_post = overheard[:position] + " ... " + distraction
    logging.info(to_post)
    logging.info(len(to_post))
    return to_post


# --- Post to Mastodon ---
def post_toot(text):
    # last check of lentgh:
    if len(text) > 500:
        logging.info("overheard too long, cancelling send")
        return
    else:
        m.toot(text)


def main():
    while True:
        try:
            # Initiate cli screen
            global post_count
            clear_screen()
            post_time = datetime.now()
            logging.info("Starting Overheard Conversations")
            print_banner()
            logging.info(f"Post number: {post_count}")

            # Get Overheard Conversation
            logging.info("Getting conversation")
            overheard = openai_overhear()

            # Check the length of the overheard and cut:
            if len(overheard) > 500:
                logging.info("overheard too long, cutting to 500 characters")
                to_post = get_distracted(overheard)

            # Post Overheard Conversation
            logging.info("Posting conversation")
            try:
                logging.info("%d", len(to_post))
                logging.info("Posting to Mastodon")
                post_toot(to_post)
            except Exception as e:
                logging.error(e)
                continue

            logging.info("Post completed")
            post_count += 1
            logging.info(post_time)

            # Generate a random interval between min and max post interval
            random_interval = random.randint(min_post_interval,
                                             max_post_interval)
            next_post_time = post_time + timedelta(seconds=random_interval)
            logging.info(f"Sleeping for {random_interval} seconds until {next_post_time}")
            time.sleep(random_interval)

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(random_interval)


if __name__ == "__main__":
    main()
