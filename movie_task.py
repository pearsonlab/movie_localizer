from psychopy import visual, core, event, gui
import json
import os
import sys
from utils import flicker


mental = [182, 250, 270, 286]
pain = [122, 134, 156, 192, 206, 224, 312]
social = [62, 86, 96, 110, 124]
control = [24, 48, 70]

'''
conds(1).durs = [8, 8, 10, 18]; % mental
conds(2).durs = [2, 6, 4, 2, 6, 4, 2]; % pain third one can be 10 sec
conds(3).durs = [6, 10, 2, 6, 4]; % social
conds(4).durs = [6, 10, 8]
'''

def save_data(day_time, start_time, stop_time, participant):

    trial = {}
    trial['day_time'] = day_time
    trial['start_time'] = start_time
    trial['stop_time'] = stop_time

    trial['mental'] = mental
    trial['pain'] = pain
    trial['social'] = social
    trial['control'] = control

    if not os.path.exists('behavioral/'):
            os.makedirs('behavioral')

    with open('behavioral/mov_task_'+ participant + '.json', 'a') as f:
        f.write(json.dumps(trial))
        f.write('\n')

def get_settings():
    dlg = gui.Dlg(title='Choose Settings')
    dlg.addField('Experiment Name:', 'Movie_Task')
    dlg.addField('Subject ID:', 'practice')
    dlg.show()
    if dlg.OK:
        return dlg.data
    else:
        sys.exit()

def run():
    nothing, participant = get_settings()

    win = visual.Window(winType='pyglet', monitor="testMonitor", units="pix", screen=1,
            fullscr=True, colorSpace='rgb255', color=(0, 0, 0))
    win.mouseVisible = False
    mov = visual.MovieStim3(win, 'partly_cloudy.mp4', size=[1440,850],
                       flipVert=False, flipHoriz=False, loop=False)

    globalTimer = core.Clock()
    start_time = globalTimer.getTime()
    flicker(win, 4)
    day_time = core.getAbsTime()

    win.flip()
    core.wait(5)
    win.flip()

    while mov.status != visual.FINISHED:
        mov.draw()
        win.flip()

        if event.getKeys(keyList=['escape','q']):
            win.close()
            stop_time = globalTimer.getTime()
            save_data(day_time, start_time, stop_time, participant)
            core.quit()

    stop_time = globalTimer.getTime()
    flicker(win, 16)

    save_data(day_time, start_time, stop_time, participant)

    core.quit()

if __name__ == '__main__':
    run()
