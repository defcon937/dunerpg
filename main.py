
import random
import discord
import asyncio
from openai import OpenAI
import json

aikey = "..."
discordKey = "..."
client = OpenAI(api_key=aikey)

lock = asyncio.Lock()


modelName = "gpt-4-1106-preview"
# prompttoken = 0.05
# responstoken = 0.15
prompttoken = 0.1
responstoken = 0.3

temperature=0.6
max_tokens=1024*4
frequency_penalty=0.0
money_spent = 0

def getGPT4(ms):
    mspent = 0
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages = ms,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty
    )

    mspent += response.usage.prompt_tokens / 1000 * 0.1
    mspent += response.usage.completion_tokens / 1000 * 0.3

    msg = response.choices[0].message.content

    return [
        mspent, response.choices[0].message
    ]

def getGPT3(ms, mxtk=4096):
    mspent = 0
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages = ms,
        temperature=temperature,
        max_tokens=mxtk,
        frequency_penalty=frequency_penalty
    )

    mspent += response.usage.prompt_tokens / 1000 * 0.05
    mspent += response.usage.completion_tokens / 1000 * 0.15

    msg = response.choices[0].message.content

    return [
        mspent, response.choices[0].message
    ]

async def finish_up_character(ms):
    print("Doing MS", ms)
    money_spent = 0
    ms.append({"role": "user", "content": """PROGRAM: The player has decided they are done. If any data is empty or 0, we must fill it in for them with
    information that sounds like they would have said. Fill in the player data for skills, drives, and eminies. Add any additional information the player
    did not fill out for them so that the data sheet is complete. Add as much detail as possible so we can generate a player data json that is complete and ready
    for play. Correct any fields that may be wrong, such as a choice was selected that doesn't exist. Do not give your response as a json but in paragraph form."""})

    print("Doing call")
    response = getGPT4(ms)

    money_spent += response[0]
    ms.append(response[1])
    print("Filled in Data???", response[1].content)

    ms.append({"role": "assistant", "content": """Generate the updated Player Data json.
    Your entire response must be valid JSON and only show the JSON."""})

    response = getGPT3(ms)

    money_spent += response[0]
    ms.append(response[1])

    msg = response[1].content

    print("JSON:", msg)

    try:
        js = json.loads(msg)
        print("JS lol", js)
    except:
        print("Failed to read JSON")
        js = None

    if js:
        if "CharacterData" not in js:
            ch = js
        else:
            ch = js["CharacterData"]

        if "Name" not in ch or not ch["Name"]:
            ms.append({"role": "assistant", "content": """Generate a name for the player."""})
            response = getGPT3(message)
            money_spent += response[0]
            ms.append(response[1])
            print("Name", response)
        if "Personality" not in ch or not ch["Personality"]:
            ms.append({"role": "assistant", "content": """Generate a Personality for the player."""})
            response = getGPT3(ms)
            money_spent += response[0]
            ms.append(response[1])
            print("per", response)
        if "Appearance" not in ch or not ch["Appearance"]:
            ms.append({"role": "assistant", "content": """Generate a Appearance for the player."""})
            response = getGPT3(ms)
            money_spent += response[0]
            ms.append(response[1])
            print("app", response)
        if "Relationship" not in ch or not ch["Relationship"]:
            ms.append({"role": "assistant", "content": """Generate a Relationship for the player."""})
            response = getGPT3(ms)
            money_spent += response[0]
            ms.append(response[1])
            print("rel", response)
        if "CurrentPlanet" not in ch or not ch["CurrentPlanet"]:
            ms.append({"role": "assistant", "content": """Generate a Current Planet for the player."""})
            response = getGPT3(ms)
            money_spent += response[0]
            ms.append(response[1])
            print("pl", response)
        if "CurrentLocation" not in ch or not ch["CurrentLocation"]:
            ms.append({"role": "assistant", "content": """Generate a Current Location for the player."""})
            response = getGPT3(ms)
            money_spent += response[0]
            ms.append(response[1])
            print("loc", response)
        if "Ambition" not in ch or not ch["Ambition"]:
            ms.append({"role": "assistant", "content": """Generate a Ambition for the player."""})
            response = getGPT3(ms)
            money_spent += response[0]
            ms.append(response[1])
            print("am", response)
        if "DriveStatement" not in ch or not ch["DriveStatement"]:
            ms.append({"role": "assistant", "content": """Generate a Drive Statement for the player."""})
            response = getGPT3(ms)
            money_spent += response[0]
            ms.append(response[1])
            print("ds", response)

        drives = ch["Drives"]
        skills = ch["Skills"]

        for s in skills.keys():
            if skills[s] < 1 or skills[s] > 8:
                skills[s] = random.randint(4, 8)

        ms.append({"role": "assistant", "content": "Skills: " + json.dumps(skills)})

        for s in drives.keys():
            if drives[s] < 1 or drives[s] > 8:
                drives[s] = random.randint(4, 8)

        ms.append({"role": "assistant", "content": "Drives: " + json.dumps(drives)})

        if "SecondaryExpertise" not in ch or ch["SecondaryExpertise"] not in SecondaryExpertise:
            ms.append({"role": "assistant", "content": "Secondary Expertise: " + random.choice(SecondaryExpertise)})

    ms.append({"role": "assistant", "content": """Generate the updated Player Data json.
    Your entire response must be valid JSON and only show the JSON."""})

    response = getGPT3(ms)

    money_spent += response[0]
    ms.append(response[1])

    msg = response[1].content

    print("JSON:", msg)

    return [money_spent, msg]


