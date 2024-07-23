import json
import os
import random
import time

# ^Imports the necessary libraries


# Helper function to print with delay for dramatic effect
def delay_print(text, delay=1):
    print(text)
    time.sleep(delay)


# Define the game state
def start_game():
    global game_state
    game_state = {
        "player": {
            "name": "Player",
            "hp": 100,
            "weapon": "Greatsword",
            "inventory": {
                "Potion": {
                    "quantity": 5,
                    "effect": {
                        "heal": 25
                    }
                },
                "Egg": {},
            },
            "location": "Mahana Village",
            "monsties": {},
            "hearts": 3,
            "zenny": 0,
            "resources": {},  # <--- Will track gathered resources
            "level": 1,
            "exp": 0,
            "attack": 9,
            "defense": 10,
        },
        "quests": {
            "[Tutorial]: Get a Monstie egg and hatch it at the Stables.": {
                "status": "Available",
                "type": "Gathering",
                "target": "Herb",
                "quantity": 5,
                "reward": {
                    "zenny": 100,
                    "item": "Potion",
                    "quantity": 1
                }
            },
            "[Easy]: Hunt a Velocidrome.": {
                "status": "Available",
                "type": "Hunt",
                "target": "Velocidrome",
                "quantity": 1,
                "reward": {
                    "zenny": 200,
                    "item": "Herb",
                    "quantity": 2
                }
            }
        },
        "characters": {
            "Navirou": {
                "dialogue": [
                    "Looks like there might be some Monstie Eggs around!",
                    "I wanna eat a Mahana Dunker... Uug..."
                ]
            },
            "Ena": {
                "dialogue": [
                    "This is a special egg. Guardian Ratha gave me it.",
                    "You have potential. Use it to your advantage."
                ]
            },
            "Lilia": {
                "dialogue": [
                    "Welcome back, Rider! What can I do for you today?",
                    "I miss the old times when I lived in Hakum Village..."
                ]
            },
            "Kayna": {
                "dialogue": [
                    "Watch out there, newbie! Monsters can be quite dangerous.",
                    "I heard there's a new threat in the forest. Be careful, newbie!"
                ]
            },
            "Alwin": {
                "dialogue": [
                    "I see you've been busy. Your skills are improving!",
                    "There's a powerful monster spotted near Lamure. Be prepared!"
                ]
            }
        },
        "locations": {
            "Mahana Village": {
                "description":
                ("The bustling Mahana Village. Here you'll find the Market, "
                 "the Smithy, the Melynx Inc., and your house."),
                "exits": {
                    "North": "Field",
                    "East": "Kamuna Forest"
                },
                "actions": {
                    "Market": 'market',
                    "Smithy": 'smithy',
                    "Melynx Inc.": 'melynx',
                    "House": 'house'
                }
            },
            "Kamuna Forest": {
                "description":
                ("The dense forest surrounding the Hakolo archipelago. "
                 "Wild monsters roam here."),
                "exits": {
                    "West": "Mahana Village"
                },
                "actions": {
                    "Explore": 'explore_kamuna_forest',
                    "Gather": 'gather_kamuna_forest'
                }
            },
            "Alcala": {
                "description":
                ("A region known for its ancient ruins and dangerous monsters."
                 ),
                "exits": {
                    "West": "",
                    "South": "Lamure"
                },
                "actions": {
                    "Explore": 'explore_alcala',
                    "Gather": 'gather_alcala'
                }
            },
            "Lamure": {
                "description":
                "A snowy area home to monsters like the Gammoth.",
                "exits": {
                    "North": "Alcala",
                    "East": "Pomore Garden"
                },
                "actions": {
                    "Explore": 'explore_lamure',
                    "Gather": 'gather_lamure'
                }
            },
            "Pomore Garden": {
                "description":
                "Known for its beautiful flora and rare monsters.",
                "exits": {
                    "West": "Lamure"
                },
                "actions": {
                    "Explore": 'explore_pomore_garden',
                    "Visit Flower Field": 'visit_flower_field',
                    "Gather": 'gather_pomore_garden'
                }
            },
            "Field": {
                "description": "A grassy field.",
                "exits": {
                    "South": "Mahana Village"
                },
                "actions": {
                    "Gather": 'gather_field'
                }
            }
        },
        "monsters": {
            "Aptonoth": {
                "name": "Aptonoth",
                "hp": 20,
                "attacks": ["Body Slam", ""],
                "type": "Herbivore",
                "kinship_skill": "Tail Swipe",
                "skills": ["Tail Swipe", "Sonic Pounce"]
            },
            "Velociprey": {
                "name": "Velociprey",
                "hp": 30,
                "attacks": ["Double Jump Kick", "Charge"],
                "type": "Bird Wyvern",
                "kinship_skill": "Sonic Pounce",
                "skills": ["Double Jump Kick", "Charge"]
            },
            "Velocidrome": {
                "name": "Velocidrome",
                "hp": 35,
                "attacks": ["Claw Swipe", "Double Jump Kick"],
                "type": "Bird Wyvern",
                "kinship_skill": "Razor Talon",
                "skills": ["Claw Swipe", "Double Jump Kick"]
            },
            "Kulu-Ya-Ku": {
                "name": "Kulu-Ya-Ku",
                "hp": 45,
                "attacks": ["Rock Throw", "Peck"],
                "type": "Bird Wyvern",
                "kinship_skill": "Boulder Bash",
                "skills": ["Rock Throw", "Peck"]
            },
            "Yian Kut-Ku": {
                "name": "Yian Kut-Ku",
                "hp": 40,
                "attacks": ["Fireball", "Rock Breaker"],
                "type": "Bird Wyvern",
                "kinship_skill": "Fire Blast",
                "skills": ["Fireball", "Rock Breaker"]
            },
            "Bulldrome": {
                "name": "Bulldrome",
                "hp": 35,
                "attacks": ["Charge", "Tackle"],
                "type": "Fanged Beast",
                "kinship_skill": "Horn Charge",
                "skills": ["Charge", "Tackle"]
            },
            "Pukei-Pukei": {
                "name": "Pukei-Pukei",
                "hp": 42,
                "attacks": ["Tongue Whip", "Toxic Throw"],
                "type": "Bird Wyvern",
                "kinship_skill": "Toxic Breath",
                "skills": ["Tongue Whip", "Toxic Throw"]
            },
            "Apceros": {
                "name": "Apceros",
                "hp": 30,
                "attacks": ["Tail Whip", "Body Slam"],
                "type": "Herbivore",
                "kinship_skill": "Stomp",
                "skills": ["Tail Whip", "Body Slam"]
            },
            "Slagtoth": {
                "name": "Slagtoth (Green)",
                "hp": 32,
                "attacks": ["Stomp", "Body Slam"],
                "type": "Herbivore",
                "kinship_skill": "Mud Bomb",
                "skills": ["Stomp", "Body Slam"]
            },
            "Royal Ludroth": {
                "name": "Royal Ludroth",
                "hp": 48,
                "attacks": ["Water Bomb", "Charge"],
                "type": "Leviathan",
                "kinship_skill": "Water Cannon",
                "skills": ["Water Bomb", "Charge"]
            },
            "Arzuros": {
                "name": "Arzuros",
                "hp": 34,
                "attacks": ["Claw Swipe", "Body Slam"],
                "type": "Fanged Beast",
                "kinship_skill": "Roar",
                "skills": ["Claw Swipe", "Body Slam"]
            },
            "Paolumu": {
                "name": "Paolumu",
                "hp": 38,
                "attacks": ["Air Strike", "Bite"],
                "type": "Flying Wyvern",
                "kinship_skill": "Wind Blast",
                "skills": ["Air Strike", "Bite"]
            },
            "Nargacuga": {
                "name": "Nargacuga",
                "hp": 50,
                "attacks": ["Spike Tail", "Claw Slash"],
                "type": "Flying Wyvern",
                "kinship_skill": "Shadow Claw",
                "skills": ["Spike Tail", "Claw Slash"]
            },
            "Rathian": {
                "name": "Rathian",
                "hp": 52,
                "attacks": ["Tail Whip", "Fireball"],
                "type": "Flying Wyvern",
                "kinship_skill": "Fire Breath",
                "skills": ["Tail Whip", "Fireball"]
            },
            "Gypceros": {
                "name": "Gypceros",
                "hp": 55,
                "attacks": ["Beak Smash", "Poisonous Venom"],
                "type": "Bird Wyvern",
                "kinship_skill": "Venom Spit",
                "skills": ["Beak Smash", "Poisonous Venom"]
            },
            "Zamtrios": {
                "name": "Zamtrios",
                "hp": 59,
                "attacks": ["Wave Splash", "Charge"],
                "type": "Amphibian",
                "kinship_skill": "Ice Wave",
                "skills": ["Wave Splash", "Charge"]
            },
            "Khezu": {
                "name": "Khezu",
                "hp": 62,
                "attacks": ["Spark", "Electric Jolt"],
                "type": "Flying Wyvern",
                "kinship_skill": "Lightning Strike",
                "skills": ["Spark", "Electric Jolt"]
            },
            "Lagombi": {
                "name": "Lagombi",
                "hp": 58,
                "attacks": ["Bite", "Claw Swipe"],
                "type": "Fanged Beast",
                "kinship_skill": "Snowball",
                "skills": ["Bite", "Claw Swipe"]
            },
            "Anjanath": {
                "name": "Anjanath",
                "hp": 64,
                "attacks": ["Stomp", "Bite"],
                "type": "Brute Wyvern",
                "kinship_skill": "Fire Breath",
                "skills": ["Stomp", "Bite"]
            },
            "Barioth": {
                "name": "Barioth",
                "hp": 62,
                "attacks": ["Fangs", "Ice Shard"],
                "type": "Flying Wyvern",
                "kinship_skill": "Ice Blast",
                "skills": ["Fangs", "Ice Shard"]
            },
            "Legiana": {
                "name": "Legiana",
                "hp": 60,
                "attacks": ["Ice Shard", "Icicle Barrage"],
                "type": "Flying Wyvern",
                "kinship_skill": "Frost Breath",
                "skills": ["Ice Shard", "Icicle Barrage"]
            },
            "Diablos": {
                "name": "Diablos",
                "hp": 64,
                "attacks": ["Horn Toss", "Tail Whip"],
                "type": "Flying Wyvern",
                "kinship_skill": "Earth Quake",
                "skills": ["Horn Toss", "Tail Whip"]
            },
            "Mizutsune": {
                "name": "Mizutsune",
                "hp": 58,
                "attacks": ["Bubble Barrage", "Claw Swipe"],
                "type": "Leviathan",
                "kinship_skill": "Water Bubble",
                "skills": ["Bubble Barrage", "Claw Swipe"]
            },
            "Lagiacrus": {
                "name": "Lagiacrus",
                "hp": 56,
                "attacks": ["Spark", "Jet Stream"],
                "type": "Leviathan",
                "kinship_skill": "Lightning Blast",
                "skills": ["Spark", "Jet Stream"]
            },
            "Kirin": {
                "name": "Kirin",
                "hp": 62,
                "attacks": ["Electric Jolt", "Charge"],
                "type": "Elder Dragon",
                "kinship_skill": "Thunderbolt",
                "skills": ["Electric Jolt", "Charge"]
            }
        },
        "common_eggs": [
            "Velocidrome", "Kulu-Ya-Ku", "Yian Kut-Ku", "Apceros", "Arzuros",
            "Paolumu", "Zamtrios", "Lagiacrus"
        ],
        "rare_eggs": [
            "Pukei-Pukei", "Royal Ludroth", "Nargacuga", "Rathian", "Khezu",
            "Anjanath", "Barioth", "Legiana", "Mizutsune", "Kirin"
        ]
    }


