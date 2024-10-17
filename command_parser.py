# # # # # # # # # # # # #
# # command_parser.py # #
# # # # # # # # # # # # #
import re

def parse_nomi_response(response_text):
    """
    Parses the Nomi AI's response and returns a command for the Lovense device.

    Args:
        response_text (str): The text response from the Nomi AI.

    Returns:
        dict: A command dictionary, e.g., {'action': 'Vibrate:10', 'timeSec': 20}
              or None if no command is found.
    """

    # Initialize command variables
    response_text = response_text.lower()
    action = None
    time_sec = 20  # Default duration

    # Patterns for different actions
    vibrate_pattern = re.compile(r'\b(vibrate|buzz|pulse|shake)\b(?:.*?(\d+))?', re.IGNORECASE)
    stop_pattern = re.compile(r'\b(stop|pause|halt|cease)\b', re.IGNORECASE)
    pattern_pattern = re.compile(r'\b(pattern|mode|preset)\b(?:.*?(pulse|wave|fireworks|earthquake))?', re.IGNORECASE)
    strength_pattern = re.compile(r'\b(strength|level|intensity)\b(?:.*?(\d+))', re.IGNORECASE)

    # Match patterns
    if stop_pattern.search(response_text):
        action = 'Stop'
        time_sec = 0
    elif vibrate_match := vibrate_pattern.search(response_text):
        strength = vibrate_match.group(2)
        if strength:
            # Ensure strength is within acceptable range (1-20)
            strength = int(strength)
            if 1 <= strength <= 20:
                action = f'Vibrate:{strength}'
            else:
                action = 'Vibrate:10'  # Default strength
        else:
            action = 'Vibrate:10'  # Default strength
    elif pattern_match := pattern_pattern.search(response_text):
        preset_name = pattern_match.group(2)
        if preset_name:
            action = f'Preset:{preset_name}'
        else:
            action = 'Preset:pulse'  # Default preset
    elif strength_match := strength_pattern.search(response_text):
        strength = int(strength_match.group(2))
        if 1 <= strength <= 20:
            action = f'Vibrate:{strength}'
        else:
            action = 'Vibrate:10'  # Default strength

    # Construct the command dictionary if an action is found
    if action:
        return {'action': action, 'timeSec': time_sec}
    else:
        return None  # No command detected

