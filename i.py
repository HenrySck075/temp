import os, regex as re, requests
epicpath="C:/Users/HenryS/Desktop/Misc. content/actual homework lol/images"
downpath="C:/Users/HenryS/Desktop/Misc. content/pixiv_restored"
#     "error":false,
#     "message":"",
#     "body":{
#         "illustId":"94395744",
#         "illustTitle":"\ud83d\udc40",
#         "illustComment":"",
#         "id":"94395744",
#         "title":"\ud83d\udc40",
#         "description":"",
#         "illustType":0,
#         "createDate":"2021-11-26T17:23:00+00:00",
#         "uploadDate":"2021-11-26T17:23:00+00:00",
#         "restrict":0,
#         "xRestrict":0,"sl":2,
#         "urls":{
#             "mini":"https:\/\/i.pximg.net\/c\/48x48\/img-master\/img\/2021\/11\/27\/02\/23\/27\/94395744_p0_square1200.jpg",
#             "thumb":"https:\/\/i.pximg.net\/c\/250x250_80_a2\/img-master\/img\/2021\/11\/27\/02\/23\/27\/94395744_p0_square1200.jpg",
#             "small":"https:\/\/i.pximg.net\/c\/540x540_70\/img-master\/img\/2021\/11\/27\/02\/23\/27\/94395744_p0_master1200.jpg",
#             "regular":"https:\/\/i.pximg.net\/img-master\/img\/2021\/11\/27\/02\/23\/27\/94395744_p0_master1200.jpg",
#             "original":"https:\/\/i.pximg.net\/img-original\/img\/2021\/11\/27\/02\/23\/27\/94395744_p0.jpg"
#         }

print("enter loop")
for i in os.listdir(epicpath):
    if "SPOILER_" in i:continue #i dont want to
    if (r:=re.search(" (.*)_p0_(.*)1200" if i.count('_') == 3 else " (.*)_p0",i))!=None:
        imgid=r.group(0)
        head={"x-user-id":76179633,"referer":f"https://www.pixiv.net/en/artworks/{imgid}"}
        resp=requests.get(f'https://www.pixiv.net/ajax/illust/{imgid}?ref=https%3A%2F%2Fwww.pixiv.net%2F&lang=en&version=a396fb43977c854f88d11c71cd0fbac4d20d42d8').json()
        if not resp['error']:
        input(" ")
        #illust.download(downpath,filename=f"{imgid}_p0")