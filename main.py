import ssd1306
import machine
import utime as  time
import framebuf
import base64
import math
print("GurgleApps.com Pico Pong")
# would have used pin 1 & 2 but they were broken on one of our Pico Boards
speaker_pin = 3
play_button_pin = 2
left = 26
right = 27
clockPin = 5
dataPin = 4
bus = 0
mode_init = 1
mode_playing = 2
mode_game_over = 3
mode = mode_init # mode_init,mode_playing,mode_game_over
analog_pin_left = machine.ADC(left)
analog_pin_right = machine.ADC(right)
play_button = machine.Pin(play_button_pin,machine.Pin.IN, machine.Pin.PULL_DOWN)
speaker = machine.PWM(machine.Pin(speaker_pin))
speaker.duty_u16(0)
i2c = machine.I2C(bus,sda=machine.Pin(dataPin),scl=machine.Pin(clockPin))
display = ssd1306.SSD1306_I2C(128,64,i2c)
logoSmallB = b'aBn/gP//wH//4D//8B/w/AAf/gAP/wAH/4AD8MAAAeAAAPAAAHgAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAA4AAAAAAAOAAAAAACAOAAAAAAADgAAAAAAgCxAAAAAAHQAB4AMeIAscAAGMAB2AAeBPHiAJHsACmqAbwAGySBIhixLxwhr8H4ABEkgSIt8S+UIS3h+AARJIEiLfktsGE5IVIAFCSBoj2ZrbgoqSGYABckgeIhGe2MOOkgngATPIAiKQFthYBpIZgAEzwBIjgBD70ACSCYAB4AAaAQAQ0YAAEgmAAOAADgAAEMAAAAJpgAAAAAQAAADAAAAACADAAAHgAADwQAB4AAAw+AAP/AAH/gAD/wAB8P+A///Af//gP//wH/D////////////////w'
logoLargeB = b'gB//8A////AP///wD///8A///4AB//+AAf//gAH//4AB//wAAD/8AAA//AAAP/wAAD/gAAAH4AAAB+AAAAfgAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAAAAAMAAAAAAAAAB4AAAAAAAAAHgAAAAAABgAeAAAAAAAAADwAAAAAAAYAFhgAAAAAAAHcAA4AAwZGADYYAAAHHAABwAAfAB8PxgA2HyAADz7AA94AH4CfjMYAMxswABs68AG8ABmMmQzGDiMZvBwYMvsA/QAZjJgMxh4/Gb4+GDP/g/wAMIyYDMYTPxmzNBgzz4B8ADCMmAzGN3sZszAZM8yDxQAwDJgExj5jmbM8GxPMgdwAM4yYB8YwYZ+zHh8fzMHdADPN2AfGMmAfswbMDszB3QARz9gAxjZgGzsmwADMwZ0AGY6ADMYeABg/PIAATMWdAB+AAATCGAAYNzgAAAzBnQAPgAAHwAAAGDAAAAAAxZ0ABwAAA8AAAAAwAAAAAA2cAAAAAAAAAAAAMAAAAAABgDgAAAH4AAAB+BAAAfgAAAH/AAAP/wAAD/8AAA//AAAP//AA///wAP//8AD///AA///+B////gf///4H///+B//'
logoPongB = b'gCz///////////////////////////////////////////wD8Pgf8D//AH/A/7wfgf/8APDwD8Af/wA/gHg8HwD//ABw4AeAD/8AHwA4HB4Af/wAcOAHgA//AA4AGBwcAH/8MHDggwAH/w4OABgcHAB//DgwwcMDB/8PDA4YDBg4P/w4MMPDB4f/DwweCAwYfD/8ODDDwweH/w8MHggEGHw//Dgww+cPh/8PDB8IBBj8P/w4MMP+D4P/DwwfCAQQ///8OHDD/g+CAQ4MPwwAMP///CBww/4PwgEEDD8MQDDAP/wAcMP+D4IBABw/DEAwwB/8APDD/w+CAQA8PwxgMMAf/APww+EPh/8AfB8MYDDgH/wf8MPhD4f/B/weCGAw+H/8P/DDww+H/wf8HghwMPh//D/wwcMHB/8H/h4YcDB4f/w/8OHDgA//B/4AGDg4MP/8P/DgA4AP/wf+ABg4OAD//D/w4AfAH/8H/wA4ODgA//wf8PAP4D//B/+AeDw8Af/8P//4H/j//wf/8/h//gP/////////////////////////////////////////////////////////////////////////////////////////////////////////////DnMD4c+Dh4ODwf4eHjx//gZzAcDPg4eBgYH8DA44f/xucxGNz5+HmZiP+NjGGH/8/nMZn8+fg5mYj/n5xhh//P5zEZ/PgxOZmIf5+eYYf/zGcwEYz4MzgYHD+fnmUn/8xnMDmM+HM4OD4fn55kJ//OZzE5zPnwGfn/H5+cZCf/xmIxGMx54Bn5/x+PjGRn/+BgMRgMCCMZ+fgZwIDmZ//gcHGcDAgjmfn4OcDB5mf///3//////////v/////////////////////////////////////////////////w=='
logoPongIB = b'gCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8DwfgD8AA/4A/AEPgfgAD/w8P8D/gAP/Af4fD4P8AA/+PH/h/8AD/4P/H4+H/gAP/jx/4f/AA//H/5+Pj/4ADz48ffP/4APHx/+fj4/+AA8fPPjz8+ADw8/Hn8+fHwAPHzzw8+HgA8PPh9/Png8ADx888PPh4APDz4ff754PAA8fPPBjweADw8+D3++cDwAPHzzwB8HwA8PPg9/vvAAADx488AfB9/vHzwPP/zwAAA9+PPAHwPf7788Dzv88/wAP/jzwB8H3+/+PA87/PP+AD/w88APB9/v/DwPOfzz/gA/wPPB7weAD/g+Dzn88f4APgDzwe8HgA+APh95/PB4ADwA88PPB4APgD4fePzweAA8APPjz4+AD4AeHnj8+HgAPADx48f/AA+AH/58fHzwADwA8f/H/wAPgB/+fHx/8AA8APH/g/4AD4AP/Hx8f/AAPgDw/wH8AA+AB/h8PD/gADwAAH4AcAAPgADAeAAfwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Yz8HjB8eHx8PgHh4cOAAfmM/j8wfHh+fn4D8/HHgAORjO5yMGB4ZmdwByc554ADAYzmYDBgfGZncAYGOeeAAwGM7mAwfOxmZ3gGBhnngAM5jP7nMHzMfn48BgYZrYADOYz8ZzB4zHx8HgYGGb2AAxmM7GMwYP5gYA4GBjm9gAOZ3O5zOGH+YGAOBwc5uYAB+fzufz99zmBgfmP38ZmAAfj45j8/fcZgYHxj8+GZgAAAIAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='
clean_count = 0
analog_min = 22000
analog_max = 51000
paddle_l_y_old = -1
paddle_r_y_old = -1
max_score = 10
ball_speed = 6
ball_width = 3
ball_height = 3
ball_half_height = ball_height >> 1
ball_x = 0
ball_y = 0
ball_vx = ball_speed
ball_vy = ball_speed
max_x = 128
max_y = 64
min_x = 0
min_y = 0
paddle_width = 3
paddle_height = 12
paddle_half_height = paddle_height >> 1
paddle_x = 128 - paddle_width
paddle_y = 30
paddle_speed = 5
net_width = 2
net_segmment_height = 5
net_segmment_gap = 3
l_score = 0
r_score = 0
last_up = time.ticks_ms()
buff = framebuf.FrameBuffer(bytearray(max_x*max_y),max_x,max_y,framebuf.MONO_HLSB)

