import os
import json

RUNEWORD_DIRECTORY = os.path.join("data", "mmorpg_runeword")
use_input_output = True  # true if using input/output files instead of manually typing.

def get_matching_files(base_directory, equipment_type, max_rune_slots, available_runes):
    matching_files = []

    for filename in os.listdir(RUNEWORD_DIRECTORY):
        if filename.endswith('.json'):
            with open(os.path.join(RUNEWORD_DIRECTORY, filename), 'r') as file:
                data = json.load(file)
                slots = data.get('slots', [])
                runes = data.get('runes', [])

                # Match equipment type and check if the runeword uses only available runes
                if equipment_type not in slots:
                    continue
                if len(runes) > max_rune_slots:
                    continue

                # Check if all runes in the file are available in the player's runes
                if all(rune.upper() in available_runes for rune in runes):
                    matching_files.append(filename)

    return matching_files

def format_stats(stats, single_line_format):
    formatted_stats = []

    # Separate stats into percentage and flat, and prioritize negative stats
    negative_stats = [s for s in stats if s['max'] < 0]
    positive_stats = [s for s in stats if s['max'] >= 0]
    percentage_stats = [s for s in positive_stats if s['type'] == 'PERCENT']
    flat_stats = [s for s in positive_stats if s['type'] == 'FLAT']

    # Format negative stats
    for stat in negative_stats:
        stat_str = f"{stat['min']}%" if stat['type'] == 'PERCENT' else f"{stat['min']}"
        formatted_stats.append(f"{stat_str} {stat['stat'].replace('_', ' ').title()}")

    # Format percentage stats
    for stat in percentage_stats:
        if stat['min'] == stat['max']:
            formatted_stats.append(f"+{int(stat['max'])}% {stat['stat'].replace('_', ' ').title()}")
        else:
            formatted_stats.append(f"+{int(stat['min'])}-{int(stat['max'])}% {stat['stat'].replace('_', ' ').title()}")

    # Format flat stats
    for stat in flat_stats:
        if stat['min'] == stat['max']:
            formatted_stats.append(f"+{int(stat['max'])} {stat['stat'].replace('_', ' ').title()}")
        else:
            formatted_stats.append(f"+{int(stat['min'])}-{int(stat['max'])} {stat['stat'].replace('_', ' ').title()}")

    # If single_line_format is True, return stats as a single line
    if single_line_format:
        return ", ".join(formatted_stats)
    else:
        # Otherwise, return each stat on a new line
        return formatted_stats

def display_file_contents(base_directory, filenames, single_line_format):
    slot_order = ['helmet', 'chest', 'boots', 'pants']

    directory = os.path.join(base_directory, RUNEWORD_DIRECTORY)
    for filename in filenames:
        with open(os.path.join(directory, filename), 'r') as file:
            data = json.load(file)
            runeword_name = data['id'].replace('_', ' ').title()
            runes = ", ".join(rune.upper() for rune in data['runes'])
            slots = sorted(data['slots'], key=lambda s: slot_order.index(s) if s in slot_order else len(slot_order))
            slots = ", ".join(slot.title() for slot in slots)
            stats = format_stats(data['stats'], single_line_format)

            print(f"\n{runeword_name}")
            print(f"Runes: {runes}")
            print(f"Slots: {slots}")
            # Print the stats based on the format toggle
            if isinstance(stats, list):
                for stat in stats:
                    print(stat)
            else:
                print(stats)

def get_equipment_types(base_directory):
    directory = os.path.join(base_directory, RUNEWORD_DIRECTORY)
    equipment_types = set()

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                slots = data.get('slots', [])
                for slot in slots:
                    equipment_types.add(slot.capitalize())  # Capitalize each type

    return sorted(equipment_types)

def get_max_rune_slots(base_directory):
    directory = os.path.join(base_directory, RUNEWORD_DIRECTORY)
    max_rune_slots = 0

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                runes = data.get('runes', [])
                max_rune_slots = max(max_rune_slots, len(runes))

    return max_rune_slots

def format_equipment_types(equipment_types):
    categories = {
        "Weapons": ["Sword", "Spear", "Dagger", "Axe", "Hammer", "Staff", "Bow", "Crossbow"],
        "Armor": ["Helmet", "Chest", "Boots", "Pants"],
        "Jewelry": ["Necklace", "Ring"],
        "Miscellaneous": ["Tome", "Totem", "Shield"]
    }

    formatted_output = []
    extra_types = []

    # Group equipment types into categories
    for category, items in categories.items():
        found_items = [item for item in items if item in equipment_types]
        if found_items:
            formatted_output.append(", ".join(found_items))
            for item in found_items:
                equipment_types.remove(item)

    # Add any extra types found (outside of predefined categories)
    if equipment_types:
        extra_types = list(equipment_types)
        formatted_output.append(", ".join(extra_types))
        print(f"Found {len(extra_types)} extra types!")

    return "\n".join(formatted_output)

