import keyboard
while True:
    if keyboard.read_key()=='enter':
        print('starting calibration')
        break
    elif keyboard.read_key() != 'enter':
        print('yout have pressed another key. Press control+c tp skip program')

