import gui
import PySimpleGUI as sg

def run():
    window = gui.make_window(gui.DomainFactory())
    window = window.combine_layout()
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
    window.close()

if __name__ == '__main__':
    run()