def play_theme():
    notes = [[587,0.5],[523,0.5],[587,0.5],[0,0.5],[587,0.5],[523,0.5],[587,0.5],[0,0.5]
             ,[587,0.5],[523,0.5],[440,0.5],[523,0.5],[659,0.5],[523,0.5],[587,0.75]]
    for note in notes:
        speaker.duty_u16(int(65535/2))
        if note[0] == 0:
            speaker.duty_u16(0)
        else:
            speaker.freq(note[0])
        time.sleep(note[1])
    speaker.duty_u16(0)

def draw_net(d):
    y=0
    while y<max_y:
        d.fill_rect((max_x-net_width)>>1,y,net_width,net_segmment_height,1)
        y+=net_segmment_height + net_segmment_gap

def roundUp(x):
    return ((x+7)&(-8))

def dataToBuff(data):
    height = len(data)
    width = len(data[0])
    height = roundUp(height)
    width = roundUp(width)
    fbuf = framebuf.FrameBuffer(bytearray(int(width * height / 8)), width, height, framebuf.MONO_HLSB)
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            fbuf.pixel(x,y,c)
    return fbuf

def customToBuff(data):
    width = data[0]
    height = data[1]
    fbuff = framebuf.FrameBuffer(data[2:],width,height, framebuf.MONO_HLSB)
    return fbuff
      
def show_large_logo():
    display.blit(logoLargeBuff, 0, 0)
    display.show()
    
"""
Change value of analog pin to y position
"""
def analog_to_y(analog_pin):
    analog = analog_pin.read_u16()
    if analog < analog_min:
        analog = analog_min
    if analog > analog_max:
        analog = analog_max
    analog = analog - analog_min
    analog = analog / (analog_max - analog_min)
    analog= int(analog * (max_y - paddle_height))
    return analog

def sound_miss():
    speaker.duty_u16(int(65535/2))
    speaker.freq(220)
    timer = machine.Timer()
    timer.init(freq=2, mode=machine.Timer.ONE_SHOT, callback=sound_off)
    
def sound_hit():
    speaker.duty_u16(int(65535/2))
    speaker.freq(440)
    timer = machine.Timer()
    timer.init(freq=20, mode=machine.Timer.ONE_SHOT, callback=sound_off)
    