Houses = [
    "House Corrino"
    "House Harkonnen",
    "House Atreides",
    "Spacing Guild",
    "Order of the Mentats",
    "Bene Gesserit",
    "Suk Medical School",
    "Bene Tleilax",
    "Swordmasters of Ginaz",
    "Fremen"
]

PrimaryExpertise = [
    "ARTISTIC",
    "ESPIONAGE",
    "FARMING",
    "INDUSTRIAL",
    "KANLY",
    "MILITARY",
    "POLITICAL",
    "RELIGION",
    "SCIENCE"
]

SecondaryExpertise = [
    "Machinery",
    "Produce",
    "Expertise",
    "Workers",
    "Understanding"
]

Roles = [
    "RULER",
    "CONSORT",
    "ADVISOR",
    "CHIEF PHYSICIAN",
    "COUNCILOR",
    "ENVOY",
    "HEIR",
    "MARSHAL",
    "SCHOLAR",
    "SPYMASTER",
    "SWORDMASTER",
    "TREASURER",
    "WARMASTER",
]

HatedReason = [
    "COMPETITION",
    "SLIGHT",
    "DEBT",
    "ANCIENT FEUD",
    "MORALITY",
    "SERVITUDE",
    "FAMILY TIES",
    "THEFT",
    "JEALOUSY"
]

Focuses = {
    "Battle": [
        "Assassination",
        "Atomics",
        "Dirty Fighting",
        "Dueling",
        "Evasive Action",
        "Lasgun",
        "Long Blades",
        "Pistols",
        "Rifle",
        "Shield fighting",
        "Short Blades",
        "Sneak Attacks",
        "Strategy",
        "Tactics",
        "Unarmed Combat"
    ],
    "Communicate": [
        "Acting",
        "Bartering",
        "Charm",
        "Deceit",
        "Diplomacy",
        "Disguise",
        "Empathy",
        "Gossip",
        "Innuendo",
        "Inspiration",
        "Interrogation",
        "Intimidation",
        "Linguistics",
        "Listening",
        "Music",
        "Neurolinguistics",
        "Persuasion",
        "Secret Language",
        "Teaching",
    ],
    "Discipline": [
        "Command",
        "Composure",
        "Espionage",
        "Infiltration",
        "Observe",
        "Precision",
        "Resolve",
        "Self-Control",
        "Survival"
    ],
    "Move": [
        "Acrobatics",
        "Body Control",
        "Climb",
        "Dance",
        "Distance Running",
        "Drive",
        "Escaping",
        "Grace",
        "Pilot",
        "Stealth",
        "Swift",
        "Swim",
        "Unobtrusive",
        "Worm Rider"
    ],
    "Understand": [
        "Advanced Technology",
        "Botany",
        "CHOAM Bureaucracy",
        "Cultural Studies",
        "Danger Sense",
        "Data Analysis",
        "Deductive reasoning",
        "Ecology",
        "Emergency Medicine",
        "Etiquette",
        "Faction Lore",
        "Genetics",
        "Geology",
        "House Politics",
        "Imperial Politics",
        "Infectious Diseases",
        "Kanly",
        "Philosophy",
        "Physical Empathy",
        "Physics",
        "Poison",
        "Psychiatry",
        "Religion",
        "Smuggling",
        "Surgery",
        "Traps",
        "Virology"
    ]
}

Archetype = [
    "Analyst",
    "Athlete",
    "Commander",
    "Courtier",
    "Duelist",
    "Empath",
    "Envoy",
    "Herald",
    "Infiltrator",
    "Messenger",
    "Protector",
    "Scholar",
    "Scout",
    "Sergeant",
    "Smuggler",
    "Spy",
    "Steward",
    "Strategist",
    "Tactician",
    "Warrior"
]

