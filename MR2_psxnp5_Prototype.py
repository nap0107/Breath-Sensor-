HP_TIME_CONSTANT=0.05
SAMPLE_TIME=0.01

TIME_THRESHOLD=0.3
SILENCE_BEFORE=0.2
SILENCE_AFTER=0.2

UP_THRESHOLD=.01
DOWN_THRESHOLD=-.01

import graphs, sensors,time
import filters
graphs.set_style("exhale","rgb(0,0,0)",0,1)
graphs.set_style("hp","rgb(0,255,0)",-.1,.1,subgraph_y=1)

hpFilter=filters.HighPassFilter.make_from_time_constant(HP_TIME_CONSTANT,SAMPLE_TIME)
c=0

lastPosition=0

lastUp=None
lastDown=None
crossingUp=None

crossingDown=None

while True:
    exhale_level=sensors.sound.get_level()
    hp=hpFilter.on_value(exhale_level)
    graphs.on_value("exhale",exhale_level)
    graphs.on_value("hp",hp)
    time.sleep(SAMPLE_TIME) 
    if lastPosition!=-1 and hp<DOWN_THRESHOLD:
        lastPosition=-1
        lastDown=crossingDown
        crossingDown=time.time()
    if lastPosition!=1 and hp>UP_THRESHOLD:
        lastPosition=1
        lastUp=crossingUp
        crossingUp=time.time()
    if crossingDown!=None and crossingUp!=None and crossingDown>crossingUp:
        if crossingDown-crossingUp<TIME_THRESHOLD and time.time()- crossingDown>SILENCE_AFTER:
                if lastDown==None or (lastDown<crossingUp and crossingUp-lastDown)>SILENCE_BEFORE:
                    print("Proper exhale!",lastDown,crossingUp)
                lastUp=crossingUp
                lastDown=crossingDown