# Save and load functions
def save_game():
    with open('MHST2_save.json', 'w') as file:
        json.dump(game_state, file, indent=4)
    delay_print("Game saved successfully!")


def load_game():
    global game_state
    if os.path.exists('MHST2_save.json'):
        with open('MHST2_save.json', 'r') as file:
            game_state = json.load(file)
        delay_print("Game loaded successfully!")
    else:
        delay_print("No saved game found. Starting a new game.")


# Define use_item function
def use_item(item_name):
    """
    Placeholder function for using an item.
    This function should be implemented based on the game's logic.
    """
    delay_print(f"You use the {item_name}.")
    if item_name == "Potion":

        def heal(player):  # Pass player as an argument
            player["hp"] += 15
            delay_print("You healed yourself using a Potion for 15 HP.")

        heal(game_state["player"])  # Call heal and pass the player dictionary
        pass


# Define combat functions
def battle_monster(monster):
    player_hp = game_state["player"]["hp"]
    monster_hp = monster["hp"]
    delay_print(f"You are fighting a wild {monster['name']}!")
    while player_hp > 0 and monster_hp > 0:
        delay_print(f"\nYour HP: {player_hp}")
        delay_print(f"{monster['name']}'s HP: {monster_hp}")
        delay_print("Choose an action:")
        delay_print("1. Attack")
        delay_print("2. Use Item")
        delay_print("3. Use Skill")  # Added skill option
        if game_state["player"]["monsties"]:
            delay_print("4. Use Kinship Skill")  # Added kinship skill option
        choice = input("Enter your choice: ")
        if choice == '1':
            damage = random.randint(game_state["player"]["attack"],
                                    game_state["player"]["attack"] + 10)
            monster_hp -= damage
            delay_print(
                f"You attack the {monster['name']} and deal {damage} damage.")
        elif choice == '2':
            item_name = input("Enter the item name to use: ")
            use_item(item_name)
        elif choice == '3':
            if game_state["player"]["monsties"]:
                monstie_id = list(game_state["player"]["monsties"].keys())[
                    0]  # Assuming only one Monstie for now
                monstie = game_state["player"]["monsties"][monstie_id]
                delay_print(f"Available Skills for {monstie['name']}:")
                for i, skill in enumerate(monstie["skills"]):
                    delay_print(f"{i+1}. {skill}")
                skill_choice = int(input("Choose a skill: "))
                if 1 <= skill_choice <= len(monstie["skills"]):
                    chosen_skill = monstie["skills"][skill_choice - 1]
                    kinship_cost = 20  # Example cost
                    if monstie["kinship_gauge"] >= kinship_cost:
                        monstie["kinship_gauge"] -= kinship_cost
                        damage = random.randint(25, 40)  # Example damage
                        monster_hp -= damage
                        delay_print(
                            f"You used {chosen_skill}! "
                            f"The {monster['name']} took {damage} damage.")
                    else:
                        delay_print(
                            f"Not enough Kinship Gauge to use {chosen_skill}.")
                else:
                    delay_print("Invalid choice.")
            else:
                delay_print("You don't have a Monstie to use skills.")
        elif choice == '4' and game_state["player"]["monsties"]:
            monstie_id = list(game_state["player"]["monsties"].keys())[0]
            monstie = game_state["player"]["monsties"][monstie_id]
            if monstie["kinship_gauge"] >= 100:
                kinship_skill = monstie["kinship_skill"]
                damage = random.randint(35, 60)  # Example damage
                monster_hp -= damage
                delay_print(
                    f"You unleashed {kinship_skill}! The {monster['name']} "
                    f"took {damage} damage.")
                monstie["kinship_gauge"] = 0
            else:
                delay_print("Kinship Gauge is not full.")
        else:
            delay_print("Invalid choice. You missed your turn.")

        if monster_hp > 0:
            monster_attack = random.choice(monster['attacks'])
            damage = random.randint(5, 15)
            player_hp -= damage
            delay_print(f"The {monster['name']} attacks with "
                        f"{monster_attack} and deals {damage} damage.")

        if player_hp <= 0:
            game_state["player"]["hearts"] -= 1
            delay_print(f"You lost a heart! You have "
                        f"{game_state['player']['hearts']} hearts left.")
            if game_state["player"]["hearts"] == 0:
                delay_print(
                    "You have no hearts left! Returning to the last location..."
                )
                return
            else:
                player_hp = 100  # Player revives
                delay_print(
                    f"You return to your last location with {player_hp} HP.")

        if monster_hp <= 0:
            game_state["player"]["hearts"] -= 1
            delay_print("Your Monstie fainted! You have "
                        f"{game_state['player']['hearts']} hearts left.")

            if game_state["player"]["hearts"] == 0:
                delay_print(
                    "You have no hearts left! Returning to the last location..."
                )
                return
            else:
                monster_hp = monster["hp"]  # Monster revives
                delay_print("The monster returns to its location with "
                            f"{monster_hp} HP.")

        if game_state["player"]["monsties"]:
            for monstie in game_state["player"]["monsties"].values():
                monstie["kinship_gauge"] += 10
                if monstie["kinship_gauge"] >= 100:
                    delay_print(f"{monstie['name']}'s Kinship Gauge is full!")
                    # Add logic to allow the player to use the kinship skill
                    delay_print(
                        f"You use {monstie['Aptonoth']}'s Kinship Skill: "
                        f"{monstie['kinship_skill']}!")

                    # Implement logic for using the kinship skill based on the skill.
                    if monstie["kinship_skill"] == "Slip 'n' Slam":
                        # Deal extra damage to the monster
                        monster_hp -= 15
                        delay_print(
                            f"{monstie['Aptonoth']} uses Slip 'n' Slam, "
                            f"dealing 15 damage!")
                    # ... other kinship skills and their effects
                    # ... WIP XD
                    monstie["kinship_gauge"] = 0


