import os
from subprocess import run


def clear_screen():
    """Clear the terminal/console output in a cross-platform way."""
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            run(['clear'], check=False)
    except Exception:
        # Fallback: print several newlines if clearing fails
        print('\n' * 100)