#objective: create a 60fps original resolution recreation of "Bad Apple" in Minecraft in any way
#execute store result score @p dash run data get entity @e[tag=topleft] Pos
import math,cv2
from PIL import Image
from copy import deepcopy
from typing import Dict,List
videoFile='./crop/out00.mp4'
mcfunctionFile='./datapacks/data/apple/functions/place.mcfunction'

mcfunctionContent=[
    'execute at @e[tag=topleft] run summon armor_stand ~ ~-6 150 {{Tags:["cb"]}}',
    "execute at @e[tag=cb] run setblock ~ ~-1 ~ barrier replace"
]
cmdPreset:Dict[str,str|List[str]]={
    "cmd":'\n'.join([
        "execute at @e[tag=cb] align xyz run setblock ~-{x} ~{y} ~{z} command_block replace",
        "execute at @e[tag=cb] align xyz run data modify block  ~-{x} ~{y} ~-{z} Command set value 'execute at @e[tag=topleft] run fill ~-{x1} ~2 ~-{z1} ~-{x2} ~2 ~-{z2} {block}'",
        "execute at @e[tag=cb] align xyz run setblock ~-{x} ~{y2} ~{z} redstone_wire[east=side,west=side,south=side] replace"]),
    "next":'\n'.join([
        "execute at @e[tag=cb] align xyz run setblock ~ ~{y1} ~-{z1} repeater[facing={facing},delay={delay}] replace",
        "execute at @e[tag=cb] align xyz run setblock ~ ~{y2} ~-{z2} barrier replace",
        "execute at @e[tag=cb] align xyz run setblock ~ ~{y1} ~-{z1} redstone_wire[east=up,west=up] replace"]),
    #thay x,z mỗi lần dùng
    "moveLayer":[
        "execute at @e[tag=cb] align xyz run setblock ~-{x} ~{y2} ~-{z} barrier replace\nexecute at @e[tag=cb] align xyz run setblock ~-{x} ~{y} ~-{z} redstone_wire[{we}=up,south=side] replace\n",
        "execute at @e[tag=cb] align xyz run setblock ~-{x} ~{y2} ~-{z} barrier replace\nexecute at @e[tag=cb] align xyz run setblock ~-{x} ~{y} ~-{z} redstone_wire[south=up,{we}=side] replace\n",
        "execute at @e[tag=cb] align xyz run setblock ~-{x} ~{y2} ~-{z} barrier replace\nexecute at @e[tag=cb] align xyz run setblock ~-{x} ~{y} ~-{z} redstone_wire[{we}=up,south=side] replace\n",
        "execute at @e[tag=cb] align xyz run setblock ~-{x} ~{y2} ~-{z} barrier replace\nexecute at @e[tag=cb] align xyz run setblock ~-{x} ~{y} ~-{z} redstone_wire[north=up,{we}=side] replace\n",
    ],
    "monika": "execute at @e[tag=cb] run setblock ~ ~{y2} ~-{z2} barrier replace\nexecute at @e[tag=cb] run setblock ~ ~{y1} ~-{z1} redstone_wire[east=side,west=side] replace"
}
x,y,z=0,0,-150
direction=0#right, 1 for left
def fill_scale(array,pos,color):
    "pxArray, pixel pos, color (0,1)"
    maxWidth,maxHeight=len(array),len(array[0])
    maxMatchW=0
    maxMatchH=0
    xoff,yoff=1,0
    skippo=[]
    for h in range(pos[1],maxHeight):
        if array[pos[0]+1][h+yoff]!=color and xoff==1: break
        if array[pos[0]][h+yoff]==color:
            xoff=0
            for w in range(pos[0],maxWidth):
                if array[w+xoff][h+yoff]==color:
                    skippo.append((w+xoff,h+yoff))
                    maxMatchW+=1
                elif xoff-1<maxMatchW:
                    maxMatchW=xoff-1
                else:
                    break
                xoff+=1
            yoff+=1
        else:
            maxMatchH=yoff
    return (pos[0],maxMatchW),(pos[1],maxMatchH),skippo

def moveLayer(pos:List[tuple],side:str):
    for i in range(4):
        po=pos[i]
        mcfunctionContent.append(cmdPreset["moveLayer"][i].format(x=x+po[0],y=y+po[1],y2=y+po[1]+1,z=z+po[2],we=side))
cap = cv2.VideoCapture(videoFile) # says we capture an image from a webcam
width  = math.floor(cap.get(3))
height = math.floor(cap.get(4))
blocks=['white_wool','gray_wool','black_wool']
last_pxArray=[]
repeatedFrames=1
while(cap.isOpened()):
    ret,cv2_im = cap.read()
    if ret :
        converted = cv2.cvtColor(cv2_im,cv2.COLOR_BGR2RGB)

        im = Image.fromarray(converted)
        pxArray=[]
        #please help me
        for w in range(im.width):
            lay=[]
            for h in range(im.height):
                c=sum(im.getpixel((w,h)) > 128*3)
                if c>60*3 and c<190*3: color=1#gray
                elif c<190*3:color=2#black
                else:color=0#white
                lay.append(color)
            pxArray.append(lay)
        skip=[]
        z+=1;x=0
        if repeatedFrames==4:
            mcfunctionContent.append(cmdPreset["next"].format(z1=z,z2=z+1,y1=y-1,y2=y,facing='east' if direction==0 else 'west',delay=4))
            mcfunctionContent.append(cmdPreset["monika"].format(z1=z+1,z2=z+2,y1=y-1,y2=y))
            z+=2
            repeatedFrames=1
        for w,pw in enumerate(pxArray):
            for h,ph in enumerate(pw):
                if ph != last_pxArray[w][h] and (w,h) not in skip:
                    mcfunctionContent.append(cmdPreset["next"].format(z1=x,z2=z+1,y1=y,y2=y+1,facing='east' if direction==0 else 'west',delay=repeatedFrames))
                    d1,d2,skipext=fill_scale(pxArray,(w,h),ph)
                    mcfunctionContent.append(cmdPreset["cmd"].format(x=x,y=y,y2=y+1,z=z+2,x1=d1[0],z1=d1[0],x2=d2[0],z2=d2[0]),block=blocks[color])
                    skip.extend(skipext)
                    x+=1;z+=2
                elif last_pxArray==pxArray:repeatedFrames+=1
        if z>=150:
            moveLayer([(0,0,1),(1,-1,2),(1,-2,3),(0,-3,3)],'east')
            y-=3
            mcfunctionContent.append(cmdPreset["monika"])
        last_pxArray=deepcopy(pxArray)
    else:break

with open(mcfunctionFile,'w') as w:
    w.write('\n'.join(mcfunctionContent))