# Define location and action functions
def market():
    while True:
        delay_print("\n=== Market ===")
        delay_print("1. Buy Potions (10 Zenny each)")
        delay_print("2. Sell Items (WIP)")
        delay_print("3. Return to Village")
        choice = input("Choose an option: ")
        if choice == '1':
            delay_print(
                "You buy potions and other supplies necessary for your journey."
            )
            quantity = int(input("How many Potions would you like to buy? "))
            cost = quantity * 10
            if cost > game_state["player"]["zenny"]:
                quantity = game_state["player"]["zenny"] // 10
                delay_print(f"You can only afford {quantity} Potions.")
            game_state["player"]["inventory"]["Potion"]["quantity"] += quantity
            game_state["player"]["zenny"] -= cost
            delay_print(f"You bought {quantity} Potions!")
        elif choice == '2':
            sell_items()
        elif choice == '3':
            break
        else:
            delay_print("Invalid choice, please try again.")


def smithy():
    while True:
        delay_print("\n=== Smithy ===")
        delay_print("1. Forge Weapons (WIP)")
        delay_print("2. Upgrade gear (WIP)")
        delay_print("3. Sell items (WIP)")
        delay_print("4. Return to Village")
        choice = input("Choose an option: ")
        if choice == '1':
            forge_gear()
        elif choice == '2':
            upgrade_gear()
        elif choice == '3':
            sell_items()
        elif choice == '4':
            break
        else:
            delay_print("Invalid choice, please try again.")


