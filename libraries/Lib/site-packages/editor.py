import sys
import time
import traceback

from browser import document as doc, window

editor = doc["editor"]
def get_value(): return editor.value
def set_value(x):editor.value = x
editor.getValue = get_value
editor.setValue = set_value

class cOutput:

    def write(self, data):
        doc["console"].value += str(data)

    def flush(self):
        pass

# Send print output to console
sys.stdout = cOutput()
sys.stderr = cOutput()

#print('local storage available:',hasattr(window, 'localStorage'))

if hasattr(window, 'localStorage'):
    from browser.local_storage import storage
else:
    storage = None

def reset_src_area():
    if storage and "py_src" in storage:
        editor.value = storage["py_src"]

output = ''

def show_console(ev):
    doc["console"].value = output
    doc["console"].cols = 60

# run a script, in global namespace
def run(*args):
    #doc["console"].value = ''    # Clears console
    src = editor.getValue()
    if storage is not None:
       storage["py_src"] = src

    t0 = time.perf_counter()
    try:
        ns = {'__name__':'__main__'}
        exec(src, ns)
        state = 1
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        state = 0

    print('<completed in %6.2f ms>' % ((time.perf_counter() - t0) * 1000.0))
    
    # Scroll to bottom so any new text is visible
    doc['console'].scrollTop = doc['console'].scrollHeight

    return state

reset_src_area()