Talents = [
    "ADRENALINE SHOT",
    "ADVISOR",
    "BINDING PROMISE",
    "BOLD",
    "BOLSTER",
    "CALCULATED PREDICTION",
    "CAUTIOUS",
    "COLLABORATION",
    "COMBAT MEDIC",
    "CONSTANTLY WATCHING",
    "COOL UNDER PRESSURE",
    "DECISIVE ACTION",
    "DEDICATION",
    "FIND TROUBLE",
    "DELIBERATE MOTION",
    "GUILDSMAN",
    "DIRECT",
    "HIDDEN MOTIVES",
    "DRIVEN",
    "HYPERAWARENESS",
    "DUAL FEALTY",
    "FAILED NAVIGATOR",
    "IMPERIAL CONDITIONING",
    "IMPROVED RESOURCES",
    "MASTERFUL INNUENDO",
    "IMPROVISED WEAPON",
    "MENTAT DISCIPLINE",
    "INTENSE STUDY",
    "MIND PALACE",
    "MAKE HASTE",
    "MASK OF POWER",
    "NIMBLE",
    "MASTER-AT-ARMS",
    "OTHER MEMORY",
    "RANSACK",
    "PASSIVE SCRUTINY",
    "RAPID MANEUVER",
    "PERFORMER",
    "RAPID RECOVERY",
    "PRANA-BINDU CONDITIONING",
    "RESILIENCE",
    "RIGOROUS CONTROL",
    "PRIORITY BOARDING",
    "SPECIALIST",
    "PUTTING THEORY INTO PRACTICE",
    "STIRRING RHETORIC",
    "TWISTED MENTAT",
    "SUBTLE STEP",
    "UNQUESTIONABLE LOYALTY",
    "SUBTLE WORDS",
    "VERIFY",
    "THE REASON I FIGHT",
    "VOICE",
    "THE SLOW BLADE",
    "TO FIGHT SOMEONE IS TO KNOW THEM",
]

def default_create_character(cd):
    message = [{"role": "assistant", "content": """You are the gamemaster for a Dune RPG."""}]

    message.append({"role": "assistant", "content": "Houses: " + json.dumps(Houses)})
    message.append({"role": "assistant", "content": "Primary Expertise: " + json.dumps(PrimaryExpertise)})
    message.append({"role": "assistant", "content": "Secondary Expertise: " + json.dumps(SecondaryExpertise)})
    message.append({"role": "assistant", "content": "Roles: " + json.dumps(Roles)})
    message.append({"role": "assistant", "content": "Hated Reason: " + json.dumps(HatedReason)})
    message.append({"role": "assistant", "content": "Focuses: " + json.dumps(Focuses)})
    message.append({"role": "assistant", "content": "Archetype: " + json.dumps(Archetype)})
    message.append({"role": "assistant", "content": "Talents: " + json.dumps(Talents)})

    message.append({"role": "assistant", "content": 'Player Data: ' + json.dumps(cd)})

    message.append({"role": "user", "content": """PROGRAM: A new player wants to join the game. They are creating a new character. Do not list give simple 1-10 lists when showing a list.

    We can ask them 1-2 questions at a time.

    They need to pick 1 house to join
    they need to pick 1 role
    1 primary Expertise and 1 secondary Expertise
    2 focuses
    2 talent
    1 archetype

    Focus has five categories: Battle, Communicate, Discipline, Move, and Understand. The player should pick 2 of these five categories. From there,
    they should pick 1 focus within each of those categories. The character data skills list the 5 category. If the value is 0, this means it needs
    to be generated. The value should be between 4 and 8. If the player has picked the category, it should be closer to 8. You must use your best
    judgement what the value should be based on what options the player has given.

    To determine the value of drives: each drive should be between 4 and 8, where 4 is least important to their character and 8 is most important.

    To determine the value of Enemy: pick a house which most likely will hate them. Give a good reason why the house would hate this character. The
    amount hate (Hated) should be between 1 and 20 where 1 is disliked and 20 is never sleeps to try and assassinate them.

    Do not let them select a choice that does not exist. If they do, ask them again and suggest a few choices that may be close to their option.
    Make sure to check the list carefully. Make sure to list their options.

    They also need to pick a name then define:
    - their personality,
    - Their ambition
    - relationships
    - title within the house they picked.
    - what planet they are currently at
    - where they are on the planet, maybe it's a city, maybe it's in a forest or desert, maybe it's on a ship in space orbiting the planet.

    From here on out, pretend you are the game master talking directly to the player. The player cannot see this message or any previous messages.
    Do not overload the player by asking for too much at once. Make sure to remind them they are welcome to ask for more information and details about each
    choice.
    Make sure to immerse the player and talk to them like a person who loves Dune. Do not list give simple 1-10 lists when showing a list.

    When you think the player has successfully finished creating their character, reply with a message that just says "FINISHED" to indicate to the program it's ready
    to go to the next stage.

    Do not ask them to define the numbers for drive and skills.

    THE PLAYER CANNOT SEE ANY MESSAGES OR LISTS BEFORE THIS LINE
    ---------
    """})

    return message