def forge_gear():
    delay_print("Which gear would you like to forge? (WIP)")
    # Implement forging logic here
    while True:
        delay_print("\n=== Forge Menu ===")
        delay_print("1. Forge Greatsword (Requires: 10 Iron Ore, 50 Zenny)")
        delay_print("2. Forge Hammer (Requires: 15 Iron Ore, 60 Zenny)")
        delay_print("3. Forge Bow (Requires: 12 Iron Ore, 55 Zenny)")
        delay_print("4. Return to Smithy")
        choice = input("Choose an option: ")
        if choice == '1':
            resources = game_state["player"]["resources"]
            zenny = game_state["player"]["zenny"]

            if resources.get("Iron Ore", 0) >= 10 and zenny >= 50:
                game_state["player"]["resources"]["Iron Ore"] -= 10
                game_state["player"]["zenny"] -= 50
                delay_print("You forged a Greatsword!")
            else:
                delay_print("You don't have enough materials or Zenny.")
        elif choice == '2':
            iron_ore = game_state["player"]["resources"].get("Iron Ore", 0)
            zenny = game_state["player"]["zenny"]

            if iron_ore >= 15 and zenny >= 60:
                game_state["player"]["resources"]["Iron Ore"] -= 15
                game_state["player"]["zenny"] -= 60
                delay_print("You forged a Hammer!")
            else:
                delay_print("You don't have enough materials or Zenny.")
        elif choice == '3':
            resources = game_state["player"]["resources"]
            iron_ore = resources.get("Iron Ore", 0)
            zenny = game_state["player"]["zenny"]

            if iron_ore >= 12 and zenny >= 55:
                game_state["player"]["resources"]["Iron Ore"] -= 12
                game_state["player"]["zenny"] -= 55
                delay_print("You forged a Bow!")
            else:
                delay_print("You don't have enough materials or Zenny.")
        elif choice == '4':
            break
        else:
            delay_print("Invalid choice, please try again.")


