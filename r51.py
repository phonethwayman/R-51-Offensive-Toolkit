import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_DIR, 'banner'))
sys.path.append(os.path.join(ROOT_DIR, 'programs'))

try:
    from main_banner import show_menu_and_get_choice
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import main_banner.py. Check file path. Error: {e}")
    sys.exit(1)

# Option 1 Tool Import
try:
    from portscanner import run_port_scanner
except ImportError:
    print("Warning: portscanner.py not found. Option 2 disabled.")
    def run_port_scanner():
        print("Port Scanner module not loaded.")


#  Main Logic Function
def main():
    """
    The main execution loop for the R51 tool. Handles menu interaction and tool calls.
    """
    while True:
        choice = show_menu_and_get_choice()
        
        if choice == '1':
            print("\n[+] Starting Port Scanner...")
            run_port_scanner()
            
        elif choice == '0':
            print("👋 Exiting R51. Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")
            
        if choice != '0':
            input("\nPress Enter to return to the main menu...")
            
if __name__ == "__main__":
    main()