# Define intents
intents = discord.Intents.all()
intents.messages = True  # Enable the bot to receive messages

play_state = {}

with open('dunerpg.json', 'r') as file:
    play_state = json.load(file)

if "players" not in play_state:
    play_state["players"] = {}

def generate_player():
    return {
        "ChatData": [],
        "CreatingCharacter": False,
        "Playing": False,
        "RPLastMessage": None,
        "OoCLastMessage": None,
        "CharacterData": {
            "Name": "",
            "Personality": "",
            "Appearance": "",
            "Relationship": "",
            "House": "",
            "PrimaryExpertise": "",
            "SecondaryExpertise": "",
            "HouseTitle": "",
            "CurrentPlanet": "",
            "CurrentLocation": "",
            "Enemy": {
                "House": "",
                "Hated": 0,
                "Reason": ""
            },
            "Archetype": "",
            "Skills": {
                "Battle": 0,
                "Communicate": 0,
                "Discipline": 0,
                "Move": 0,
                "Understand": 0
            },
            "Focuses": [],
            "Talents": [],
            "DriveStatement": "",
            "Ambition": "",
            "Drives": {
                "Duty": 0,
                "Faith": 0,
                "Justice": 0,
                "Power": 0,
                "Truth": 0
            }
        }
    }

async def save(pstate):
    async with lock:
        with open('dunerpg.json', 'w+') as file:
            json.dump(pstate, file, indent=4)

async def send_large_message(channel, message, chunk_size=2000):
    # Ensure the message is a string and escape triple backticks
    message = str(message).replace("```", "\\```")
    
    # Split the message into chunks
    chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
    
    # Send each chunk
    for chunk in chunks:
        await channel.send(chunk)

# Define the bot with intents
discordClient = discord.Client(intents=intents)

@discordClient.event
async def on_ready():
    print(f'We have logged in as {discordClient.user}')