def upgrade_gear():
    delay_print("Which gear would you like to upgrade? (WIP)")
    # Implement upgrading logic here
    while True:
        delay_print("\n=== Upgrade Menu ===")
        delay_print("1. Upgrade Greatsword (Requires: 5 Iron Ore, 20 Zenny)")
        delay_print("2. Upgrade Hammer (Requires: 7 Iron Ore, 25 Zenny)")
        delay_print("3. Upgrade Bow (Requires: 6 Iron Ore, 22 Zenny)")
        delay_print("4. Return to Smithy")
        choice = input("Choose an option: ")
        if choice == '1':
            player_resources = game_state["player"]["resources"]
            player_zenny = game_state["player"]["zenny"]

            has_enough_iron_ore = player_resources.get("Iron Ore", 0) >= 5
            has_enough_zenny = player_zenny >= 20

            if has_enough_iron_ore and has_enough_zenny:
                # Resources and Zenny are suficient?
                game_state["player"]["resources"]["Iron Ore"] -= 5
                game_state["player"]["zenny"] -= 20
                # If yes, then...
                delay_print("You upgraded your Greatsword!")
            else:
                # If no, then...
                delay_print("You don't have enough materials or Zenny.")
        elif choice == '2':
            player_resources = game_state["player"]["resources"]
            player_zenny = game_state["player"]["zenny"]

            iron_ore = player_resources.get("Iron Ore", 0)
            has_sufficient_resources = iron_ore >= 7
            has_sufficient_zenny = player_zenny >= 25

            if has_sufficient_resources and has_sufficient_zenny:
                # Resources and Zenny are suficient?
                game_state["player"]["resources"]["Iron Ore"] -= 7
                game_state["player"]["zenny"] -= 25
                # If yes, then...
                delay_print("You upgraded your Hammer!")
            else:
                #If no, then...
                delay_print("You don't have enough materials or Zenny.")
        elif choice == '3':
            player_resources = game_state["player"]["resources"]
            iron_ore = player_resources.get("Iron Ore", 0)
            zenny = game_state["player"]["zenny"]

            if iron_ore >= 6 and zenny >= 22:
                # Resources and Zenny are suficient?
                game_state["player"]["resources"]["Iron Ore"] -= 6
                game_state["player"]["zenny"] -= 22
                # If yes, then...
                delay_print("You upgraded your Bow!")
            else:
                # If no, then...
                delay_print("You don't have enough materials or Zenny.")
        elif choice == '4':
            break
        else:
            delay_print("Invalid choice, please try again.")