def sound_bounce():
    speaker.duty_u16(int(65535/2))
    speaker.freq(330)
    timer = machine.Timer()
    timer.init(freq=20, mode=machine.Timer.ONE_SHOT, callback=sound_off)

def sound_off(timer):
    speaker.duty_u16(0)

def point_to(player):
    global l_score,r_score, mode
    sound_miss()
    if player == "left":
        l_score+=1
        buff.fill_rect(30,0,20,8,0)
        buff.text(str(l_score),30,0,1)
        if l_score == max_score:
            mode = mode_game_over
            buff.text("WIN!",17,30,1)
            display.blit(buff,0,0)
            display.show()
            time.sleep(0.5)
            play_theme()
    elif player == "right":
        r_score+=1
        buff.fill_rect(90,0,20,8,0)
        buff.text(str(r_score),90,0,1)
        if r_score == max_score:
            mode = mode_game_over
            buff.text("WIN!",83,30,1)
            display.blit(buff,0,0)
            display.show()
            time.sleep(0.5)
            play_theme()
    display.blit(buff,0,0)
    
def intro():
    global l_score, r_score
    display.fill(0)
    display.show()
    show_large_logo()
    time.sleep(1)
    display.fill(0)
    display.blit(logoPong, 0, 2)
    display.show()
    time.sleep(2.5)
    display.blit(logoPongI, 0, 2)
    display.show()
    time.sleep(3)
    buff.fill(0)
    l_score = 0
    r_score = 0
    draw_net(buff)
    buff.text(str(l_score),30,0,1)
    buff.text(str(r_score),90,0,1)
    display.blit(buff,0,0)
    clean_count = 0
    
def play_frame():
    global clean_count, paddle_l_y_old, paddle_r_y_old,ball_x,ball_y,ball_vx,ball_vy
    paddle_l_y = analog_to_y(analog_pin_left)
    paddle_r_y = analog_to_y(analog_pin_right)
    clean_count = (clean_count + 1) % 6
    if clean_count == 0:
        display.blit(buff,0,0)
      
    if paddle_l_y != paddle_l_y_old or clean_count == 0:
        display.fill_rect(0,paddle_l_y_old,paddle_width,paddle_height,0)
        display.fill_rect(0,paddle_l_y,paddle_width,paddle_height,1) #left paddle
        paddle_l_y_old = paddle_l_y
        
    if paddle_r_y != paddle_r_y_old or clean_count == 0:
        display.fill_rect(max_x - paddle_width,paddle_r_y_old,paddle_width,paddle_height,0)
        display.fill_rect(max_x - paddle_width,paddle_r_y,paddle_width,paddle_height,1) #left paddle
        paddle_r_y_old = paddle_r_y
    display.fill_rect(int(ball_x),int(ball_y),ball_width,ball_height,1)
    display.show()
    display.fill_rect(int(ball_x),int(ball_y),ball_width,ball_height,0)
    ball_x += ball_vx
    ball_y += ball_vy
    if ball_y > max_y - ball_height:
        sound_bounce()
        ball_vy = -ball_vy
        ball_y = max_y - ball_height
    elif ball_y < min_y:
        sound_bounce()
        ball_vy = -ball_vy
        ball_y = min_y
    if ball_x >= max_x - ball_width: #hit right paddle
        dy = (ball_y + ball_height) - paddle_r_y
        if dy > 0 and dy < paddle_height + ball_height:
            sound_hit()
            dy = dy / (paddle_height+ball_height)
            ball_x = max_x - ball_width
            angle = math.radians(90-60+dy*120)
            ball_vx = -math.sin(angle) * ball_speed
            ball_vy = -math.cos(angle) * ball_speed
            print("dy: ",dy, "vx: ", ball_vx)
        else:
            point_to("left")
            ball_x = max_x >> 1
            ball_y = max_y >> 1
            ball_vx = -ball_vx
    elif ball_x <= min_x + paddle_width:
        dy = (ball_y + ball_height) - paddle_l_y
        if dy > 0 and dy < paddle_height + ball_height:
            sound_hit()
            dy = dy / (paddle_height+ball_height)
            ball_x = min_x + paddle_width
            angle = math.radians(90-60+dy*120)
            ball_vx = math.sin(angle) * ball_speed
            ball_vy = -math.cos(angle) * ball_speed
        else:
            point_to("right")
            ball_x = max_x >> 1
            ball_y = max_y >> 1
            ball_vx = -ball_vx  
    display.fill_rect(int(ball_x),int(ball_y),ball_width,ball_height,1)
    display.show()
    time.sleep(0.05)

logoSmallBuff = customToBuff(bytearray(base64.b64decode(logoSmallB)))
logoLargeBuff = customToBuff(bytearray(base64.b64decode(logoLargeB)))
logoPong = customToBuff(bytearray(base64.b64decode(logoPongB)))
logoPongI = customToBuff(bytearray(base64.b64decode(logoPongIB)))

while True:
    if mode == mode_playing:
        play_frame()
    elif mode == mode_init:
        intro()
        mode = mode_playing
    elif mode == mode_game_over:
        time.sleep(0.1)
        if play_button.value():
            intro()
            mode=mode_playing
    


