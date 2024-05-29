import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

def countdown(stdscr):
	stdscr.clear()
	for i in range(3, 0, -1):
		stdscr.clear()
		stdscr.addstr(f"Starting in {i}...")
		stdscr.refresh()
		time.sleep(1)

def display_text(stdscr, target, current, wpm=0, accuracy=0):
	stdscr.addstr(target, curses.color_pair(3))
	stdscr.addstr(1, 0, f"WPM: {wpm}  Accuracy: {accuracy:.2f}%")

	for i, char in enumerate(current):
		correct_char = target[i]
		if char == correct_char:
			color = curses.color_pair(1)
		else:
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)
	
	# Highlight the current character
	if len(current) < len(target):
		stdscr.addstr(0, len(current), target[len(current)], curses.color_pair(4))

def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def calculate_accuracy(target, current):
	correct_chars = sum(1 for i, char in enumerate(current) if i < len(target) and char == target[i])
	return (correct_chars / len(current)) * 100 if current else 0

def wpm_test(stdscr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
		accuracy = calculate_accuracy(target_text, current_text)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm, accuracy)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)

def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

	start_screen(stdscr)
	while True:
		countdown(stdscr)
		wpm_test(stdscr)
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue or ESC to exit...")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)