def sell_items():
    delay_print("What would you like to sell? (WIP)")
    # Implement selling logic here
    delay_print("\n=== Sell Items ===")
    delay_print("Available Items:")
    for item, details in game_state["player"]["inventory"].items():
        delay_print(f"{item}: {details['quantity']} (Sell Price: "
                    f"{details.get('sell_price', 0)})")
    while True:
        delay_print("\nWhat would you like to sell?")
        item_to_sell = input("Enter the item name (or 'back' to return): ")
        if item_to_sell.lower() == 'back':
            break
        if item_to_sell in game_state["player"]["inventory"]:
            quantity = int(input("How many would you like to sell? "))
            if quantity <= game_state["player"]["inventory"][item_to_sell][
                    "quantity"]:
                inventory = game_state["player"]["inventory"]
                item = inventory.get(item_to_sell, {})
                sell_price = item.get("sell_price", 0)
                if sell_price > 0:
                    game_state["player"]["inventory"][item_to_sell][
                        "quantity"] -= quantity
                    game_state["player"]["zenny"] += quantity * sell_price
                    delay_print(f"You sold {quantity} {item_to_sell} "
                                f"for {quantity * sell_price} Zenny.")
                else:
                    delay_print(
                        f"You can't sell {item_to_sell} at the market.")
            else:
                delay_print(f"You don't have that many {item_to_sell}.")
        else:
            delay_print("Invalid item name.")


def gather_resources(location):
    """
    Placeholder function for gathering resources. 
    This function should be implemented based on the game's logic.
    """
    delay_print(f"You gather resources in the {location}.")
    # Implement logic for gathering resources based on location
    game_state["player"]["resources"]["Herb"] += random.randint(1, 3)
    delay_print(f"You found {random.randint(1, 3)} Herb.")


def explore_field():

    def gather_field():
        delay_print("\nYou decide to explore the field.")
        gather_resources("Field")


def explore_kamuna_forest():
    delay_print("\nYou venture deeper into the Kamuna Forest.")
    monster = random.choice(list(game_state["monsters"].keys()))
    delay_print(f"You encounter a wild {monster}!")
    battle_monster(game_state["monsters"][monster])
    # Monster Den Check
    if random.randint(1, 10) <= 5:
        explore_monster_den()


def gather_kamuna_forest():
    delay_print("\nYou gather resources in the Kamuna Forest.")
    gather_resources("Kamuna Forest")


def explore_alcala():
    delay_print("\nYou arrive at Alcala and encounter a wild monster.")
    monster = random.choice(list(game_state["monsters"].keys()))
    delay_print(f"You encounter a wild {monster}!")
    battle_monster(game_state["monsters"][monster])
    # Monster Den Check
    if random.randint(1, 10) <= 5:
        explore_monster_den()


def explore_lamure():
    delay_print("\nYou explore the desert-like area of Lamure.")
    monster = random.choice(list(game_state["monsters"].keys()))
    delay_print(f"You encounter a wild {monster}!")
    battle_monster(game_state["monsters"][monster])
    # Monster Den Check
    if random.randint(1, 10) <= 5:
        explore_monster_den()


