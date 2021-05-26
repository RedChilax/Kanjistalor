from pynput import keyboard
import win32clipboard
import webbrowser		

COMBINATION = [{keyboard.Key.shift , keyboard.KeyCode(char='m')} , {keyboard.Key.shift , keyboard.KeyCode(char='M')}]

current = set()

def execute():
	win32clipboard.OpenClipboard()
	data = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()
	webbrowser.open(u"https://fr.wiktionary.org/wiki/"+data)
	
def on_press(key) :
	if any([key in COMBO for COMBO in COMBINATION]): 
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in COMBINATION):
			execute()
def on_release(key) : 
	if any([key in COMBO for COMBO in COMBINATION]): 
		current.remove(key)
		

with keyboard.Listener(on_press=on_press , on_release=on_release) as listener : 
	listener.join()