@discordClient.event
async def on_message(message):
    # Check if the message is from the bot itself or not from the target channel
    if message.author == discordClient.user:
        return

    user_id = str(message.author.id)

    if not user_id in play_state["players"]:
        play_state["players"][user_id] = generate_player()
        await save(play_state)

    user_state = play_state["players"][user_id]

    # Respond to the message
    if message.content:
        print(message.author.display_name, message.content)

        # await message.channel.send(f"Hello! You said: {message.content}")
        # ms = [{"role": "assistant", "content": f"""You are the gamemaster for a Dune RPG and are called Shai Hulud. A player named {message.author.display_name} is about to send a message and
        #     we need to know what to do. Your reply should be a 1 word command and you need to pick from the follow choices: Nothing, OutOfCharacter, NewCharacter, Roleplay.
        #     Nothing means you think we should not reply to the message. OutOfCharacter means you think we should banter with the person speaking out of character
        #     because they are not wanting to actually play right now but wants to talk with you. New Character means they are not currently playing the game but
        #     are in the process of creating a character or wants to create a new character. Roleplay means that they are playing and has a character and wants
        #     to do a new action. They MUST have CreatedCharacter = true to do roleplay."""}]
        # ms.append({"role": "assistant", "content": f"Character Data: {user_state['CharacterData']}"})
        # ms.append({"role": "user", "content": message.content})
        
        # r = getGPT3(ms)

        # c = r[1].content

        # print("OC Content:", c)

        # if (c.lower() == "nothing"):
        #     return

        rplm = None
        if "RPLastMessage" in user_state and user_state["RPLastMessage"]:
            rplm = user_state["RPLastMessage"]

        ooclm = None
        if "OoCLastMessage" in user_state and user_state["OoCLastMessage"]:
            ooclm = user_state["OoCLastMessage"]

        if message.channel.id == 1221842748047495210 and user_state["CreatingCharacter"]:
            user_state["ChatData"].append({"role": "user", "content": message.content})
            r1 = getGPT3(user_state["ChatData"])
            user_state["ChatData"].append({"role": "assistant", "content": r1[1].content})
            await save(play_state)

            if ("FINISHED" in r1[1].content):
                print("Doing some crazy workload right now")
                msg = await finish_up_character(user_state["ChatData"])

                try:
                    js = json.loads(msg[1])
                    print("JS lol", js)
                    user_state['CharacterData'] = js
                    user_state['CreatingCharacter'] = False
                    user_state['Playing'] = True
                    user_state["ChatData"] = []
                    await save(play_state)
                    await message.channel.send(f"(You wasted {round(msg[0], 2)} cents)(CC) Your character has been created!")

                    ms = [{"role": "assistant", "content": f"""You are the gamemaster for a Dune RPG and are called Shai Hulud. A player named {message.author.display_name}
                    just created a new character. Welcome the new player, Welcome them to the sand planet and give them a big introduction using information from their character
                    sheet."""}]
                    ms.append({"role": "assistant", "content": f"Character Data: {user_state['CharacterData']}"})
                    r1 = getGPT4(ms)
                    await send_large_message(message.channel, f"(You wasted {round(r1[0], 2)} cents)(InGame) {r1[1].content}")
                except Exception as e:
                    print("Failed to read JSON", e)
                    js = None
            else:
                await message.channel.send(f"(You wasted {round(r1[0], 2)} cents)(CC) {r1[1].content}")

        elif (message.channel.id == 1221842425698586634):
            ms = [{"role": "assistant", "content": f"""You are the gamemaster for a Dune RPG and are called Shai Hulud. A player named {message.author.display_name} is about to send a message
            out of character and needs a reply. Reply in character as the game master and Shai Hulud."""}]
            ms.append({"role": "assistant", "content": f"Character Data: {user_state['CharacterData']}"})
            if ooclm:
                ms.extend(ooclm)
            ms.append({"role": "user", "content": message.content})
            r1 = getGPT3(ms, 1024)
            await send_large_message(message.channel, f"(You wasted {round(r1[0], 2)} cents) (OoC) {r1[1].content}")

            user_state["OoCLastMessage"] = [
                {"role": "user", "content": message.content},
                {"role": "assistant", "content": r1[1].content}
            ]
            await save(play_state)
        elif (message.channel.id == 1221842394442633248):
            ms = [{"role": "assistant", "content": f"""You are the gamemaster for a Dune RPG MUD. A player named {message.author.display_name} is about to send a message
            in characeter and needs a reply. Reply in character as the game master. This is a Discord message so you can use Markdown to enchance the
            text. At the end, you should give the a short list of possible actions the player can take. These actions should be near future actions and
            localized to the specific interaction.
            If the player made an action in his message, you should make a D20 roll. Never tell the player to roll a dice themselves.
            Do not do too much on behalf of the user. Let them choice their own adventure.
            In the style of an old school BASH MUD, List things the player might be able to look at, list things the player might be able to interact with,
            list pepole the player might be able to talk with."""}]
            ms.append({"role": "assistant", "content": f"{message.author.display_name} Character Data: {user_state['CharacterData']}"})
            if rplm:
                ms.extend(rplm)
            ms.append({"role": "user", "content": message.content})
            r1 = getGPT3(ms, 1024)
            await send_large_message(message.channel, f"(You wasted {round(r1[0], 2)} cents) (RP) {r1[1].content}")

            ms.append({"role": "assistant", "content": """The PROGRAM needs to update the user state. Which of the following actions did the user
            just perform? The final output should be in the
            form of a JSON. Summary should be 2-3 sentences about what happened as a result of the player's action. Keep the summary short and include
            critical information that the LLM would need to know for future references.
            Example: \{"Action": "Defeat Enemy", "Description": "Darth Vader has been defeated!", "Summary": "Here is the summary of
            the response that the assistant gave."\}"""})
            r2 = getGPT3(ms, 512)
            print("Progress Type", r2[0], r2[1].content)

            if not rplm:
                rplm = []
            
            rplm.extend([
                {"role": "user", "content": r2[1].content}
            ])

            user_state["RPLastMessage"] = rplm[-20:]

            await save(play_state)
        elif (message.channel.id == 1221842748047495210):
            if not user_state["Playing"]:
                user_state["CreatingCharacter"] = True
                ms = default_create_character(user_state["CharacterData"])
                user_state["ChatData"].extend(ms)
                r1 = getGPT3(ms)
                user_state["ChatData"].append({"role": "assistant", "content": r1[1].content})
                await save(play_state)
                await message.channel.send(f"(You wasted {round(r1[0], 2)} cents)(CC) {r1[1].content}")


discordClient.run(discordKey)