def explore_loloska():
    delay_print("\nYou explore the snowy biomes of Loloska.")
    monster = random.choice(list(game_state["monsters"].keys()))
    delay_print(f"You encounter a wild {monster}!")
    battle_monster(game_state["monsters"][monster])
    # Monster Den Check
    if random.randint(1, 10) <= 5:
        explore_monster_den()


def explore_pomore_garden():
    delay_print("\nYou explore the beautiful Pomore Garden.")
    monster = random.choice(list(game_state["monsters"].keys()))
    delay_print(f"You encounter a wild {monster}!")
    battle_monster(game_state["monsters"][monster])
    # Monster Den Check
    if random.randint(1, 10) <= 5:
        explore_monster_den()


def explore_monster_den():
    delay_print("\nYou stumble upon a Monster Den!")
    egg_pool = game_state["common_eggs"]  # Default to common eggs
    if random.randint(1, 100) == 1:  # 1% chance for a Rare Monster Den
        egg_pool = game_state["rare_eggs"]
        delay_print("You've stumbled upon a Rare Monster Den!")
    delay_print("Available eggs:")
    for i, egg_type in enumerate(egg_pool):
        delay_print(f"{i+1}. {egg_type}")
    choice = int(input("Choose an egg: "))
    if 1 <= choice <= len(egg_pool):
        chosen_egg = egg_pool[choice - 1]
        game_state["player"]["inventory"]["Egg"]["type"] = chosen_egg
        game_state["player"]["inventory"]["Egg"]["quantity"] += 1
        delay_print(f"You got a {chosen_egg} egg!")
    else:
        delay_print("Invalid choice.")


def find_eggs():
    delay_print("\nYou search for Monstie eggs in the Kamuna Forest.")
    delay_print("You find a mysterious egg! It could be something special...")


def visit_flower_field():
    delay_print("\nYou visit the Flower Field in Pomore Garden.")
    delay_print("It's a serene place with rare flora and fauna.")


def leave_village():
    while True:
        delay_print("\nWhere would you like to go?")
        delay_print("1. Field")
        delay_print("2. Kamuna Forest")
        delay_print("3. Alcala")
        delay_print("4. Lamure")
        delay_print("5. Loloaska")
        delay_print("6. Pomore Garden")
        delay_print("7. Return to Village")
        choice = input("Choose an option: ")
        if choice == '1':
            explore_field()
        elif choice == '2':
            explore_kamuna_forest()
        elif choice == '3':
            explore_alcala()
        elif choice == '4':
            explore_lamure()
        elif choice == '5':
            explore_loloska()
        elif choice == '6':
            explore_pomore_garden()
        elif choice == '7':
            break
        else:
            delay_print("Invalid choice. Returning to the village.")


def camp_menu():
    while True:
        delay_print("\n=== Camp Menu ===")
        delay_print("1. Combine")
        delay_print("2. Change Weapon")
        delay_print("3. Check Inventory")
        delay_print("4. Manage Quests")  # Added quest management
        delay_print("5. Return to Village")
        choice = input("Choose an option: ")
        if choice == '1':
            delay_print("Recipes learnt: Herb + Potion = Mega Potion")
            # Define combination recipes
            recipes = {('Herb', 'Potion'): 'Mega Potion'}

            def combine_items(item1, item2, items,
                              recipes):  # Pass recipes as argument
                """Combine two items according to the recipes."""
                if (item1, item2) in recipes or (item2, item1) in recipes:
                    new_item = recipes.get((item1, item2)) or recipes.get(
                        (item2, item1))
                    if items[item1]['quantity'] > 0 and items[item2][
                            'quantity'] > 0:
                        items[item1]['quantity'] -= 1
                        items[item2]['quantity'] -= 1
                        if new_item in items:
                            items[new_item]['quantity'] += 1
                        else:
                            items[new_item] = {'quantity': 1}
                        print(
                            f"Combined {item1} and {item2} to create {new_item}!"
                        )
                else:
                    print("Not enough items to combine.")

            def display_items(items):
                """Display the current items and their quantities."""
                print("\nCurrent Items:")
                for item, details in items.items():
                    print(f"{item}: {details['quantity']}")

            # Assuming 'game_state' and 'recipes' are defined somewhere in the code
            items = game_state["player"][
                "inventory"]  # Accessing player inventory
            item1 = input("Enter the first item to combine: ")
            item2 = input("Enter the second item to combine: ")
            combine_items(item1, item2, items,
                          recipes)  # Passing inventory as argument
            display_items(items)  # Displaying updated inventory

        elif choice == '2':
            delay_print("Available Weapons: Greatsword, Hammer, Bow")
            weapon_choice = int(
                input("Choose a weapon (1-Greatsword, 2-Hammer, 3-Bow): "))
            change_weapon(weapon_choice)
        elif choice == '3':
            check_inventory()
        elif choice == '4':
            manage_quests()
        elif choice == '5':
            break
        else:
            delay_print("Invalid choice, please try again.")


