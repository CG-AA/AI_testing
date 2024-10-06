import useAI
import os
import curses

menu_text = "\n\t0. Refresh\n\t1. Show prompts\n\t2. Exit\n\tPress Enter to generate text\n"
menu_lines = 5

def refresh_prompts():
    with open("user_prompt.txt", "r") as file:
        useAI.user_prompt = file.read()
    with open("system_prompt.txt", "r") as file:
        useAI.system_prompt = file.read()

def get_input(stdscr, original_message=""):
    lines = []
    stdscr.clear()
    stdscr.addstr("Enter your input (press Ctrl+D to end):\n")
    stdscr.refresh()

    current_line = original_message
    stdscr.addstr(original_message)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        
        # get input
        if key == curses.KEY_ENTER or key in [10, 13]:
            lines.append(current_line)
            current_line = ""
            stdscr.addstr("\n")
        elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace key
            if current_line:  # Only delete if there is something to delete
                current_line = current_line[:-1]
                y, x = stdscr.getyx()
                stdscr.move(y, x - 1)
                stdscr.delch()
        elif key == 4:  # Ctrl+D to end input
            lines.append(current_line)
            break
        else:
            current_line += chr(key)
            stdscr.addch(key)
        
        stdscr.refresh()
    
    return lines

def delete_lines(n):
    for _ in range(n):
        print("\033[F\033[K", end="")

def show_prompts(stdscr):
    stdscr.clear()
    stdscr.addstr(f"User prompt:\n{useAI.user_prompt}\n\nSystem prompt:\n{useAI.system_prompt}")
    stdscr.refresh()
    stdscr.getch()

def start():
    with open("ai_role.txt", "r") as file:
        ai_role = file.read()
        useAI.generate_text(ai_role=ai_role)


def menu(stdscr):
    refresh_prompts()
    stdscr.clear()
    stdscr.addstr(menu_text)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in [ord('0'), ord('1'), ord('2'), 10]:  # 10 = ENTER
            break

    delete_lines(menu_lines + 1)
    if key == ord('0'):
        refresh_prompts()
    elif key == ord('1'):
        show_prompts(stdscr)
    elif key == ord('2'):
        exit()
    elif key == 10:
        start()
    else:
        print("Invalid input")

    menu(stdscr)

def main():
    os.system("clear")
    curses.wrapper(menu)


if __name__ == "__main__":
    main()