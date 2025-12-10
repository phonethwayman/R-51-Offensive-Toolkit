import os
import subprocess
import sys

# --- Package Installation Check ---
try:
    from termcolor import colored
except ImportError:
    print("[!] 'termcolor' package not found. Installing now...")
    try:
        # Use subprocess to run the pip install command
        subprocess.check_call([sys.executable, "-m", "pip", "install", "termcolor"])
        from termcolor import colored
        print("[+] 'termcolor' installed successfully.")
    except Exception as e:
        print(f"[-] Could not install 'termcolor'. Please install it manually: pip install termcolor. Error: {e}")
        sys.exit(1)

# --- Function to Display Banner ---
def display_banner():
    """
    Reads the banner from the file and displays it with color,
    using targeted content matching for the 'Defence' quote.
    """
    banner_path = os.path.join(os.path.dirname(__file__), 'banner')
    
    # --- Configuration for Targeted Line Split (using the user's slice points) ---
    TARGET_PHRASE = "Defence is the Planning of an Attack" 
    START_TEXT_SLICE = 27
    END_TEXT_SLICE = 63
    
    try:
        # OPENING THE FILE WITH UTF-8 ENCODING
        with open(banner_path, 'r', encoding='utf-8') as f:
            banner_lines = f.readlines()
    except FileNotFoundError:
        print(colored("[-] Banner file (R51/banner/banner) not found!", 'red'))
        return

    # Define color mappings based on your general output pattern (line indices)
    colors_map = {
        'yellow_part': range(6),      # Lines 0 to 5
        'green_part': range(6, 12),   # Lines 6 to 11
    }

    # Print the banner line by line with color
    for i, line in enumerate(banner_lines):
        line_stripped = line.strip('\n')
        
        # --- Targeted Content Match Logic for the Quote ---
        if TARGET_PHRASE in line_stripped:
            
            # Part 1: Left ASCII Border (Red)
            part1_red = line_stripped[:START_TEXT_SLICE]
            
            # Part 2: Quote Text (White)
            part2_white = line_stripped[START_TEXT_SLICE:END_TEXT_SLICE]
            
            # Part 3: Right ASCII Border (Red)
            part3_red = line_stripped[END_TEXT_SLICE:]
            
            # Print the three parts, coloring them separately
            print(colored(part1_red, 'red') + colored(part2_white, 'white', attrs=['bold']) + colored(part3_red, 'red'))
            
            continue # Skip the general print logic for this line

        # --- Standard Color Logic for all other lines ---
        if i in colors_map['yellow_part']:
            color = 'yellow'
        elif i in colors_map['green_part']:
            color = 'green'
        else:
            color = 'red'
        
        # Apply the general color to the whole line
        print(colored(line_stripped, color))
        
# --- Function to Show Menu and Get Choice ---
def show_menu_and_get_choice():
    """
    Displays the banner and the main menu options using the Simple Bracket Style.
    Returns the user choice string.
    """
    display_banner()
    
    # Display the unique hacking-style menu
    print(colored("\n===============================================", 'cyan', attrs=['bold']))
    print(colored("        🤖 R51 - CYBER SECURITY TOOLSET 🤖", 'cyan', attrs=['bold']))
    print(colored("===============================================", 'cyan', attrs=['bold']))
    
    # Menu Items - Simple Bracket Style
    BRACKET_COLOR = 'magenta'
    NUMBER_COLOR = 'yellow'
    
    
    print(colored(" [", BRACKET_COLOR, attrs=['bold']) + colored("1", NUMBER_COLOR, attrs=['bold']) + colored("] ", BRACKET_COLOR, attrs=['bold']) + 
          colored("Port Scanner (programs/portscanner.py)", 'white', attrs=['bold']))
    
    print(colored(" [", BRACKET_COLOR, attrs=['bold']) + colored("0", NUMBER_COLOR, attrs=['bold']) + colored("] ", BRACKET_COLOR, attrs=['bold']) + 
          colored("Exit R51", 'white', attrs=['bold']))
    
    print(colored("-----------------------------------------------", 'cyan'))

    try:
        choice = input(colored(">> Enter your selection (0-1): ", 'green', attrs=['bold']))
        return choice.strip()
    except KeyboardInterrupt:
        return '0'
        
# --- Execution Block (for direct testing) ---
if __name__ == '__main__':
    print(colored("--- Running main_banner.py directly for testing ---", 'blue'))
    try:
        choice = show_menu_and_get_choice()
        print(colored(f"\n[INFO] show_menu_and_get_choice() returned choice: {choice}", 'blue'))
    except Exception as e:
        print(f"An error occurred during direct execution: {e}")