def change_weapon(weapon_choice):
    delay_print("Available Weapons: Greatsword, Hammer, Bow")
    if weapon_choice == 1:
        game_state["player"]["weapon"] = "Greatsword"
    elif weapon_choice == 2:
        game_state["player"]["weapon"] = "Hammer"
    elif weapon_choice == 3:
        game_state["player"]["weapon"] = "Bow"
    else:
        delay_print("Invalid choice, please try again.")


def check_inventory():
    delay_print("\n=== Inventory ===")
    for item, details in game_state["player"]["inventory"].items():
        delay_print(f"{item}: {details['quantity']}")


def manage_quests():
    delay_print("\n=== Quest Board ===")
    for quest_name, quest_data in game_state["quests"].items():
        delay_print(f"{quest_name}: {quest_data['status']}")
    while True:
        delay_print("\nWhat would you like to do?")
        delay_print("1. Accept Quest")
        delay_print("2. Turn In Quest")
        delay_print("3. Return to Camp Menu")
        choice = input("Choose an option: ")
        if choice == '1':
            accept_quest()
        elif choice == '2':
            turn_in_quest()
        elif choice == '3':
            break
        else:
            delay_print("Invalid choice.")


def accept_quest():
    delay_print("\n=== Available Quests ===")
    for quest_name, quest_data in game_state["quests"].items():
        if quest_data["status"] == "Available":
            delay_print(f"{quest_name}")
    quest_name = input("Enter the name of the quest to accept: ")
    if quest_name in game_state["quests"] and game_state["quests"][quest_name][
            "status"] == "Available":
        game_state["quests"][quest_name]["status"] = "Accepted"
        delay_print(f"You accepted the {quest_name} quest!")
    else:
        delay_print("Invalid quest name or quest not available.")


def turn_in_quest():
    delay_print("\n=== Accepted Quests ===")
    for quest_name, quest_data in game_state["quests"].items():
        if quest_data["status"] == "Accepted":
            delay_print(f"{quest_name}")
    quest_name = input("Enter the name of the quest to turn in: ")
    if quest_name in game_state["quests"] and game_state["quests"][quest_name][
            "status"] == "Accepted":
        # Check if quest conditions are met
        if game_state["quests"][quest_name]["type"] == "Gathering":
            if game_state["player"]["resources"].get(
                    game_state["quests"][quest_name]["target"],
                    0) >= game_state["quests"][quest_name]["quantity"]:
                # Reward player
                game_state["player"]["zenny"] += game_state["quests"][
                    quest_name]["reward"]["zenny"]
                if "item" in game_state["quests"][quest_name]["reward"]:
                    game_state["player"]["inventory"][
                        game_state["quests"][quest_name]["reward"]
                        ["item"]]["quantity"] += game_state["quests"][
                            quest_name]["reward"]["quantity"]
                game_state["quests"][quest_name]["status"] = "Completed"
                delay_print(
                    f"You completed the {quest_name} quest! You received your rewards."
                )
            else:
                target = game_state['quests'][quest_name]['target']
                message = f"You haven't gathered enough {target} yet."
                delay_print(message)
        elif game_state["quests"][quest_name]["type"] == "Hunt":
            # Implement hunt quest completion logic
            delay_print(f"You haven't completed the {quest_name} quest yet.")
    else:
        delay_print("Invalid quest name or quest not accepted.")


def startup_menu():
    while True:
        delay_print("\n=== Startup Menu ===")
        delay_print("1. Start New Game")
        delay_print("2. Load Saved Game")
        delay_print("3. Quit")
        choice = input("Choose an option: ")
        if choice == '1':
            start_game()
        elif choice == '2':
            load_game()
            start_game()
        elif choice == '3':
            delay_print("Thank you for playing!")
            break
        else:
            delay_print("Invalid choice, please try again.")

    if __name__ == "__main__":
        startup_menu()