def get_last_input():
    last_input_file = os.path.join('data', '.code_data', 'last_output.txt')

    if os.path.exists(last_input_file):
        with open(last_input_file, 'r') as file:
            equipment_type = file.readline().strip()
            max_rune_slots = int(file.readline().strip())
            return equipment_type, max_rune_slots
    return None, None

def save_last_input(equipment_type, max_rune_slots):
    last_input_file = os.path.join('data', '.code_data', 'last_output.txt')

    with open(last_input_file, 'w') as file:
        file.write(f"{equipment_type}\n")
        file.write(f"{max_rune_slots}\n")

def toggle_input_output_operations(base_directory):
    input_file = 'data/.input.txt'
    output_file = 'data/.output.txt'

    # If .input.txt doesn't exist, create it with the default values
    if not os.path.exists(input_file):
        with open(input_file, 'w') as file:
            file.write("Runes: VEN, YUN, WIR, ENO, ITA, VEN, WIR\n")
            file.write("shield|6\n")
            file.write("sword|5\n")

    # Read input from .input.txt
    with open(input_file, 'r') as file:
        lines = file.readlines()
        runes = lines[0].strip().split(': ')[1].split(', ')
        equipment = [line.strip() for line in lines[1:]]

    # Normalize the rune names to uppercase and strip spaces for comparison
    available_runes = set(rune.strip().upper() for rune in runes)

    # Process runewords based on input data
    result = []
    for equip in equipment:
        equip_type, max_slots = equip.split('|') if '|' in equip else (equip.strip(), 6)  # Default to 6 slots
        equip_type = equip_type.strip()
        max_slots = int(max_slots)
        matching_files = get_matching_files(base_directory, equip_type, max_slots, available_runes)

        if not matching_files:
            continue

        result.append(f"======== {equip_type.capitalize()} ({max_slots}) ========")
        for filename in matching_files:
            with open(os.path.join(base_directory, RUNEWORD_DIRECTORY, filename), 'r') as file:
                data = json.load(file)
                runeword_name = data['id'].replace('_', ' ').title()
                runes_in_file = [rune.strip().upper() for rune in data['runes']]  # Maintain the original order here
                matching_runes = available_runes.intersection(runes_in_file)

                if not matching_runes:
                    continue

                formatted_stats = format_stats(data['stats'], True)
                result.append(
                    f"{runeword_name}\nRunes: {', '.join(runes_in_file)}\nSlots: {', '.join(data['slots'])}\n{formatted_stats}\n")

    # If no matching files are found, make the output file blank and print the message to the console
    if not result:  # If no runewords are found
        with open(output_file, 'w') as file:
            file.truncate(0)  # Clear the file content
        print("No matching runewords found.")
    else:
        with open(output_file, 'w') as file:
            file.write("\n".join(result))

def main():
    base_directory = os.path.dirname(__file__)  # Get the directory where the script is located

    if use_input_output:
        # Use .input.txt and .output.txt
        toggle_input_output_operations(base_directory)
        return

    # Scan for equipment types in the JSON files
    equipment_types = get_equipment_types(base_directory)

    if not equipment_types:
        print("Error: No equipment types found in JSON files.")
        return  # Exit the program if no types are found

    # Format and display the types of equipment
    formatted_types = format_equipment_types(equipment_types)
    print(formatted_types)

    # Display the max number of rune slots (no extra space before this)
    max_rune_slots = get_max_rune_slots(base_directory)
    print(f"Max slots: {max_rune_slots}\n")

    # Proceed with the original prompt
    equipment_type, max_rune_slots_input = get_last_input()

    if equipment_type is None or max_rune_slots_input is None:
        equipment_type = input("Type of equipment: ")
        max_rune_slots_input = int(input("Number of rune slots: "))

        # Save these inputs for future use
        save_last_input(equipment_type, max_rune_slots_input)

    # Set to True for stats to be displayed in one line, False for separate lines
    single_line_format = True  # You can toggle this between True/False

    matching_files = get_matching_files(base_directory, equipment_type, max_rune_slots_input, available_runes)

    if not matching_files:
        print("No matching runewords found.")
        return

    runewords = ", ".join(filename.rsplit('.', 1)[0].replace('_', ' ').title() for filename in matching_files)
    print(f"Runewords: {runewords}")

    display_file_contents(base_directory, matching_files, single_line_format)

if __name__ == "__main__":
    main()
