# -*- coding: utf-8 -*-
from linepys import *
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from gtts import gTTS
import time,random,sys,json,codecs,urllib,urllib3,requests,threading,glob,os,subprocess,multiprocessing,re,ast,shutil,calendar,tempfile,string,six,timeago,calendar
from random import randint

mulas = time.time()

#ki = LineClient()
ki = LineClient(authToken='EoFF1rZQGdW2FTO4Vmz7.Jk6ykRXKF0y9NrUQ5HonvW.u6I9vxOYn8Uy1+ST+K8P2AvwI9VPB96mzCmRE9zw7T0=')
ki.log("Auth Token : " + str(ki.authToken))
poll = LinePoll(ki)
mid = ki.getProfile().mid
admsa = "uc11acad2da3f37a2b64e2452cbbca2c5"
kitsune = "uef60668fda1d37ede35875ab150171a7"
with open('1.json', 'r') as fp:
    wait = json.load(fp)
with open('2.json', 'r') as fp:
    wait2 = json.load(fp)
    
mimic = {
    "status":False,
    "target":{},
    "setkey":"",
    "pap":"http://otaku-w9pxf76zfsktmx3e.stackpathdns.com/wp-content/uploads/2017/08/Sarada-1024x576.png",
    "Autochat":False,
    }

agent = {'User-Agent' : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
base_url = "http://api.genius.com"
headers = {'Authorization': 'TQkoT8_dOQ7j2NEvnEJwHDOGJfOPr3RFb8Dc3-IXlOnPN4cy0zuq0fvSkWcNlJDL'}
artist_name = "The Decemberists"
apimovie = "1ed4e17d7cb07549e8a7884c5dde6577"
apiyoutube = "AIzaSyAF-_5PLCt8DwhYc7LBskesUnsm1gFHSP8"

def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            page = page[end_content:]
    return items
def waktu(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    return '%02d Jam %02d Menit %02d Detik' % (hours, mins ,secs)

# Receive messages from LinePoll

# Receive messages from LinePoll
def NOTIFIED_INVITE_INTO_GROUP(op):
    if mid in op.param3:
        G = ki.getGroup(op.param1)
        if wait["autoJoin"] == True:
            if len(G.kitsunemembers) <= wait["Members"]:
                ki.rejectGroupInvitation(op.param1)
            else:
                ki.acceptGroupInvitation(op.param1)
        else:
            pass                   
        if len(G.kitsunemembers) <= wait["Members"]:
            ki.rejectGroupInvitation(op.param1)
    else:
        if op.param1 in wait["autoCancel"]:
            if op.param2 in wait["bots"]:
                pass
            else:
                X = ki.getGroup(op.param1)
                if X.invitee is not None:
                    gInviMids = [contact.mid for contact in X.invitee]
                    ki.cancelGroupInvitation(op.param1, gInviMids)
        else:
            try:
                if op.param3 in wait["blacklist"]:
                    random.choice(P2).cancelGroupInvitation(op.param1, [op.param3])
            except:
                if op.param3 in wait["blacklist"]:
                    ki.cancelGroupInvitation(op.param1, [op.param3])
poll.addOpInterruptWithDict({
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})
def SEND_MESSAGE(op):
        msg = op.message
        kitxt = msg.text
        msg_id = msg.id
        kitsune = msg.to
        saya = msg._from
        if msg.contentType == 1:
                if wait["ChangeDP"] == True:
                    try:
                        ki.downloadObjectMsg(msg_id,'path','dataSeen/adityab.png')
                        ki.updateProfilePicture('dataSeen/adityab.png')
                        ki.sendMessage(kitsune, " 「 Profile 」\nType: Change Profile Picture\nStatus: Profile Picture Hasbeen change♪")
                    except Exception as e:
                        ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
                    wait["ChangeDP"] = False
                    backupjson_1()
                if wait["ChangeGDP"] == True:
                    try:
                        ki.downloadObjectMsg(msg_id,'path','dataSeen/adityab.png')
                        ki.updateGroupPicture(kitsune,'dataSeen/adityab.png')
                        ki.sendMessage(kitsune, " 「 Group 」\nType: Change Cover Group\nStatus: Cover Group Hasbeen change♪")
                    except Exception as e:                         ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
                    wait["ChangeGDP"] = False
                    backupjson_1()
                if wait["Addimage"] == True:
                    try:
                        ki.downloadObjectMsg(msg_id,'path','dataSeen/%s.jpg' % wait["Img"])
                        ki.sendMessage(kitsune, " 「 Picture 」\nType: Add Picture\nStatus: Success Add Picture♪")
                    except Exception as e:
                        ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
                    wait["Img"] = {}
                    wait["Addimage"] = False
                    backupjson_1()
        if msg.contentType == 16:
            ki.likePost(msg.contentMetadata["mid"], msg.contentMetadata["postId"], likeType=1001)
        if msg.contentType == 7:
            if wait["Addsticker"] == True:
                try:
                    wait["Sticker"][wait["Img"]] = msg.contentMetadata
                    ki.sendMessage(kitsune, " 「 Sticker 」\nSTKID: "+msg.contentMetadata['STKID']+"\nSTKPKGID: "+msg.contentMetadata['STKPKGID']+"\nSTKVER: "+msg.contentMetadata['STKVER'])
                except Exception as e:
                    ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
                wait["Img"] = {}
                wait["Addsticker"] = False
                backupjson_1()
        if msg.contentType == 13:
                if wait["wwhitelist"] == True:
                    addwl(kitsune,msg.contentMetadata["mid"])
                    wait["wwhitelist"] = False
                    backupjson_1()
                if wait["dwhitelist"] == True:
                    delwl(kitsune,msg.contentMetadata["mid"])
                    wait["dwhitelist"] = False
                    backupjson_1()
                if wait["wblacklist"] == True:
                    addbl(kitsune,msg.contentMetadata["mid"])
                    wait["wblacklist"] = False
                    backupjson_1()
                if wait["dblacklist"] == True:
                    delbl(kitsune,msg.contentMetadata["mid"])
                    wait["dblacklist"] = False
                    backupjson_1()
                if msg.to in wait["kitsunecontact"]:
                    msg.contentType = 0
                    ki.contactsa(kitsune,"",msg.contentMetadata["mid"]) 
    # Check content only text message
        if msg.contentType == 0:
            if kitxt.lower() == wait["setkey"]+' help' or kitxt.lower() == wait["setkey"]+'help':help(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' list groups' or kitxt.lower() == wait["setkey"]+'list groups':ki.listgroup(kitsune, '')
            if kitxt.lower() == wait["setkey"]+' list members' or kitxt.lower() == wait["setkey"]+'list members':ki.listmember(kitsunewb )
            if kitxt.lower() == wait["setkey"]+' me' or kitxt.lower() == wait["setkey"]+'me':ki.me(kitsune,saya)
            if kitxt.lower() == wait["setkey"]+'abort' or kitxt.lower() == wait["setkey"]+' abort':aborted(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'set' or kitxt.lower() == wait["setkey"]+' set':set(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' timeline' or kitxt.lower() == wait["setkey"]+'timeline':timelune(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' urban' or kitxt.lower() == wait["setkey"]+'urban':urban(kitsune)
            if kitxt.lower() == wait["setkey"]+' youtube' or kitxt.lower() == wait["setkey"]+'youtube':youtube(kitsune)
            if kitxt.lower() == wait["setkey"]+' lurk' or kitxt.lower() == wait["setkey"]+'lurk':lurk(kitsune)
            if kitxt.lower() == wait["setkey"]+' keep' or kitxt.lower() == wait["setkey"]+'keep':keep(kitsune)
            if kitxt.lower() == wait["setkey"]+' image' or kitxt.lower() == wait["setkey"]+'image':image(kitsune)
            if kitxt.lower() == wait["setkey"]+'steal' or kitxt.lower() == wait["setkey"]+' steal':steal(kitsune)
            if kitxt.lower() == wait["setkey"]+'wikipedia' or kitxt.lower() == wait["setkey"]+' wikipedia':wikipedia(kitsune)
            if kitxt.lower() == wait["setkey"]+'movie' or kitxt.lower() == wait["setkey"]+' movie':movie(kitsune)
            if kitxt.lower() == wait["setkey"]+'music' or kitxt.lower() == wait["setkey"]+' music':lagulagu(kitsune)
            if kitxt.lower() == wait["setkey"]+'profile' or kitxt.lower() == wait["setkey"]+' profile':profdetail(kitsune)
            if kitxt.lower() == wait["setkey"]+'ikkeh' or kitxt.lower() == wait["setkey"]+' ikkeh':copy(kitsune)
            if kitxt.lower() == wait["setkey"]+'ikkeh setdefault' or kitxt.lower() == wait["setkey"]+' ikkeh setdefault':setbackupprofile(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'pp' or kitxt.lower() == wait["setkey"]+' pp':ki.stealpp(kitsune,saya)
            if kitxt.lower() == wait["setkey"]+' autoadd' or kitxt.lower() == wait["setkey"]+'autoadd':autoadd(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' list' or kitxt.lower() == wait["setkey"]+'list':list(kitsune)
            if kitxt.lower() == wait["setkey"]+' quote' or kitxt.lower() == wait["setkey"]+'quote':quote(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'1cak' or kitxt.lower() == wait["setkey"]+' 1cak':wancak(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' about' or kitxt.lower() == wait["setkey"]+'about':ki.about(kitsune,saya)
            if kitxt.lower() == wait["setkey"]+'debug' or kitxt.lower() == wait["setkey"]+' debug':debug(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'get note' or kitxt.lower() == wait["setkey"]+' get note':ki.GroupPost(kitsune)
            if kitxt.lower() == wait["setkey"]+' myticket' or kitxt.lower() == wait["setkey"]+'myticket':ki.myticket(kitsune)
            if kitxt.lower() == wait["setkey"]+' mention on' or kitxt.lower() == wait["setkey"]+'mention on':antimentionon(kitsune,"")
            if kitxt.lower() == wait["setkey"]+'sampul' or kitxt.lower() == wait["setkey"]+' sampul':ki.stealcover(kitsune,saya)
            if kitxt.lower() == wait["setkey"]+' mention off' or kitxt.lower() == wait["setkey"]+'mention off':antimentionoff(kitsune,"")
            if kitxt.lower() == wait["setkey"]+'steal cover' or kitxt.lower() == wait["setkey"]+' steal cover':ki.stealcover(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+' steal pp' or kitxt.lower() == wait["setkey"]+'steal pp':ki.stealpp(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'ikkeh off' or kitxt.lower() == wait["setkey"]+' ikkeh off':ki.backupmyprofile(kitsune)
            if kitxt.lower() == wait["setkey"]+' autoadd on' or kitxt.lower() == wait["setkey"]+'autoadd on':autoaddon(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' autoadd off' or kitxt.lower() == wait["setkey"]+'autoadd off':autoaddoff(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'speed' or kitxt.lower() == wait["setkey"]+' speed':ki.speed(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'stacks' or kitxt.lower() == wait["setkey"]+' stacks':ki.stackspeed(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'changedp' or kitxt.lower() == wait["setkey"]+' changedp':changedp(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'changedp group' or kitxt.lower() == wait["setkey"]+' changedp group':ChangeGDP(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' list pict' or kitxt.lower() == wait["setkey"]+'list pict':listpict(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' list sticker' or kitxt.lower() == wait["setkey"]+'list sticker':liststicker(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'wlall' or kitxt.lower() == wait["setkey"]+' wlall':appendData(kitsune,'',wait['bots'])
            if kitxt.lower() == wait["setkey"]+'blall' or kitxt.lower() == wait["setkey"]+' blall':appendData(kitsune,'',wait['blacklist'])
            if kitxt.lower() == wait["setkey"]+'delwlall' or kitxt.lower() == wait["setkey"]+' delwlall':removeData(kitsune,'',wait['bots'])
            if kitxt.lower() == wait["setkey"]+'delblall' or kitxt.lower() == wait["setkey"]+' delblall':removeData(kitsune,'',wait['blacklist'])
            if kitxt.lower() == wait["setkey"]+' instagram' or kitxt.lower() == wait["setkey"]+'instagram':instagram(kitsune)
            if kitxt.lower() == wait["setkey"]+'cancel' or kitxt.lower() == wait["setkey"]+' cancel':ki.cancelinvite(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' autoadd msg clear' or kitxt.lower() == wait["setkey"]+'autoadd msg clear':autoaddmsgclear(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' getid' or kitxt.lower() == wait["setkey"]+'getid':getinformation(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+' protect on' or kitxt.lower() == wait["setkey"]+'protect on':protecton(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' protect off' or kitxt.lower() == wait["setkey"]+'protect off':protectoff(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' cancel on' or kitxt.lower() == wait["setkey"]+'cancel on':cancelon(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' cancel off' or kitxt.lower() == wait["setkey"]+'cancel off':canceloff(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' contact on' or kitxt.lower() == wait["setkey"]+'contact on':contacton(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' contact off' or kitxt.lower() == wait["setkey"]+'contact off':contactoff(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' qr on' or kitxt.lower() == wait["setkey"]+'qr on':qron(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' qr off' or kitxt.lower() == wait["setkey"]+'qr off':qroff(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' autoread on' or kitxt.lower() == wait["setkey"]+'autoread on':autoreadon(kitsune,"")
            if kitxt.lower() == wait["setkey"]+' autoread off' or kitxt.lower() == wait["setkey"]+'autoread off':autoreadoff(kitsune,"")
            if kitxt.lower() == wait["setkey"]+'list friends' or kitxt.lower() == wait["setkey"]+' list friends':ki.listfriend(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'mytimeline' or kitxt.lower() == wait["setkey"]+' mytimeline':ki.mytimeline(kitsune,saya)
            if kitxt.lower() == wait["setkey"]+'get timeline' or kitxt.lower() == wait["setkey"]+' get timeline':ki.gettimeline(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'mimic' or kitxt.lower() == wait["setkey"]+' mimic':mimiclisted(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'whitelist' or kitxt.lower() == wait["setkey"]+' whitelist':whitelist(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'blacklist' or kitxt.lower() == wait["setkey"]+' blacklist':blacklist(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'ourl' or kitxt.lower() == wait["setkey"]+' ourl':ki.openqr(kitsune,'')
            if kitxt.lower() == wait["setkey"]+'curl' or kitxt.lower() == wait["setkey"]+' curl':ki.closeqr(kitsune,'')
            if kitxt.lower() == wait["setkey"]+' crash' or kitxt.lower() == wait["setkey"]+'crash':ki.crash(kitsune)
            if kitxt.lower() == wait["setkey"]+' gift' or kitxt.lower() == wait["setkey"]+'gift':ki.giftmessage(kitsune)
            if kitxt.lower() == wait["setkey"]+' meme' or kitxt.lower() == wait["setkey"]+'meme':ki.memelist(kitsune)
            if kitxt.lower() == wait["setkey"]+' youtube new' or kitxt.lower() == wait["setkey"]+'youtube new':ki.youtubenew(kitsune)
            if kitxt.lower() == wait["setkey"]+' mimic on' or kitxt.lower() == wait["setkey"]+'mimic on':mimicon(kitsune)
            if kitxt.lower() == wait["setkey"]+' mimic off' or kitxt.lower() == wait["setkey"]+'mimic off':mimicoff(kitsune)
            if kitxt.lower() == wait["setkey"]+'url' or kitxt.lower() == wait["setkey"]+' url':ki.urlqr(kitsune)
            if kitxt.lower() == wait["setkey"]+'addbl' or kitxt.lower() == wait["setkey"]+' addbl':addbl(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'delbl' or kitxt.lower() == wait["setkey"]+' delbl':delbl(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'addwl' or kitxt.lower() == wait["setkey"]+' addwl':addwl(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'delwl' or kitxt.lower() == wait["setkey"]+' delwl':delwl(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'addml' or kitxt.lower() == wait["setkey"]+' addml':addmimic(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'delml' or kitxt.lower() == wait["setkey"]+' delml':delmimic(kitsune,kitsune)
            if kitxt.lower() == wait["setkey"]+'list block' or kitxt.lower() == wait["setkey"]+' list block':ki.listblock(kitsune)
            if kitxt.lower() == wait["setkey"]+'kill' or kitxt.lower() == wait["setkey"]+' kill':random.choice(P1).killbl(kitsune)
            if kitxt.lower() == 'mykey':mykey(kitsune,'')
            if kitxt.lower() == 'mykey off':mykeyoff(kitsune,'')
            if kitxt.lower() == 'mykey reset':mykeyreset(kitsune,'')
            if kitxt.lower() == 'ki1':ki.sendContact(kitsune,ki1mid)
            if kitxt.lower() == 'ki2':ki.sendContact(kitsune,ki2mid)
            if kitxt.lower() == 'ki3':ki.sendContact(kitsune,ki3mid)
            if kitxt.lower() == 'ki4':ki.sendContact(kitsune,ki4mid)
            if kitxt.lower() == 'ki5':ki.sendContact(kitsune,ki5mid)
            if kitxt.lower() == 'ki6':ki.sendContact(kitsune,ki6mid)
            if kitxt.lower() == 'ki7':ki.sendContact(kitsune,ki7mid)
            if kitxt.lower() == 'ki8':ki.sendContact(kitsune,ki8mid)
            if kitxt.lower() == 'ki9':ki.sendContact(kitsune,ki9mid)
            if kitxt.lower() == 'ki10':ki.sendContact(kitsune,ki10mid)
            if kitxt.lower() == 'ki11':ki.sendContact(kitsune,ki11mid)
            if kitxt.lower() == 'ki12':ki.sendContact(kitsune,ki12mid)
            if kitxt.lower() == 'ki13':ki.sendContact(kitsune,ki13mid)
            if kitxt.lower() == 'ki14':ki.sendContact(kitsune,ki14mid)
            if kitxt.lower() == 'ki15':ki.sendContact(kitsune,ki15mid)
            if kitxt.lower() == 'ki16':ki.sendContact(kitsune,ki16mid)
            if kitxt.lower() == 'ki17':ki.sendContact(kitsune,ki17mid)
            if kitxt.lower() == 'ki18':ki.sendContact(kitsune,ki18mid)
            if kitxt.lower() == 'ki19':ki.sendContact(kitsune,ki19mid)
            if kitxt.lower() == 'ki21':ki.sendContact(kitsune,ki21mid)
            if kitxt.lower() == 'ki20':ki.sendContact(kitsune,ki20mid)
            if kitxt.lower() == wait["setkey"]+' list protect' or kitxt.lower() == wait["setkey"]+'list protect':
                gid = ki.getGroupIdsJoined()
                ret = " 「 Groups 」\nList Protection groups:"
                no = 0
                total = len(gid)
                for group in gid:
                    G = ki.getGroup(group)
                    member = len(G.kitsunemembers)
                    no += 1
                    if group in wait["kitsuneprotection"]:
                        md="[1] "
                    else:
                        md="[0] "
                    if group in wait["kitsuneurl"]:
                        md+="[1] "
                    else:
                        md+="[0] "
                    if group in wait["autoCancel"]:
                        md+="[1] "
                    else:
                        md+="[0] "
                    ret += "\n" + str(no) + ". " + G.name +" "+md
                ki.sendMessage(kitsune,ret+"\n[Kick] [Link] [Invitation] [1|ON] [0|OFF]")
            if kitxt.lower() == wait["setkey"]+' bot' or kitxt.lower() == wait["setkey"]+'bot':
                for mi_d in Botsa:
                    ki.sendContact(kitsune,mi_d)
            if kitxt.lower().startswith(wait["setkey"]+'broadcast 3') or kitxt.lower().startswith(wait["setkey"]+' broadcast 3'):
                separate = kitxt.split("\n")
                text = kitxt.replace(separate[0]+"\n","")
                a = ki.getGroupIdsJoined()
                for i in a:
                    G = ki.getGroup(i)
                    if len(G.kitsunemembers) > wait["Members"]:
                        ki.sendMessage(i,text)
            if kitxt.lower().startswith(wait["setkey"]+'ytdl') or kitxt.lower().startswith(wait["setkey"]+' ytdl'):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                cond = text.split("|")
                search = str(cond[0])
                r = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q="+search+"&type=video&key=AIzaSyAF-_5PLCt8DwhYc7LBskesUnsm1gFHSP8")
                data = r.text
                data = json.loads(data)
                if len(cond) == 2:
                    try:
                        num = int(cond[1])
                        music = data["items"][num - 1]
                        b= "https://youtu.be/"+str(music["id"]['videoId'])
                        import pafy
                        v = pafy.new(b)
                        ki.sendImageWithURL(kitsune,v.thumb)
                        a= " 「 Youtube 」\nType: Youtube Download\n"
                        a+= str(v)
                        no = 0
                        for music in v.streams[0:5]:
                            no += 1
                            a+="\n   " + str(no) + ". "+ki.google_url_shorten(music.url) +"\n       "+str(music.quality)+" "+music.extension+"\n"
                        a+="Status: Success Get Link"
                        ki.sendMessage(kitsune, a)
                    except Exception as e:
                        ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
            if kitxt.lower() == wait["setkey"]+'addwl on' or kitxt.lower() == wait["setkey"]+' addwl on':
                wait["wwhitelist"] = True
                backupjson_1()
                ki.sendMessage(kitsune," 「 Whitelist 」\nType: Add Whitelist\nStatus: Turned ON\nSend a contact to add into whitelist♪")
            if kitxt.lower() == wait["setkey"]+'delbl on' or kitxt.lower() == wait["setkey"]+' delbl on':
                wait["dblacklist"] = True
                backupjson_1()
                ki.sendMessage(kitsune," 「 Blacklist 」\nType: Delete Blacklist\nStatus: Turned ON\nSend a contact to delete from blacklist♪")
            if kitxt.lower() == wait["setkey"]+'delwl on' or kitxt.lower() == wait["setkey"]+' delwl on':
                wait["dwhitelist"] = True
                backupjson_1()
                ki.sendMessage(kitsune," 「 Whitelist 」\nType: Delete Whitelist\nStatus: Turned ON\nSend a contact to delete from whitelist♪")
            if kitxt.lower() == wait["setkey"]+'addbl on' or kitxt.lower() == wait["setkey"]+' addbl on':
                wait["wblacklist"] = True
                backupjson_1()
                ki.sendMessage(kitsune," 「 Blacklist 」\nType: Add Blacklist\nStatus: Turned ON\nSend a contact to add into blacklist♪")
            if kitxt.lower().startswith(wait["setkey"]+'meme') or kitxt.lower().startswith(wait["setkey"]+' meme'):
                separate = kitxt.split("|")
                text = separate[1]
                hmm = separate[2]
                r = requests.get("https://api.imgflip.com/get_memes")
                data = r.text
                data = json.loads(data)
                try:
                    num = int(separate[3])
                    music = data['data']['memes'][num - 1]
                    meme = int(music['id'])
                    api = pyimgflip.Imgflip(username='adityanugraha', password='anjinglu1')
                    result = api.caption_image(meme, text,hmm)
                    ki.jangantag(kitsune,' 「 Meme 」\nStatus: Waiting...','Type: Meme Generator',saya,"Request: Get Meme "+str(music['name']))
                    ki.sendImageWithURL(kitsune,result['url'])
                except Exception as e:
                    ki.taagsaya(kitsune,"Type: Meme Generator",saya,str(e))
            if kitxt.lower() == wait["setkey"]+'mayhem' or kitxt.lower() == wait["setkey"]+' mayhem':
                a = []
                b = ki.getGroup(kitsune)
                for i in b.kitsunemembers:
                    if i.mid not in wait["bots"] and i.mid not in Botsa:
                        a.append(i.mid)
                ki.sendMessage(kitsune," 「 Mayhem 」\nMayhem is STARTING♪\n'abort' to abort♪""")
                ki.sendMessage(kitsune," 「 Mayhem 」\n %i victims shall yell hul·la·ba·loo♪\n/ˌhələbəˈlo͞o,ˈhələbəˌlo͞o/" % len(a))
                for c in a:
                    random.choice(P1).kickoutFromGroup(kitsune,[c])
            if kitxt.lower().startswith(wait["setkey"]+'image ') or kitxt.lower().startswith(wait["setkey"]+' image '):
                if msg.text.lower().startswith(wait["setkey"]+' image '):
                    foo = wait["setkey"]+' image '
                else:
                    foo = wait["setkey"]+'image '
                key = len(foo)
                key1 = msg.text[key:]
                text = key1.replace(" ","%20")
                url = 'https://www.google.com/search?hl=en&biw=1366&bih=659&tbm=isch&sa=1&ei=vSD9WYimHMWHvQTg_53IDw&q=' + text
                raw_html =  (download_page(url))
                items = []
                items = items + (_images_get_all_items(raw_html))
                path = random.choice(items)
                ki.jangantag(kitsune,' 「 Image 」\nStatus: Waiting...','Type: Image Search',saya,"Request: Get Image "+str(text.replace("%20"," ").title()))
                try:
                    start = time.time()
                    ki.sendImageWithURL(kitsune,path)
                    elapsed_time = time.time() - start
                    adits= (1+2,11+2,2+2,12+2,3+2,13+2,4+2,14+2,5+2,15+2,6+2,16+2,7+2,17+2,8+2,18+2,9+2,19+2,10+2,20+2,21+2,22+2,23+2,24+2,25+2,26+2,27+2,28+2,29+2,30+2,31+2,32+2,33+2,34+2,35+2,36+2,37+2,38+2,39+2,40+2)
                    ki.sendMessage(kitsune," 「 Image 」\nStatus: Success\nType: Image Search\nTarget: #"+str(random.choice(adits))+" from #"+str(len(items))+"\nTaken: %.10f" % (elapsed_time/8))
                except Exception as e:
                    ki.taagsaya(kitsune,"Type: Image Search",saya,str(e))
            if kitxt.lower().startswith(wait["setkey"]+'keep ') or kitxt.lower().startswith(wait["setkey"]+' keep '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 1:ki.keeploli(kitsune,kitsunetext,mid)
                if len(kitsunesplit) == 2:ki.keeplolidata(kitsune,kitsunetext,saya,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'youtube ') or kitxt.lower().startswith(wait["setkey"]+' youtube '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 1:ki.youtubelist(kitsune,kitsunetext,mid)
                if len(kitsunesplit) == 2:ki.youtubelistdata(kitsune,kitsunetext,saya,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'wikipedia ') or kitxt.lower().startswith(wait["setkey"]+' wikipedia '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 1:ki.wikipedialist(kitsune,kitsunetext,saya)
                if len(kitsunesplit) == 2:ki.wikipedialistdata(kitsune,kitsunetext,saya,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'movie ') or kitxt.lower().startswith(wait["setkey"]+' movie '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 1:ki.movielist(kitsune,kitsunetext,saya)
                if len(kitsunesplit) == 2:ki.movielistdata(kitsune,kitsunetext,saya,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'jadwal ') or kitxt.lower().startswith(wait["setkey"]+' jadwal '):
                separate = kitxt.split("shalat ")
                text = kitxt.replace(separate[0] + "shalat ","")
                ki.jadwalshalat(kitsune,text)
            if kitxt.lower().startswith(wait["setkey"]+'deviant ') or kitxt.lower().startswith(wait["setkey"]+' deviant '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                cond = text.split("|")
                search = str(cond[0])
                r = requests.get("https://www.deviantart.com/oauth2/token?grant_type=client_credentials&client_id=7178&client_secret=d6e59d074e9d6c38e5b7b83f5bfb7c00")
                token = r.text
                token = json.loads(token)
                channel = str(token['access_token'])
                r = requests.get("https://www.deviantart.com/api/v1/oauth2/browse/popular?q="+search+"&timerange=1month&limit=100&mature_content=true&access_token="+channel)
                data = r.text
                data = json.loads(data)
                if len(cond) == 1:
                    if data['results'] != []:
                        no = 0
                        a= " 「 Image 」\nType: Search Image"
                        for music in data['results']:
                            no += 1
                            a+= "\n" + str(no) + ". " + music['title']
                        a+= "\nUsage:%s image %s|num" %(wait["setkey"], str(search))
                        ki.sendMessage(kitsune,a)
                    else:
                        ki.sendMessage(kitsune,"「 Image 」\nStatus: Error\n" + str(search)+" nothing in image")
                if len(cond) == 2:
                    try:
                        num = int(cond[1])
                        music = data['results'][num - 1]
                        gtime = music['published_time']
                        try:
                            ki.sendImageWithURL(kitsune,music['content']['src'])
                        except:
                            ki.sendImageWithURL(kitsune,music['preview']['src'])
                        a=" 「 Image 」\nType: Search Image\nTitle: "+music['title']
                        a+="\nCategory: "+music['category']
                        a+="\nTotal Favourites: "+str(music['stats']['favourites'])
                        a+="\nTotal Comments: "+str(music['stats']['comments'])
                        a+="\nCreated at: "+str(timeago.format(gtime))
                        ki.sendMessage(kitsune,a)
                    except Exception as e:
                        ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
            if kitxt.lower().startswith(wait["setkey"]+'gn ') or kitxt.lower().startswith(wait["setkey"]+' gn '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                profiles = ki.getGroup(kitsune)
                profile = ki.getGroup(kitsune)
                profile.name = text
                ki.updateGroup(profile)
                ki.sendMessage(kitsune," 「 Group 」\nType: Change Group Name\nStatus: Success\nFrom: "+profiles.name+"\nTo: " + profile.name)
            if kitxt.lower().startswith(wait["setkey"]+'get n') or kitxt.lower().startswith(wait["setkey"]+' get n'):
                separate = kitxt.split("ote")
                text = kitxt.replace(separate[0] + "ote","")
                kitsunesplit = text.split(" ")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 2:ki.getGroupPostdetail(kitsune,kitsunetext,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'mybio') or kitxt.lower().startswith(wait["setkey"]+' mybio'):
                separate = kitxt.split("\n")
                text = kitxt.replace(separate[0]+"\n","")
                profile = ki.getProfile()
                profile.kitsuneBio = text
                ki.updateProfile(profile)
                ki.sendMessage(kitsune," 「 Profile 」\nType: Change a status message\n" + profile.kitsuneBio+"\nStatus: Success change status message")
            if kitxt.lower().startswith(wait["setkey"]+'autojoin s') or kitxt.lower().startswith(wait["setkey"]+' autojoin s'):
                separate = kitxt.split("et ")
                text = kitxt.replace(separate[0]+"et ","")
                wait["Members"] = int(text)
                backupjson_1()
                ki.sendMessage(kitsune, " 「 Autojoin 」\nType: Minim Members\nStatus: Success Set\nTo: "+text+" Members")
            if kitxt.lower().startswith(wait["setkey"]+'say@') or kitxt.lower().startswith(wait["setkey"]+' say@'):
                separate = kitxt.split("@")
                text = kitxt.replace(separate[0]+"@","")
                splt = text.split(" ")
                tts = gTTS(text=splt[1], lang=splt[0], slow=False)
                path = "pythonLine.data"
                ac = tts.save(path)
                ki.sendAudio(kitsune,path)
                os.remove(path)
            if kitxt.lower().startswith(wait["setkey"]+'myna') or kitxt.lower().startswith(wait["setkey"]+' myna'):
                separate = kitxt.split("me ")
                text = kitxt.replace(separate[0]+"me ","")
                profiles = ki.getProfile()
                profile = ki.getProfile()
                profile.kitsuneName = text
                ki.updateProfile(profile)
                ki.sendMessage(kitsune," 「 Profile 」\nType: Change Display Name\nStatus: Success\nFrom: "+profiles.kitsuneName+"\nTo: "+profile.kitsuneName)
            if msg.text.lower().startswith(wait["setkey"]+'add stick'):
                separate = kitxt.split("er ")
                text = kitxt.replace(separate[0]+"er ","")
                wait["Sticker"][text] = '%s' % text
                wait["Img"] = '%s' % text
                wait["Addsticker"] = True
                backupjson_1()
                ki.sendMessage(kitsune, " 「 Sticker 」\nSend the sticker")
            if kitxt.lower() in wait["Images"]:
                try:
                    ki.sendImage(msg.to, wait["Images"][kitxt.lower()])
                except Exception as e:
                    ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
            if kitxt.lower() in wait["Sticker"]:
                try:
                    ki.sendMessage(kitsune,text=None,contentMetadata=wait['Sticker'][kitxt.lower()], contentType=7)
                except Exception as e:
                    ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
            if kitxt.lower().startswith(wait["setkey"]+'add pi'):
                separate = kitxt.split("ct ")
                text = kitxt.replace(separate[0]+"ct ","")
                wait["Images"][text] = 'dataSeen/%s.jpg' % text
                wait["Img"] = '%s' % text
                wait["Addimage"] = True
                backupjson_1()
                ki.sendMessage(kitsune, " 「 Picture 」\nSend a Picture to save")
            if kitxt.lower().startswith(wait["setkey"]+'del pic'):
                separate = kitxt.split("t ")
                xres = kitxt.replace(separate[0]+"t ","")
                text = kitxt.replace(separate[0]+"t ","")
                del wait["Images"][xres]
                backupjson_1()
                path = os.remove("dataSeen/%s.jpg" % str(text))
                ki.sendMessage(kitsune," 「 Delete Picture 」\nSukses Delete dataSeen/%s.jpg" % str(text))
            if kitxt.lower().startswith(wait["setkey"]+'list groups'):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0]+" ","")
                cond = text.split(" ")
                if len(cond) == 2:
                    num = int(cond[1])
                    gid = ki.getGroupIdsJoined()
                    group = ki.getGroup(gid[num-1])
                    zxc = " 「 Daftar Member 」\nName: "+group.name+"\nMembers:"
                    total = "\nGroup ID:\n"+gid[num-1]+"\nLocal ID: " + str(num)
                    no = 0
                    if len(group.kitsunemembers) > 0:
                        for a in group.kitsunemembers:
                            no += 1
                            zxc += "\n   " + str(no) + ". " + a.kitsuneName
                        ki.sendMessage(kitsune,zxc + total)
            if kitxt.lower().startswith('mykey s'):
                separate = kitxt.split("et ")
                text = kitxt.replace(separate[0]+"et ","")
                a = wait["setkey"]
                wait["setkey"] = text
                backupjson_1()
                ki.sendMessage(kitsune," 「 Key 」\nType: Set key\nStatus: Success\nFrom: "+a.title()+"\nTo: "+text.title())
            if kitxt.lower().startswith(wait["setkey"]+'text '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                s = open('text.txt',"w")
                s.write(text)
                s.close()
                ki.sendFile(kitsune,'text.txt')
            if kitxt.lower().startswith(wait["setkey"]+'autoadd msg set'):
                separate = kitxt.split("\n")
                text = kitxt.replace(separate[0]+"\n","")
                wait["autoaddpesan"] = text
                backupjson_1()
                ki.sendMessage(kitsune," 「 Auto Add 」\nAuto add message has been set to:\n" + wait["autoaddpesan"])
            if kitxt.lower().startswith(wait["setkey"]+'urban ') or kitxt.lower().startswith(wait["setkey"]+' urban '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 1:ki.urbansearch(kitsune,kitsunetext,saya)
                if len(kitsunesplit) == 2:ki.urbansearchdata(kitsune,kitsunetext,saya,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'lyric ') or kitxt.lower().startswith(wait["setkey"]+' lyric '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                ki.lyric(kitsune,text)
            if kitxt.lower().startswith(wait["setkey"]+'music ') or kitxt.lower().startswith(wait["setkey"]+' music '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 1:ki.musicsearch(kitsune,kitsunetext,saya)
                if len(kitsunesplit) == 2:ki.musicsearchdata(kitsune,kitsunetext,saya,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'itunes ') or kitxt.lower().startswith(wait["setkey"]+' itunes '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                start = time.time()
                r = requests.get("https://itunes.apple.com/search?term="+kitsunetext)
                data = r.text
                data = json.loads(data)
                elapsed_time = time.time() - start
                if len(kitsunesplit) == 1:
                    if data['results'] != []:
                        no = 0
                        a = " 「 Music 」\nType: Music List"
                        for music in data['results']:
                            no += 1
                            a += "\n   " + str(no) + ". " + str(music["trackName"]) + " by " + str(music["artistName"])
                        a += "\nUsage:%s music %s|num" %(wait["setkey"], str(text))
                        ki.sendMessage(kitsune,a)
                    else:
                        ki.taagsaya(kitsune,"Type: Search Definition",mid,str(text)+" not found")
                if len(kitsunesplit) == 2:
                    try:
                        pl = int(kitsunesplit[1])
                        music = data["results"][pl - 1]
                        a = " 「 Music 」\nType: Search Music"
                        try:
                            a += "\n  Single : " + str(music["collectionName"])
                        except:
                            a += "\n  Single : Nothing"
                        a += "\n  Artist : " + str(music["artistName"])
                        a += "\n  Album  : " + str(music["trackName"])+'\n'
                        ki.jangantag(kitsune,a,'Taken: %.10f' % (elapsed_time/2),mid,"Status: Success")
                        ki.jangantag(kitsune,' 「 Music 」\nStatus: Waiting...','Type: Downloading Music',mid,"Request: Get Music "+text)
                        path = music['previewUrl']
                        ki.sendAudioWithURL(kitsune,path)
                    except Exception as e:
                        return ki.taagsaya(kitsune,"Type: Search Music",mid,str(e))
            if kitxt.lower().startswith(wait["setkey"]+'instagram ') or kitxt.lower().startswith(wait["setkey"]+' instagram '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                kitsunesplit = text.split("|")
                kitsunetext = str(kitsunesplit[0])
                if len(kitsunesplit) == 1:ki.igsearch(kitsune,kitsunetext,saya)
                if len(kitsunesplit) == 2:ki.igsearchdata(kitsune,kitsunetext,saya,int(kitsunesplit[1]))
            if kitxt.lower().startswith(wait["setkey"]+'steal cover ') or kitxt.lower().startswith(wait["setkey"]+' steal cover '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    ki.stealcover(kitsune,key1)
            if kitxt.lower().startswith(wait["setkey"]+'get timeline') or kitxt.lower().startswith(wait["setkey"]+' get timeline'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    separate = kitxt.split(" ")
                    text = kitxt.replace(separate[0] + " ","")
                    cond = text.split("|")
                    if len(cond) == 1:ki.gettimeline(kitsune,key1)
                    if len(cond) == 2:
                        try:
                            num = int(cond[1])
                            music = ki.getHomeProfile(key1)['result']['feeds'][num - 1]
                            try:h = str(ki.getHomeProfile(key1)['result']['homeInfo']['userInfo']['nickname'])
                            except:h = "Tidak Ketahui"
                            a = "Penulis: "+h
                            try:
                                g= str(music['post']['contents']['text'])
                            except:
                                g="None"
                            a +="\nStatus: "+g
                            a +="\nTotal Like: "+str(music['post']['postInfo']['likeCount'])
                            a +="\nTotal Comment: "+str(music['post']['postInfo']['commentCount'])
                            gtime = music['post']['postInfo']['createdTime']
                            a +="\nCreated at: "+str(timeago.format(datetime.now(),gtime/1000))
                            a +="\nLink: line://home/post?userMid="+str(ki.getHomeProfile(key1)['result']['homeInfo']['userInfo']['writerMid'])+"&postId="+str(music['post']['postInfo']['postId'])
                            try:
                                for c in music['post']['contents']['media']:
                                    params = {'userMid': mid, 'oid': c['objectId']}
                                    path = ki.server.urlEncode(ki.server.LINE_OBS_DOMAIN, '/myhome/h/download.nhn', params)
                                ki.sendMessage(kitsune," 「 Timeline Results No "+ str(num)+" 」\n\n"+a)
                                if c['type'] == 'PHOTO':
                                    ki.sendImageWithURL(kitsune,path)
                                else:
                                    pass
                                if c['type'] == 'VIDEO':
                                    ki.sendVideoWithURL(kitsune,path)
                                else:
                                    pass
                            except:
                                ki.sendMessage(kitsune," 「 Timeline Results No "+ str(num)+" 」\n"+a)
                        except Exception as e:
                            ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
                else:    
                    if msg.toType == 2:
                        pass
                    else:
                        separate = kitxt.split(" ")
                        text = kitxt.replace(separate[0] + " ","")
                        cond = text.split("~")
                        if len(cond) == 2:
                            try:
                                num = int(cond[1])
                                music = ki.getHomeProfile(kitsune)['result']['feeds'][num - 1]
                                try:h = str(ki.getHomeProfile(kitsune)['result']['homeInfo']['userInfo']['nickname'])
                                except:h = "Tidak Ketahui"
                                a = "Penulis: "+h
                                try:
                                    g= str(music['post']['contents']['text'])
                                except:
                                    g="None"
                                a +="\nStatus: "+g
                                a +="\nTotal Like: "+str(music['post']['postInfo']['likeCount'])
                                a +="\nTotal Comment: "+str(music['post']['postInfo']['commentCount'])
                                gtime = music['post']['postInfo']['createdTime']
                                a +="\nCreated at: "+str(timeago.format(datetime.now(),gtime/1000))
                                a +="\nLink: line://home/post?userMid="+str(ki.getHomeProfile(kitsune)['result']['homeInfo']['userInfo']['writerMid'])+"&postId="+str(music['post']['postInfo']['postId'])
                                try:
                                    for c in music['post']['contents']['media']:
                                        params = {'userMid': mid, 'oid': c['objectId']}
                                        path = ki.server.urlEncode(ki.server.LINE_OBS_DOMAIN, '/myhome/h/download.nhn', params)
                                    ki.sendMessage(kitsune," 「 Timeline Results No "+ str(num)+" 」\n"+a)
                                    if c['type'] == 'PHOTO':
                                        ki.sendImageWithURL(kitsune,path)
                                    else:
                                        pass
                                    if c['type'] == 'VIDEO':
                                        ki.sendVideoWithURL(kitsune,path)
                                    else:
                                        pass
                                except:
                                    ki.sendMessage(kitsune," 「 Timeline Results No "+ str(num)+" 」\n\n"+a)
                            except Exception as e:
                                ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
            if kitxt.lower().startswith(wait["setkey"]+'addbl ') or kitxt.lower().startswith(wait["setkey"]+' addbl '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        addbl(kitsune,target)
            if kitxt.lower().startswith(wait["setkey"]+'addwl ') or kitxt.lower().startswith(wait["setkey"]+' addwl '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        addwl(kitsune,target)
            if kitxt.lower().startswith(wait["setkey"]+'delbl ') or kitxt.lower().startswith(wait["setkey"]+' delbl '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        delbl(kitsune,target)
                else:
                    separate = kitxt.split(" ")
                    text = kitxt.replace(separate[0] + " ","")
                    cond = text.split("~")
                    if len(cond) == 2:
                            num = int(cond[1])
                            if num <= len(wait["blacklist"]):
                                bl = wait["blacklist"][num-1]
                                delbl(kitsune,bl)
            if kitxt.lower().startswith(wait["setkey"]+'delwl ') or kitxt.lower().startswith(wait["setkey"]+' delwl '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        delwl(kitsune,target)
                else:
                    separate = kitxt.split(" ")
                    text = kitxt.replace(separate[0] + " ","")
                    cond = text.split("~")
                    if len(cond) == 2:
                        num = int(cond[1])
                        bl = wait["bots"][num-1]
                        delwl(kitsune,bl)
            if kitxt.lower().startswith(wait["setkey"]+'del groups'):
                    separate = kitxt.split(" ")
                    text = kitxt.replace(separate[0] + " ","")
                    cond = text.split(" ")
                    if len(cond) == 2:
                        num = int(cond[1])
                        gid = ki.getGroupIdsJoined()
                        ki.leaveGroup(gid[num - 1])
                        ki.sendMessage(kitsune,"Success leave "+ ki.getGroup(gid[num - 1]).name +" group")
            if kitxt.lower().startswith(wait["setkey"]+'ikkeh on ') or kitxt.lower().startswith(wait["setkey"]+' ikkeh on '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    ki.ikkehtarget(kitsune,key1)
            if kitxt.lower().startswith(wait["setkey"]+'getid ') or kitxt.lower().startswith(wait["setkey"]+' getid '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    getinformation(kitsune,key1)
                else:
                    separate = kitxt.split(" ")
                    text = kitxt.replace(separate[0] + " ","")
                    cond = text.split("~")
                    if len(cond) == 2:
                            num = int(cond[1])
                            gid = ki.getGroupIdsJoined()
                            group = ki.getGroup(gid[num-1])
                            try:
                                GS = group.creator.mid
                                gCreator = group.creator.kitsuneName
                                gtime = group.createdTime
                            except:
                                GS = group.kitsunemembers[0].mid
                                gCreator = group.kitsunemembers[0].kitsuneName
                                gtime = group.createdTime
                            if group.invitee is None:
                                sinvitee = "0"
                            else:
                                sinvitee = str(len(group.invitee))
                            if group.kitsuneTicket == True:
                                u = "Disable"
                            else:
                                u = "line://ti/g/" + ki.reissueGroupTicket(gid[num-1])
                            cmem = ki.getContact(GS)
                            zx = ""
                            zxc = " 「 ID 」\nGroup Name:\n" + str(group.name) + "\n\nGroup ID:\n" + gid[num-1] + "\n\nAnggota:" + str(len(group.kitsunemembers)) + "\nInvitation:" + sinvitee + "\nTicket:" + u + "\n\nCreated at:\n" + str(timeago.format(datetime.now(),gtime/1000)) + "\nby ・ "
                            zx2 = []
                            pesan2 = "@a"" "
                            xlen = str(len(zxc))
                            xlen2 = str(len(zxc)+len(pesan2)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem.mid}
                            zx2.append(zx)
                            zxc += pesan2
                            msg.contentType = 0
                            msg.text = zxc
                            lol = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
                            msg.contentMetadata = lol
                            try:
                                ki.sendMessages(msg)
                            except Exception as e:
                                ki.sendMessage(kitsune, " 「 ID 」\nGroup Name:\n" + str(group.name) + "\n\nGroup ID:\n" + gid[num-1] + "\n\nAnggota:" + str(len(group.kitsunemembers)) + "\nInvitation:" + sinvitee + "\nTicket:" + u + "\n\nCreated at:\n" + str(timeago.format(datetime.now(),gtime/1000)) + "\nby ・ "+gCreator)
                            ki.sendContact(kitsune,GS)
            if kitxt.lower() == wait["setkey"]+'lurk result' or kitxt.lower() == wait["setkey"]+' lurk result':
                if msg.to in wait2['readPoint']:
                    chiya = []
                    for rom in wait2["ROM"][kitsune].items():
                        chiya.append(rom[1])
                    sidertag(kitsune,'',chiya)
                    wait2['setTime'][kitsune]  = {}
                    wait2['ROM'][kitsune] = {}
                    backupjson_2()
                else:
                    ki.sendMessage(kitsune, " 「 Lurk 」\nLurk point not on♪")
            if kitxt.lower() == wait["setkey"]+'lurk on' or kitxt.lower() == wait["setkey"]+' lurk on':
                if msg.to in wait2['readPoint']:
                    ki.sendMessage(kitsune, " 「 Lurk 」\nLurk already set♪")
                else:
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['setTime'][kitsune]  = {}
                    wait2['ROM'][kitsune] = {}
                    backupjson_2()
                    ki.sendMessage(kitsune, " 「 Lurk 」\nLurk point set♪")
            if kitxt.lower() == wait["setkey"]+'lurk off' or kitxt.lower() == wait["setkey"]+' lurk off':
                if msg.to not in wait2['readPoint']:
                    ki.sendMessage(kitsune, " 「 Lurk 」\nLurk already off♪")
                else:
                    try:
                       del wait2['readPoint'][msg.to]
                       del wait2['setTime'][msg.to]
                    except:
                       pass
                    ki.sendMessage(kitsune, " 「 Lurk 」\nLurk point off♪")
            if kitxt.lower() == wait["setkey"]+' autojoin' or kitxt.lower() == wait["setkey"]+'autojoin':
                if wait['autoJoin'] == True:
                        msgs=" 「 Auto Join 」\nState: ENABLED♪\nState: "+str(wait["Members"])+" Available join\n"
                else:
                        msgs=" 「 Auto Join 」\nState: DISABLED♪\nState: "+str(wait["Members"])+" Available join\n"
                ki.sendMessage(kitsune, msgs+"\n  |Command|\n- Autojoin group\n   Usage:"+wait["setkey"]+" autojoin [on|off]\n- Available min join\n   Usage:"+wait["setkey"]+" autojoin set <num>")
            if kitxt.lower() == wait["setkey"]+' spam' or kitxt.lower() == wait["setkey"]+'spam':
                ki.sendMessage(kitsune, " 「 Spam 」\n\n  |Command|\n- Spam Message\n   Usage:"+wait["setkey"]+" spam 1 <1-50> [@|~] <text>\n- Spam Gift\n   Usage:"+wait["setkey"]+" spam 2 <1-50> [@|~]\n- Spam Contact\n   Usage:"+wait["setkey"]+" spam 3 <1-50> [@|~]\n- Spam Group Invite\n   Usage:"+wait["setkey"]+" spam 4 <1-50> <name> [@|~]\n- Spam Tag\n   Usage:"+wait["setkey"]+" spam 5 <1-50> [@|~]")
            if kitxt.lower() == wait["setkey"]+' autojoin on' or kitxt.lower() == wait["setkey"]+'autojoin on':
                if wait['autoJoin'] == True:
                    msgs=" 「 Auto Join 」\nAuto Join already set to ENABLED♪"
                else:
                    msgs=" 「 Auto Join 」\nAuto Join has been set to ENABLED♪"
                    wait['autoJoin']=True
                    backupjson_1()
                ki.sendMessage(kitsune, msgs)
            if kitxt.lower() == wait["setkey"]+' autojoin off' or kitxt.lower() == wait["setkey"]+'autojoin off':
                if wait['autoJoin'] == False:
                    msgs=" 「 Auto Join 」\nAuto Auto Join already set to DISABLED♪"
                else:
                    msgs=" 「 Auto Join 」\nAuto Join has been set to DISABLED♪"
                    wait['autoJoin']=False
                    backupjson_1()
                ki.sendMessage(kitsune, msgs)
            if kitxt.lower() == wait["setkey"]+'bio' or kitxt.lower() == wait["setkey"]+' bio':
                profile = ki.getProfile()
                ki.sendMessage(kitsune, profile.kitsuneBio)
            if kitxt.lower() == wait["setkey"]+'mid' or kitxt.lower() == wait["setkey"]+' mid':
                ki.sendMessage(kitsune,saya)
            if kitxt.lower() == wait["setkey"]+'gcreator' or kitxt.lower() == wait["setkey"]+' gcreator':
                try:
                    group = ki.getGroup(kitsune)
                    GS = group.creator.mid
                    ki.sendMessage(kitsune, text=None, contentMetadata={'mid': GS}, contentType=13)
                except:
                    GS = group.kitsunemembers[0].mid
                    ki.sendMessage(kitsune, text=None, contentMetadata={'mid': GS}, contentType=13)
                    ki.sendMessage(kitsune,"Karena pencipta tidak ada saat ini, saya menunjukkan pengguna yang pertama kali masuk ke akun yang ada")
            elif msg.text.lower() == wait["setkey"]+'list pending' or msg.text.lower() == wait["setkey"]+' list pending':
                kitsunefriends = ki.getGroupIdsInvited()
                num=0
                msgs="「 Pending 」\nPending List:"
                for ids in kitsunefriends:
                    ki.getGroup(ids)
                    msgs+="\n%i. %s #%s" % (num, aditya.name, len(aditya.kitsunemembers))
                    num=(num+1)
                msgs+="\n\nTotal %i Pending" % len(kitsunefriends)
                ki.sendMessage(kitsune, msgs)
            if kitxt.lower().startswith(wait["setkey"]+'blacklist ') or kitxt.lower().startswith(wait["setkey"]+' blacklist'):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                cond = text.split("~")
                if len(cond) == 2:
                        num = int(cond[1])
                        getinformation(kitsune,wait["blacklist"][num-1])
            if  kitxt.lower().startswith(wait["setkey"]+' whitelist ') or kitxt.lower().startswith(wait["setkey"]+'whitelist '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                cond = text.split("~")
                if len(cond) == 2:
                    if kitxt.lower().startswith(wait["setkey"]+' whitelist ') or kitxt.lower().startswith(wait["setkey"]+'whitelist '):
                        num = int(cond[1])
                        getinformation(kitsune,wait["bots"][num-1])
            if kitxt.lower() == wait["setkey"]+' gcancel' or kitxt.lower() == wait["setkey"]+'gcancel':
                gid = ki.getGroupIdsInvited()
                for i in gid:
                    ki.rejectGroupInvitation(i)
                ki.sendMessage(kitsune, text="Reject %i Invitation" % len(gid), contentMetadata=None, contentType=0)
            elif msg.text.lower() == wait["setkey"]+' remove all chat' or msg.text.lower() == wait["setkey"]+'remove all chat':
                ki.removeAllMessages(op.param2)
                ki.sendMessage(kitsune,"Removed all chat Sukses")
            if kitxt.lower().startswith(wait["setkey"]+'mimic'):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                cond = text.split("~")
                if len(cond) == 2:
                        num = int(cond[1])
                        if num <= len(wait["target"]):
                            getinformation(kitsune,wait["target"][num-1])
            if kitxt.lower() == wait["setkey"]+'clear mimic' or kitxt.lower() == wait["setkey"]+' clear mimic':
                kitsunefriend = ki.getContacts(wait["target"])
                for ids in kitsunefriend:
                    wait["target"] = []
                    backupjson_1()
                ki.sendMessage(kitsune," 「 Mimic 」\nDelete %i Mimic list" % len(kitsunefriend))
            if kitxt.lower() == wait["setkey"]+'clearbl' or kitxt.lower() == wait["setkey"]+' clearbl':
                kitsunefriend = ki.getContacts(wait["blacklist"])
                for ids in kitsunefriend:
                    wait["blacklist"] = []
                    backupjson_1()
                ki.sendMessage(kitsune," 「 Blacklist 」\nDelete %i Black list" % len(kitsunefriend))
            if kitxt.lower() == wait["setkey"]+'clearwl' or kitxt.lower() == wait["setkey"]+' clearwl':
                kitsunefriend = ki.getContacts(wait["bots"])
                for ids in kitsunefriend:
                    wait["bots"] = []
                    backupjson_1()
                ki.sendMessage(kitsune," 「 Blacklist 」\nDelete %i White list" % len(kitsunefriend))
            if kitxt.lower().startswith(wait["setkey"]+'steal pp') or kitxt.lower().startswith(wait["setkey"]+' steal pp'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    ki.stealpp(kitsune,key1)
                else:
                    separate = kitxt.split(" ")
                    text = kitxt.replace(separate[0]+" ","")
                    cond = text.split(" ")
                    if len(cond) == 2:
                        num = int(cond[1])
                        gid = ki.getGroupIdsJoined()
                        group = ki.getGroup(gid[num-1])
                        ki.sendImageWithURL(kitsune,"http://dl.profile.line-cdn.net/" + group.kitsunephotoStatus)
            if kitxt.lower() == wait["setkey"]+'runtime' or kitxt.lower() == wait["setkey"]+' runtime':
                start = time.time() - mulas
                ki.sendMessage(kitsune," 「 Timing 」\n" + waktu(start))
            if kitxt.lower() == 'copy me':
                ki1.clone(saya)
                ki2.clone(saya)
                ki3.clone(saya)
                ki4.clone(saya)
                ki5.clone(saya)
                ki6.clone(saya)
                ki7.clone(saya)
                ki8.clone(saya)
                ki9.clone(saya)
                ki10.clone(saya)
                ki11.clone(saya)
                ki12.clone(saya)
                ki13.clone(saya)
                ki14.clone(saya)
                ki15.clone(saya)
                ki16.clone(saya)
                ki17.clone(saya)
                ki18.clone(saya)
                ki19.clone(saya)
                ki20.clone(saya)
                ki21.clone(saya)
            if kitxt.lower() == 'renew':
                ki.sendMessage(kitsune," 「 Restarting 」\nType: Restart Program\nRestarting...")
                restart_program()
            if kitxt.lower().startswith(wait["setkey"]+'pesan set:') or kitxt.lower().startswith(wait["setkey"]+' pesan set:'):
                if kitxt.lower().startswith(wait["setkey"]+' pesan set:'):
                    foo = wait["setkey"]+' pesan set:'
                    key = len(foo)
                    key1 = kitxt[key:]
                    wait["message"] = key1
                    ki.sendMessage(kitsune," 「 Welcome Message 」\nWelcome Message has been set to:\n"+wait["message"])
                else:
                    foo = wait["setkey"]+'pesan set:'
                    key = len(foo)
                    key1 = kitxt[key:]
                    wait["message"] = key1
                    ki.sendMessage(kitsune," 「 Welcome Message 」\nWelcome Message has been set to:\n"+wait["message"])
            if kitxt.lower().startswith(wait["setkey"]+'welcomemessage pict set ') or kitxt.lower().startswith(wait["setkey"]+' welcomemessage pict set '):
                if kitxt.lower().startswith(' Welcomemessage pict set:'):
                    foo = wait["setkey"]+' welcomemessage pict set '
                    key = len(foo)
                    key1 = kitxt[key:]
                    mimic["pap"] = key1
                    ki.sendMessage(kitsune,"Welcome Message Picture has been set to")
                    urllib.urlretrieve(mimic["pap"], "welcome.png")
                    ki.kitsunePMG(kitsune,"welcome.png")
                else:
                    foo = wait["setkey"]+'welcomemessage pict set '
                    key = len(foo)
                    key1 = kitxt[key:]
                    mimic["pap"] = key1
                    ki.sendMessage(kitsune,"Welcome Message Picture has been set to")
                    urllib.urlretrieve(mimic["pap"], "welcome.png")
                    ki.kitsunePMG(kitsune,"welcome.png")
            if kitxt.lower().startswith(wait["setkey"]+'spam ') or kitxt.lower().startswith(wait["setkey"]+' spam '):
                if kitxt.lower().startswith(wait["setkey"]+' spam '):
                    txt = kitxt.split(" ")
                    jmlh = int(txt[2])
                    foo = wait["setkey"]+' spam '
                    key = len(foo)
                    key1 = kitxt[key:]
                    teks = key1.replace("" + str(txt[1])+" "+str(jmlh)+ " ","")
                    if txt[1] == "1":
                        if jmlh <= 50:
                            for x in range(jmlh):
                                ki.sendMessage(kitsune, teks)
                        ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of messages♪' % int(jmlh))
                else:
                    txt = kitxt.split(" ")
                    jmlh = int(txt[2])
                    foo = wait["setkey"]+'spam '
                    key = len(foo)
                    key1 = kitxt[key:]
                    teks = key1.replace("" + str(txt[1])+" "+str(jmlh)+ " ","")
                    if txt[1] == "1":
                        if jmlh <= 50:
                            for x in range(jmlh):
                                ki.sendMessage(kitsune, teks)
                        ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of messages♪' % int(jmlh))
            if kitxt.lower().startswith(wait["setkey"]+'spam 5 ') or kitxt.lower().startswith(wait["setkey"]+' spam 5 '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    jmlh = int(txt[2])
                    if jmlh <= 500:
                        for x in range(jmlh):
                            try:
                               ki.autorespontag(kitsune,key1)
                            except Exception as e:
                               ki.sendMessage(kitsune,str(e))
                    ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of mention♪' % int(jmlh))
                else:
                    jmlh = int(txt[2])
                    if jmlh <= 500:
                        for x in range(jmlh):
                            if msg.toType == 2:
                                pass
                            else:
                                ki.autorespontag(kitsune,kitsune)
                    ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of mention♪' % int(jmlh))
            if kitxt.lower().startswith(wait["setkey"]+'spam 4 ') or kitxt.lower().startswith(wait["setkey"]+' spam 4 '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    mi = ki.getContact(key1)
                    txt = kitxt.split(" ")
                    jmlh = int(txt[2])
                    try:
                        jmlh = int(txt[2])
                    except:
                        ki.sendMessage(msg.to, "Group name can't use spaces")
                    ki1.findAndAddContactsByMid(key1)
                    ki2.findAndAddContactsByMid(key1)
                    ki3.findAndAddContactsByMid(key1)
                    ki4.findAndAddContactsByMid(key1)
                    ki5.findAndAddContactsByMid(key1)
                    ki6.findAndAddContactsByMid(key1)
                    ki7.findAndAddContactsByMid(key1)
                    ki8.findAndAddContactsByMid(key1)
                    ki9.findAndAddContactsByMid(key1)
                    ki10.findAndAddContactsByMid(key1)
                    ki11.findAndAddContactsByMid(key1)
                    ki12.findAndAddContactsByMid(key1)
                    ki13.findAndAddContactsByMid(key1)
                    ki14.findAndAddContactsByMid(key1)
                    ki15.findAndAddContactsByMid(key1)
                    ki16.findAndAddContactsByMid(key1)
                    ki17.findAndAddContactsByMid(key1)
                    ki18.findAndAddContactsByMid(key1)
                    ki19.findAndAddContactsByMid(key1)
                    ki20.findAndAddContactsByMid(key1)
                    ki21.findAndAddContactsByMid(key1)
                    if jmlh <= 500:
                        for a in range(jmlh):
                            ki1.createGroup(wait["spam"], [key1])
                            ki2.createGroup(wait["spam"], [key1])
                            ki3.createGroup(wait["spam"], [key1])
                            ki4.createGroup(wait["spam"], [key1])
                            ki5.createGroup(wait["spam"], [key1])
                            ki6.createGroup(wait["spam"], [key1])
                            ki7.createGroup(wait["spam"], [key1])
                            ki8.createGroup(wait["spam"], [key1])
                            ki9.createGroup(wait["spam"], [key1])
                            ki10.createGroup(wait["spam"], [key1])
                            ki11.createGroup(wait["spam"], [key1])
                            ki12.createGroup(wait["spam"], [key1])
                            ki13.createGroup(wait["spam"], [key1])
                            ki14.createGroup(wait["spam"], [key1])
                            ki15.createGroup(wait["spam"], [key1])
                            ki16.createGroup(wait["spam"], [key1])
                            ki17.createGroup(wait["spam"], [key1])
                            ki18.createGroup(wait["spam"], [key1])
                            ki19.createGroup(wait["spam"], [key1])
                            ki20.createGroup(wait["spam"], [key1])
                            ki21.createGroup(wait["spam"], [key1])
                    ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of groups♪' % int(jmlh*21))
            if kitxt.lower().startswith(wait["setkey"]+'spam 2 ') or kitxt.lower().startswith(wait["setkey"]+' spam 2 '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    txt = kitxt.split(" ")
                    jmlh = int(txt[2])
                    if jmlh <= 500:
                        for x in range(jmlh):
                            ki.giftmessage(key1)
                    ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of gift♪' % int(jmlh))
                else:
                    txt = kitxt.split(" ")
                    jmlh = int(txt[2])
                    if jmlh <= 50:
                        for x in range(jmlh):
                            ki.giftmessage(kitsune)
                    ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of gift♪' % int(jmlh))
            if kitxt.lower().startswith(wait["setkey"]+'spam 3 ') or kitxt.lower().startswith(wait["setkey"]+' spam 3 '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    mi = ki.getContact(key1)
                    txt = kitxt.split(" ")
                    jmlh = int(txt[2])
                    if jmlh <= 500:
                        for x in range(jmlh):
                            ki.sendMessage(kitsune, text=None, contentMetadata={'mid': key1}, contentType=13)
                    ki.sendMessage(kitsune, '「 Spam 」\nTarget has been spammed with %i amount of contact♪' % int(jmlh))
            if kitxt.lower() == wait["setkey"]+'welcomemessage pict' or kitxt.lower() == wait["setkey"]+' welcomemessage pict':
                ki.kitsunePMG(kitsune,"welcome.png")
            if kitxt.lower() == wait["setkey"]+'pesan cek' or kitxt.lower() == wait["setkey"]+' pesan cek':
                    ki.sendMessage(kitsune, wait["message"])
            if kitxt.lower().startswith(wait["setkey"]+'nk ') or kitxt.lower().startswith(wait["setkey"]+' nk '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                            try:
                                gs = ki.getGroup(kitsune)
                                gs.kitsuneTicket = False
                                random.choice(P2).updateGroup(gs)
                                invsend = 0
                                Ticket = random.choice(P2).reissueGroupTicket(kitsune)
                                ki19.acceptGroupInvitationByTicket(kitsune,Ticket)
                                ki19.kickoutFromGroup(kitsune,[target])
                                gs.kitsuneTicket = True
                                ki19.updateGroup(gs)
                                ki100.sendText(gs)
                            except:
                                ki19.leaveGroup(kitsune)
                else:
                    ki.sendMessage(kitsune," 「 Kick Mode Siri 」\nYou have to mention a user♪")
#-----------------------------------------------------------
            if kitxt.lower().startswith(wait["setkey"]+'kick1 ') or kitxt.lower().startswith(wait["setkey"]+' kick1 ') or kitxt.lower().startswith(wait["setkey"]+'kick1') or kitxt.lower().startswith(wait["setkey"]+' kick1'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ki1.kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            ki1.sendMessage(kitsune,str(e))
                else:
                    ki1.sendMessage(kitsune," 「 Kick 」\nYou need to mention a user♪")
            if kitxt.lower().startswith(wait["setkey"]+'kick2 ') or kitxt.lower().startswith(wait["setkey"]+' kick2 ') or kitxt.lower().startswith(wait["setkey"]+'kick2') or kitxt.lower().startswith(wait["setkey"]+' kick2'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ki2.kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            ki2.sendMessage(kitsune,str(e))
                else:
                    ki2.sendMessage(kitsune," 「 Kick 」\nYou need to mention a user♪")
            if kitxt.lower().startswith(wait["setkey"]+'kick3 ') or kitxt.lower().startswith(wait["setkey"]+' kick3 ') or kitxt.lower().startswith(wait["setkey"]+'kick3') or kitxt.lower().startswith(wait["setkey"]+' kick3'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ki3.kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            ki3.sendMessage(kitsune,str(e))
                else:
                    ki3.sendMessage(kitsune," 「 Kick 」\nYou need to mention a user♪")
            if kitxt.lower().startswith(wait["setkey"]+'kick4 ') or kitxt.lower().startswith(wait["setkey"]+' kick4 ') or kitxt.lower().startswith(wait["setkey"]+'kick4') or kitxt.lower().startswith(wait["setkey"]+' kick4'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ki4.kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            ki4.sendMessage(kitsune,str(e))
                else:
                    ki4.sendMessage(kitsune," 「 Kick 」\nYou need to mention a user♪")
            if kitxt.lower().startswith(wait["setkey"]+'kick5 ') or kitxt.lower().startswith(wait["setkey"]+' kick5 ') or kitxt.lower().startswith(wait["setkey"]+'kick5') or kitxt.lower().startswith(wait["setkey"]+' kick5'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ki5.kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            ki5.sendMessage(kitsune,str(e))
                else:
                    ki5.sendMessage(kitsune," 「 Kick 」\nYou need to mention a user♪")
            if kitxt.lower().startswith(wait["setkey"]+'kick6 ') or kitxt.lower().startswith(wait["setkey"]+' kick6 ') or kitxt.lower().startswith(wait["setkey"]+'kick6') or kitxt.lower().startswith(wait["setkey"]+' kick6'):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ki6.kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            ki6.sendMessage(kitsune,str(e))
                else:
                    ki6.sendMessage(kitsune," 「 Kick 」\nYou need to mention a user♪")
            if kitxt.lower().startswith(wait["setkey"]+'makan ') or kitxt.lower().startswith(wait["setkey"]+' makan '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            random.choice(P1).kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            random.choice(P1).sendMessage(kitsune,str(e))
                else:
                    random.choice(P1).sendMessage(kitsune," 「 makan 」\nYou need to mention a user♪")
            if kitxt.lower().startswith(wait["setkey"]+'kick ') or kitxt.lower().startswith(wait["setkey"]+' kick '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            ki.kickoutFromGroup(kitsune,[target])
                        except Exception as e:
                            ki.sendMessage(kitsune,str(e))
                else:
                    ki.sendMessage(kitsune," 「 Kick 」\nYou need to mention a user♪")
            if kitxt.lower() == 'responsename':
                ki1.responsename(kitsune)
                ki2.responsename(kitsune)
                ki3.responsename(kitsune)
                ki4.responsename(kitsune)
                ki5.responsename(kitsune)
                ki6.responsename(kitsune)
                ki7.responsename(kitsune)
                ki8.responsename(kitsune)
                ki9.responsename(kitsune)
                ki10.responsename(kitsune)
                ki11.responsename(kitsune)
                ki12.responsename(kitsune)
                ki13.responsename(kitsune)
                ki14.responsename(kitsune)
                ki15.responsename(kitsune)
                ki16.responsename(kitsune)
                ki17.responsename(kitsune)
                ki18.responsename(kitsune)
                ki20.responsename(kitsune)
                ki21.responsename(kitsune)
            if kitxt.lower().startswith(wait["setkey"]+'bot ') or kitxt.lower().startswith(wait["setkey"]+' bot '):
                separate = kitxt.split(" ")
                bctxt = kitxt.replace(separate[0]+" ","")
                ki1.sendMessage(kitsune,(bctxt))
                ki2.sendMessage(kitsune,(bctxt))
                ki3.sendMessage(kitsune,(bctxt))
                ki4.sendMessage(kitsune,(bctxt))
                ki5.sendMessage(kitsune,(bctxt))
                ki6.sendMessage(kitsune,(bctxt))
                ki7.sendMessage(kitsune,(bctxt))
                ki8.sendMessage(kitsune,(bctxt))
                ki9.sendMessage(kitsune,(bctxt))
                ki10.sendMessage(kitsune,(bctxt))
                ki11.sendMessage(kitsune,(bctxt))
                ki12.sendMessage(kitsune,(bctxt))
                ki13.sendMessage(kitsune,(bctxt))
                ki14.sendMessage(kitsune,(bctxt))
                ki15.sendMessage(kitsune,(bctxt))
                ki16.sendMessage(kitsune,(bctxt))
                ki17.sendMessage(kitsune,(bctxt))
                ki18.sendMessage(kitsune,(bctxt))
                ki20.sendMessage(kitsune,(bctxt))
                ki21.sendMessage(kitsune,(bctxt))
            if kitxt.lower().startswith(wait["setkey"]+'hi'):
                separate = kitxt.split(",")
                text = kitxt.replace(separate[0]+",","")
                gs = ki.getGroup(kitsune)
                wait["rbio"] = []
                for s in gs.kitsunemembers:
                    if text in s.kitsuneName:
                       wait["rbio"].append(s.mid)
                nama = wait["rbio"]
                nm1, nm2, nm3, nm4,  nm5, jml = [], [], [], [],  [], len(nama)
                if jml <= 150:
                    ki.mention1(kitsune,"",nama)
                if jml > 150 and jml < 500:
                    for i in range(0, 150):
                        nm1 += [nama[i]]
                    ki.mention1(kitsune,"",nm1)
                    for j in range(149, len(nama)-1):
                           nm2 += [nama[j]]
                    ki.mention2(kitsune,"",nm2)
            if kitxt.lower() == wait["setkey"]+' call invite' or kitxt.lower() == wait["setkey"]+'call invite':
                ki.acquireCallRoute(kitsune)
            if kitxt.lower() == wait["setkey"]+' mentionall' or kitxt.lower() == wait["setkey"]+'mentionall':
                try:
                    group = ki.getGroup(kitsune)
                    nama = [contact.mid for contact in group.kitsunemembers]
                    nama.remove(mid)
                except:
                    group = ki.getRoom(kitsune)
                    nama = [contact.mid for contact in group.contacts]
                nm1, nm2, nm3, nm4,  nm5, jml = [], [], [], [],  [], len(nama)
                if jml <= 159:
                    ki.mention1(kitsune,"",nama)
                if jml > 150 and jml < 500:
                    for i in range(0, 150):
                        nm1 += [nama[i]]
                    ki.mention12(kitsune,"",nm1)
                    for j in range(150,300):
                           nm2 += [nama[j]]
                    ki.mention2(kitsune,"",nm2)
                    for k in range(298, len(nama)-2):
                           nm3 += [nama[k]]
                    ki.mention3(kitsune,"",nm3)
            if kitxt.lower() == wait["setkey"]+' /battle' or kitxt.lower() == wait["setkey"]+'/battle':
                try:
                    group = ki.getGroup(kitsune)
                    nama = [contact.mid for contact in group.kitsunemembers]
                    nama.remove(mid)
                except:
                    group = ki.getRoom(kitsune)
                    nama = [contact.mid for contact in group.contacts]
                nm1, nm2, nm3, nm4,  nm5, jml = [], [], [], [],  [], len(nama)
                if jml <= 160:
                    ki.mention1(kitsune,"",nama)
                if jml > 160 and jml < 500:
                    for i in range(0, 150):
                        nm1 += [nama[i]]
                    ki.mention12(kitsune,"",nm1)
                    for j in range(149,len(nama)-1):
                           nm2 += [nama[j]]
                    ki.mention2(kitsune,"",nm2)
                    for k in range(298, len(nama)-2):
                           nm3 += [nama[k]]
                    ki.mention3(kitsune,"",nm3)
            if kitxt.lower() == wait["setkey"]+' mention' or kitxt.lower() == wait["setkey"]+'mention':
                if msg.to in wait["mentionChat"]:
                        msgs=" 「 Mention 」\nAnti mention state: ENABLED♪\n"
                else:
                        msgs=" 「 Mention 」\nAnti mention state: DISABLED♪\n"
                ki.sendMessage(kitsune, msgs+"\n  |Command|\n- Anti mention\n   Usage:"+wait["setkey"]+" mention [on|off]\n- Mention by name\n   Usage:"+wait["setkey"]+" mention <a~z>\n- Tag all members\n   Usage:"+wait["setkey"]+" mentionall")
            if kitxt.lower().startswith(wait["setkey"]+'addml '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        addmimic(kitsune,target)
            if kitxt.lower().startswith(wait["setkey"]+'delml '):
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        delmimic(kitsune,target)
                else:
                    separate = kitxt.split(" ")
                    text = kitxt.replace(separate[0] + " ","")
                    cond = text.split("~")
                    if len(cond) == 2:
                            num = int(cond[1])
                            delmimic(kitsune,wait["target"][num-1])
            if kitxt.lower().startswith(wait["setkey"]+'invite ') or kitxt.lower().startswith(wait["setkey"]+' invite '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                ki.invitingContact(kitsune,text)
            if kitxt.lower().startswith(wait["setkey"]+'add ') or kitxt.lower().startswith(wait["setkey"]+' add '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                ki.addsContact(kitsune,text)
            if kitxt.lower().startswith(wait["setkey"]+'contacts ') or kitxt.lower().startswith(wait["setkey"]+' contacts '):
                separate = kitxt.split(" ")
                text = kitxt.replace(separate[0] + " ","")
                ki.stalkerin(kitsune,text)
            if 'leave ' in kitxt.lower():
                spl = kitxt.lower().replace('leave ','')
                if spl == 'on':
                    if wait['leaveRoom'] == True:
                        msgs=" 「 Auto Leave 」\nAuto Leave Multichat already ENABLED♪"
                    else:
                        msgs=" 「 Auto Leave 」Auto Leave Multichat set to ENABLED♪"
                        wait['leaveRoom']=True
                        backupjson_1()
                    ki.sendMessage(kitsune, msgs)
                if spl == 'off':
                    if wait['leaveRoom'] == False:
                        msgs=" 「 Auto Leave 」\nAuto Leave Multichat already DISABLED♪"
                    else:
                        msgs=" 「 Auto Leave 」\nAuto Leave Multichat set to DISABLED♪"
                        wait['leaveRoom']=False
                        backupjson_1()
                    ki.sendMessage(kitsune, msgs)
            if 'namelock ' in kitxt.lower():
                spl = kitxt.lower().replace('namelock ','')
                if spl == 'on':
                    if msg.to in wait['pname']:
                        msgs=" 「 Name Lock 」\nName Lock already ENABLED♪"
                    else:
                        msgs=" 「 Name Lock 」\nName Lock set to ENABLED♪"
                        wait['pname'].append(kitsune)
                        wait['pro_name'][msg.to] = ki.getGroup(msg.to).name
                        backupjson_1()
                    ki.sendMessage(kitsune, msgs)
                if spl == 'off':
                    if msg.to in wait['pname']:
                        msgs=" 「 Name Lock 」\nName Lock set to DISABLED♪"
                        wait['pname'].remove(kitsune)
                        backupjson_1()
                    else:
                        msgs=" 「 Name Lock 」\nName Lock already DISABLED♪"
                    ki.sendMessage(kitsune, msgs)
            if kitxt.lower() == wait["setkey"]+'cinta' or kitxt.lower() == wait["setkey"]+' cinta':
                        G = ki.getGroup(kitsune)
                        ginfo = ki.getGroup(kitsune)
                        G.kitsuneTicket = False
                        ki.updateGroup(G)
                        invsend = 0
                        Ticket = ki.reissueGroupTicket(kitsune)
                        ki1.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki2.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki3.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki4.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki5.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki6.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki7.acceptGroupInvitationByTicket(kitsune,Ticket)
                        G = ki.getGroup(kitsune)
                        ginfo = ki.getGroup(kitsune)
                        G.kitsuneTicket = True
                        ki1.updateGroup(G)
            if kitxt.lower() == wait["setkey"]+'all' or kitxt.lower() == wait["setkey"]+' all':
                        G = ki.getGroup(kitsune)
                        ginfo = ki.getGroup(kitsune)
                        G.kitsuneTicket = False
                        ki.updateGroup(G)
                        invsend = 0
                        Ticket = ki.reissueGroupTicket(kitsune)
                        ki1.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki2.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki3.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki4.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki5.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki6.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki7.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki8.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki9.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki10.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki11.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki12.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki13.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki14.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki15.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki16.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki17.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki18.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki20.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki21.acceptGroupInvitationByTicket(kitsune,Ticket)
            if kitxt.lower() == wait["setkey"]+'desah' or kitxt.lower() == wait["setkey"]+' desah':
                        G = ki.getGroup(kitsune)
                        ginfo = ki.getGroup(kitsune)
                        G.kitsuneTicket = False
                        ki.updateGroup(G)
                        invsend = 0
                        Ticket = ki.reissueGroupTicket(kitsune)
                        ki1.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki2.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki3.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki4.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki5.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki6.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki7.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki8.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki9.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki10.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki11.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki12.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki13.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki14.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki15.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki16.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki17.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki18.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki20.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki21.acceptGroupInvitationByTicket(kitsune,Ticket)
                        G = ki.getGroup(kitsune)
                        ginfo = ki.getGroup(kitsune)
                        G.kitsuneTicket = True
                        random.choice(P1).updateGroup(G)
            if kitxt.lower() == wait["setkey"]+'bye' or kitxt.lower() == wait["setkey"]+' bye':
                if msg.toType == 2:
                    ginfo = ki.getGroup(kitsune)
                    try:
                        ki.leaveGroup(kitsune)
                    except:
                        pass
            if kitxt.lower() == wait["setkey"]+'honey' or kitxt.lower() == wait["setkey"]+' honey':
                        G = ki.getGroup(kitsune)
                        ginfo = ki.getGroup(kitsune)
                        G.kitsuneTicket = False
                        ki.updateGroup(G)
                        invsend = 0
                        Ticket = ki.reissueGroupTicket(kitsune)
                        ki1.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki2.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki3.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki4.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki5.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki6.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki7.acceptGroupInvitationByTicket(kitsune,Ticket)
                        ki8.acceptGroupInvitationByTicket(kitsune,Ticket)
                        G = ki.getGroup(kitsune)
                        ginfo = ki.getGroup(kitsune)
                        G.kitsuneTicket = True
                        ki1.updateGroup(G)
                        G.kitsuneTicket(G)
            if kitxt.lower() == wait["setkey"]+'cau':
                if msg.toType == 2:
                    ginfo = ki.getGroup(kitsune)
                    try:
                        ki1.leaveGroup(kitsune)
                        ki2.leaveGroup(kitsune)
                        ki3.leaveGroup(kitsune)
                        ki4.leaveGroup(kitsune)
                        ki5.leaveGroup(kitsune)
                        ki6.leaveGroup(kitsune)
                        ki7.leaveGroup(kitsune)
                        ki8.leaveGroup(kitsune)
                        ki9.leaveGroup(kitsune)
                        ki10.leaveGroup(kitsune)
                        ki11.leaveGroup(kitsune)
                        ki12.leaveGroup(kitsune)
                        ki13.leaveGroup(kitsune)
                        ki14.leaveGroup(kitsune)
                        ki15.leaveGroup(kitsune)
                        ki16.leaveGroup(kitsune)
                        ki17.leaveGroup(kitsune)
                        ki18.leaveGroup(kitsune)
                        ki20.leaveGroup(kitsune)
                        ki21.leaveGroup(kitsune)
                    except:
                        pass
# Add function to LinePoll
poll.addOpInterruptWithDict({
    OpType.SEND_MESSAGE: SEND_MESSAGE
})

def RECEIVE_MESSAGE(op):
        msg = op.message
        kitxt = msg.text
        msg_id = msg.id
        kitsune = msg.to
        saya = msg._from
        if msg.contentType == 4:
            if msg.to in wait["autochat"]:
                try:
                    ki.sendMessage(saya,str(msg.contentMetadata['ALT_TEXT'][22:35]))
                    ki.sendMessage(saya,str(msg.contentMetadata['ALT_TEXT'][23:35]))
                    ki.sendMessage(saya,str(msg.contentMetadata['ALT_TEXT'][24:35]))
                except:
                    pass
        if wait["autoread"] == True:
            if msg.toType == 2:
                pass
            else:
                ki.sendChatChecked(saya,msg_id)
        if saya in wait["target"] and wait["status"] == True:
                text = msg.text
                if text is not None:
                    msg.text = msg.text
                    ki.sendMessages(msg)
                    try:
                        if msg.contentType == 1:
                            ki.sendImageWithURL(kitsune,'https://obs-sg.line-apps.com/talk/m/download.nhn?oid='+msg.id)
                        if msg.contentType == 2:
                            ki.sendVideoWithURL(kitsune,'https://obs-sg.line-apps.com/talk/m/download.nhn?oid='+msg.id)
                        if msg.contentType == 3:
                            ki.sendAudioWithURL(kitsune,'https://obs-sg.line-apps.com/talk/m/download.nhn?oid='+msg.id)
                    except Exception as e:
                        ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
                else:
                    msg.text = msg.text
                    ki.sendMessages(msg)
        if msg.contentType == 0:
            if 'MENTION' in msg.contentMetadata.keys()!= None:
                if msg.to in wait["mentionChat"]:
                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                    mentionees = mention['MENTIONEES']
                    for mention in mentionees:
                        if mention['M'] == mid:
                            cmem = ki.getContact(saya)
                            a = ki.getProfile()
                            zx = ""
                            zxc = " 「 Auto Respon 」\n・ "
                            zx2 = []
                            xname = str(cmem.kitsuneName)
                            pesan2 = "@a"" "
                            xlen = str(len(zxc))
                            xlen2 = str(len(zxc)+len(pesan2)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem.mid}
                            zx2.append(zx)
                            zxc += pesan2 + "Don't Tag "+a.kitsuneName+ " It's Annoying"
                            msg.contentType = 0
                            msg.text = zxc
                            lol = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
                            msg.contentMetadata = lol
                            if saya in wait["bots"]:
                                try:
                                    random.choice(P1).sendMessages(msg)
                                    break
                                except:
                                    ki.sendMessages(msg)
                                    break
                            else:
                                try:
                                    random.choice(P1).sendMessages(msg)
                                    random.choice(P1).kickoutFromGroup(kitsune,[saya])
                                    break
                                except:
                                    ki.sendMessages(msg)
                                    ki.kickoutFromGroup(kitsune,[saya])
                                    break
# Add function to LinePoll
poll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
})

def sidertag(to, text='', dataMid=[]):
    now = datetime.now()
    arr = []
    list_text=' 「 Lurk 」\nLurkers: %i Orang'%(len(dataMid))
    if '[list]' in text.lower():
        i=0
        for l in dataMid:
            list_text+='\n@[list-'+str(i)+']'
            i=i+1
        text=text.replace('[list]', list_text)
    elif '[list-' in text.lower():
        text=text
    else:
        i=0
        no=0
        for l in dataMid:
            z = ""
            chiya = []
        for rom in wait2["setTime"][to].items():
            chiya.append(rom[1])
        for b in chiya:
            a = str(timeago.format(now,b/1000))
            no+=1
            list_text+='\n   '+str(no)+'. @[list-'+str(i)+']\n     「 '+a+" 」"
            i=i+1
        list_text +="\n   Data Rewrite:\n      "+datetime.now().strftime('%H:%M:%S')
        text=text+list_text
    i=0
    for l in dataMid:
        mid=l
        name='@[list-'+str(i)+']'
        ln_text=text.replace('\n',' ')
        if ln_text.find(name):
            line_s=int( ln_text.index(name) )
            line_e=(int(line_s)+int( len(name) ))
        arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
        arr.append(arrData)
        i=i+1
    contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
    ki.sendMessage(to, text, contentMetadata)

def NOTIFIED_READ_MESSAGE(op):
    if op.param1 in wait2['readPoint']:
        wait2['ROM'][op.param1][op.param2] = op.param2
        wait2['setTime'][op.param1][op.param2] = op.createdTime
        backupjson_2()
    else:
        pass

poll.addOpInterruptWithDict({
    OpType.NOTIFIED_READ_MESSAGE: NOTIFIED_READ_MESSAGE
})

def NOTIFIED_UPDATE_GROUP(op):
        if op.param1 in wait["kitsuneurl"]:
            try:
                if op.param2 in wait["bots"]:
                    pass
                else:
                    G = ki.getGroup(op.param1)
                    G.kitsuneTicket = True
                    if op.param2 in wait["bots"] or op.param2 in wait["blacklist"]:
                        pass
                    else:
                        wait["blacklist"].append(op.param2)
                        backupjson_1()
                        G.kitsuneTicket = True
                        ki.updateGroup(G)
                        random.choice(P1).kickoutFromGroup(op.param1,[op.param2])
            except:
                if op.param2 in wait["bots"]:
                    pass
                else:
                    G = ki.getGroup(op.param1)
                    G.kitsuneTicket = True
                    if op.param2 in wait["bots"] or op.param2 in wait["blacklist"]:
                        pass
                    else:
                        wait["blacklist"].append(op.param2)
                        backupjson_1()
                        G.kitsuneTicket = True
                        ki.updateGroup(G)
                        random.choice(P2).kickoutFromGroup(op.param1,[op.param2])
        else:
            if op.param3 == "1":
                if op.param1 in wait['pname']:
                    group = ki.getGroup(op.param1)
                    try:
                        group.name = wait["pro_name"][op.param1]
                        random.choice(P1).updateGroup(group)
                        wait["blacklist"].append(op.param2)
                        backupjson_1()
                    except:
                        group.name = wait["pro_name"][op.param1]
                        ki.updateGroup(group)
                        wait["blacklist"].append(op.param2)
                        backupjson_1()

poll.addOpInterruptWithDict({
    OpType.NOTIFIED_UPDATE_GROUP: NOTIFIED_UPDATE_GROUP
})

def NOTIFIED_INVITE_INTO_ROOM(op):
    if wait["leaveRoom"] == True:
        ki.leaveRoom(op.param1)

poll.addOpInterruptWithDict({
    OpType.NOTIFIED_INVITE_INTO_ROOM: NOTIFIED_INVITE_INTO_ROOM
})

def NOTIFIED_LEAVE_ROOM(op):
    if wait["leaveRoom"] == True:
        ki.leaveRoom(op.param1)

poll.addOpInterruptWithDict({
    OpType.NOTIFIED_LEAVE_ROOM: NOTIFIED_LEAVE_ROOM
})

def NOTIFIED_ADD_CONTACT(op):
    zx = ""
    zxc = " 「 Autoadd 」\n "
    zx2 = []
    pesan2 = "@a"" "
    xlen = str(len(zxc))
    xlen2 = str(len(zxc)+len(pesan2)-1)
    zx = {'S':xlen, 'E':xlen2, 'M':op.param1}
    zx2.append(zx)
    zxc += pesan2
    text = zxc + " Thx For add me\n"+str(wait["autoaddpesan"])
    contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
    if wait["autoAdd"] == True:
        ki.findAndAddContactsByMid(op.param1)
        if (wait["autoaddpesan"] in [""," ","\n",None]):
            pass
        else:
            ki.sendMessage(op.param1, text, contentMetadata)
    else:
        if (wait["autoaddpesan"] in [""," ","\n",None]):
            pass
        else:
            ki.sendMessage(op.param1, text, contentMetadata)

poll.addOpInterruptWithDict({
    OpType.NOTIFIED_ADD_CONTACT: NOTIFIED_ADD_CONTACT
})

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    try:
        group_id=op.param1
        kitsune_user_id=op.param2
        if not op.param2 in wait["bots"]:
           pass
        if op.param1 in wait["kitsuneprotection"]:
         if op.param2 in wait["blacklist"]:
            try:
                random.choice(P1).kickoutFromGroup(op.param1,[op.param2])
                G = ki.getGroup(op.param1)
                G.kitsuneTicket = True
                random.choice(P1).updateGroup(G)
            except:
                ki.kickoutFromGroup(op.param1,[op.param2])
                G = ki.getGroup(op.param1)
                G.kitsuneTicket = True
                ki.updateGroup(G)
        else:
           pass
    except:
        pass

poll.addOpInterruptWithDict({
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION
})

def NOTIFIED_KICKOUT_FROM_GROUP(op):
            try:
                if mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki1.getGroup(op.param1)
                        ki1.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki1.updateGroup(G)
                        Ticket = ki1.reissueGroupTicket(op.param1)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki1.updateGroup(G)
                    except:
                        try:
                            G = ki2.getGroup(op.param1)
                            ki2.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki2.updateGroup(G)
                            Ticket = ki2.reissueGroupTicket(op.param1)
                            ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki2.updateGroup(G)
                        except:
                            try:
                                G = ki3.getGroup(op.param1)
                                ki3.kickoutFromGroup(op.param1,[op.param2])
                                G.kitsuneTicket = False
                                ki3.updateGroup(G)
                                Ticket = ki3.reissueGroupTicket(op.param1)
                                ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                                G.kitsuneTicket = True
                                ki3.updateGroup(G)
                            except:
                                pass
                if ki1mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki2.getGroup(op.param1)
                        ki2.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki2.updateGroup(G)
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        ki1.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki2.updateGroup(G)
                    except:
                        try:
                            G = ki3.getGroup(op.param1)
                            ki3.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki3.updateGroup(G)
                            Ticket = ki3.reissueGroupTicket(op.param1)
                            ki1.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki3.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki1.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki2mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki3.getGroup(op.param1)
                        backupjson_1()
                        ki3.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki3.updateGroup(G)
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki3.updateGroup(G)
                    except:
                        try:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                        except:
                            G = ki4.getGroup(op.param1)
                            ki4.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki4.updateGroup(G)
                            Ticket = ki4.reissueGroupTicket(op.param1)
                            ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki4.updateGroup(G)
                if ki3mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki4.getGroup(op.param1)
                        ki4.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki4.updateGroup(G)
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki4.updateGroup(G)
                    except:
                        try:
                            G = ki5.getGroup(op.param1)
                            ki5.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki5.reissueGroupTicket(op.param1)
                            ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki5.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            backupjson_1()
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki4mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki5.getGroup(op.param1)
                        backupjson_1()
                        ki5.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki5.updateGroup(G)
                        Ticket = ki5.reissueGroupTicket(op.param1)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki5.updateGroup(G)
                    except:
                        try:
                            G = ki6.getGroup(op.param1)
                            ki6.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki6.updateGroup(G)
                            Ticket = ki6.reissueGroupTicket(op.param1)
                            ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki6.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki5mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki6.getGroup(op.param1)
                        backupjson_1()
                        ki6.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki6.updateGroup(G)
                        Ticket = ki6.reissueGroupTicket(op.param1)
                        ki5.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki6.updateGroup(G)
                    except:
                        try:
                            G = ki7.getGroup(op.param1)
                            ki7.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki7.updateGroup(G)
                            Ticket = ki7.reissueGroupTicket(op.param1)
                            ki5.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki7.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki5.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki6mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki7.getGroup(op.param1)
                        ki7.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki7.updateGroup(G)
                        Ticket = ki7.reissueGroupTicket(op.param1)
                        ki6.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki7.updateGroup(G)
                    except:
                        try:
                            G = ki8.getGroup(op.param1)
                            ki8.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki8.updateGroup(G)
                            Ticket = ki8.reissueGroupTicket(op.param1)
                            ki6.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki8.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki6.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki7mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki8.getGroup(op.param1)
                        ki8.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki8.updateGroup(G)
                        Ticket = ki8.reissueGroupTicket(op.param1)
                        ki7.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki8.updateGroup(G)
                    except:
                        try:
                            G = ki9.getGroup(op.param1)
                            ki9.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki9.updateGroup(G)
                            Ticket = ki9.reissueGroupTicket(op.param1)
                            ki7.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki9.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki7.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki8mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki9.getGroup(op.param1)
                        ki9.kickoutFromGroup(op.param1,[op.param2])                     
                        G.kitsuneTicket = False
                        ki9.updateGroup(G)
                        Ticket = ki9.reissueGroupTicket(op.param1)
                        ki8.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki9.updateGroup(G)
                    except:
                        try:
                            G = ki10.getGroup(op.param1)
                            ki10.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki10.updateGroup(G)
                            Ticket = ki10.reissueGroupTicket(op.param1)
                            ki8.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki10.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki8.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki9mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki10.getGroup(op.param1)
                        ki10.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki10.updateGroup(G)
                        Ticket = ki10.reissueGroupTicket(op.param1)
                        ki9.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki10.updateGroup(G)
                    except:
                        try:
                            G = ki11.getGroup(op.param1)
                            ki11.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki11.updateGroup(G)
                            Ticket = ki11.reissueGroupTicket(op.param1)
                            ki9.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki11.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki9.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki10mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki11.getGroup(op.param1)
                        ki11.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki11.updateGroup(G)
                        Ticket = ki11.reissueGroupTicket(op.param1)
                        ki10.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki11.updateGroup(G)
                    except:
                        try:
                            G = ki12.getGroup(op.param1)
                            ki12.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki12.updateGroup(G)
                            Ticket = ki12.reissueGroupTicket(op.param1)
                            ki10.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki12.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki10.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki11mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki12.getGroup(op.param1)
                        ki12.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki12.updateGroup(G)
                        Ticket = ki12.reissueGroupTicket(op.param1)
                        ki11.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki12.updateGroup(G)
                    except:
                        try:
                            G = ki13.getGroup(op.param1)
                            ki13.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki13.updateGroup(G)
                            Ticket = ki13.reissueGroupTicket(op.param1)
                            ki11.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki13.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki11.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki12mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki13.getGroup(op.param1)
                        ki13.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki13.updateGroup(G)
                        Ticket = ki13.reissueGroupTicket(op.param1)
                        ki12.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki13.updateGroup(G)
                    except:
                        try:
                            G = ki14.getGroup(op.param1)
                            ki14.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki14.updateGroup(G)
                            Ticket = ki14.reissueGroupTicket(op.param1)
                            ki12.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki14.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki12.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki13mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki14.getGroup(op.param1)
                        ki14.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki14.updateGroup(G)
                        Ticket = ki14.reissueGroupTicket(op.param1)
                        ki13.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki14.updateGroup(G)
                    except:
                        try:
                            G = ki15.getGroup(op.param1)
                            ki15.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki15.updateGroup(G)
                            Ticket = ki15.reissueGroupTicket(op.param1)
                            ki13.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki15.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki13.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki14mid in op.param3:
                    if op.param2 not in wait["bots"] and op.param2 not in wait["blacklist"]:
                        wait["blacklist"].append(op.param2)
                    backupjson_1()
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki15.getGroup(op.param1)
                        ki15.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki15.updateGroup(G)
                        Ticket = ki15.reissueGroupTicket(op.param1)
                        ki14.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki15.updateGroup(G)
                    except:
                        try:
                            G = ki16.getGroup(op.param1)
                            ki16.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki16.updateGroup(G)
                            Ticket = ki16.reissueGroupTicket(op.param1)
                            ki14.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki16.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki14.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki15mid in op.param3:
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki16.getGroup(op.param1)
                        backupjson_1()
                        ki16.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki16.updateGroup(G)
                        Ticket = ki16.reissueGroupTicket(op.param1)
                        ki15.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki16.updateGroup(G)
                    except:
                        try:
                            G = ki17.getGroup(op.param1)
                            ki17.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki17.updateGroup(G)
                            Ticket = ki17.reissueGroupTicket(op.param1)
                            ki15.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki17.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki15.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki16mid in op.param3:
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki17.getGroup(op.param1)
                        backupjson_1()
                        ki17.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki17.updateGroup(G)
                        Ticket = ki17.reissueGroupTicket(op.param1)
                        ki16.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki17.updateGroup(G)
                    except:
                        try:
                            G = ki18.getGroup(op.param1)
                            ki18.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki18.reissueGroupTicket(op.param1)
                            ki16.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki18.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki16.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki17mid in op.param3:
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki18.getGroup(op.param1)
                        backupjson_1()
                        ki18.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki18.updateGroup(G)
                        Ticket = ki18.reissueGroupTicket(op.param1)
                        ki17.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki18.updateGroup(G)
                    except:
                        try:
                            G = ki20.getGroup(op.param1)
                            ki20.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki20.updateGroup(G)
                            Ticket = ki20.reissueGroupTicket(op.param1)
                            ki17.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki20.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki17.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki18mid in op.param3:
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki20.getGroup(op.param1)
                        backupjson_1()
                        ki20.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki20.updateGroup(G)
                        Ticket = ki20.reissueGroupTicket(op.param1)
                        ki18.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki20.updateGroup(G)
                    except:
                        try:
                            G = ki21.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki21.updateGroup(G)
                            Ticket = ki21.reissueGroupTicket(op.param1)
                            ki18.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki21.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki18.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki20mid in op.param3:
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki21.getGroup(op.param1)
                        backupjson_1()
                        ki21.kickoutFromGroup(op.param1,[op.param2])                        
                        G.kitsuneTicket = False
                        ki21.updateGroup(G)
                        Ticket = ki21.reissueGroupTicket(op.param1)
                        ki20.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki21.updateGroup(G)
                    except:
                        try:
                            G = ki22.getGroup(op.param1)
                            ki22.kickoutFromGroup(op.param1,[op.param2])                        
                            G.kitsuneTicket = False
                            ki22.updateGroup(G)
                            Ticket = ki22.reissueGroupTicket(op.param1)
                            ki20.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki22.updateGroup(G)
                        except:
                            G = ki.getGroup(op.param1)
                            ki.kickoutFromGroup(op.param1,[op.param2])                      
                            G.kitsuneTicket = False
                            ki.updateGroup(G)
                            Ticket = ki.reissueGroupTicket(op.param1)
                            ki20.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki.updateGroup(G)
                if ki21mid in op.param3:
                    if op.param2 in wait["bots"]:
                        return
                    try:
                        G = ki.getGroup(op.param1)
                        backupjson_1()
                        ki.kickoutFromGroup(op.param1,[op.param2])                      
                        G.kitsuneTicket = False
                        ki.updateGroup(G)
                        Ticket = ki.reissueGroupTicket(op.param1)
                        ki21.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G.kitsuneTicket = True
                        ki.updateGroup(G)
                    except:
                        try:
                            G = ki1.getGroup(op.param1)
                            ki1.kickoutFromGroup(op.param1,[op.param2])                     
                            G.kitsuneTicket = False
                            ki1.updateGroup(G)
                            Ticket = ki1.reissueGroupTicket(op.param1)
                            ki21.acceptGroupInvitationByTicket(op.param1,Ticket)
                            G.kitsuneTicket = True
                            ki1.updateGroup(G)
                        except:
                            pass


            except:
                pass
            if op.param1 in wait["kitsuneprotection"]:
                try:
                    if op.param2 in wait["bots"]:
                        pass
                    else:
                        if op.param2 in wait["bots"] or op.param2 in wait["blacklist"]:
                            pass
                        else:
                            wait["blacklist"].append(op.param2)
                            backupjson_1()
                        random.choice(P1).kickoutFromGroup(op.param1,[op.param2])
                except:
                    if op.param2 in wait["bots"]:
                        pass
                    else:
                        if op.param2 in wait["bots"] or op.param2 in wait["blacklist"]:
                            pass
                        else:
                            wait["blacklist"].append(op.param2)
                            backupjson_1()
                        random.choice(P2).kickoutFromGroup(op.param1,[op.param2])

poll.addOpInterruptWithDict({
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP
})
def appendData(to,text,Data=[]):
    a = []
    b = ki.getGroup(to)
    for i in b.kitsunemembers:
        if i.mid not in Data:
            Data.append(i.mid)
            backupjson_1()
    if Data == wait['blacklist']:
        ki.sendMessage(to, "Sukses Blacklist All Members")
    else:
        ki.sendMessage(to, "Sukses Whitelist All Members")
def removeData(to,text,Data=[]):
    a = []
    b = ki.getGroup(to)
    for i in b.kitsunemembers:
        if i.mid in Data:
            Data.remove(i.mid)
            backupjson_1()
    if Data == wait['blacklist']:
        ki.sendMessage(to, "Sukses Delete Blacklist All Members")
    else:
        ki.sendMessage(to, "Sukses Delete Whitelist All Members")
def delmimic(to,mid):
    try:
        wait["target"].remove(mid)
        backupjson_1()
        ki.delinml(to,"", mid)
    except:
        ki.delnoml(to,"", mid)
def addmimic(to,mid):
    if mid not in wait["target"]:
        wait["target"].append(mid)
        backupjson_1()
        ki.mimictoml(to,"", mid)
    else:
        ki.mimicinml(to,"", mid)
def addwl(to,mid):
    if mid in wait["bots"]:
        ki.wlinwl(to,"",mid)
    else:
        if mid in wait["blacklist"]:
            ki.wlinbl(to,"",mid)
        else:
            wait["bots"].append(mid)
            backupjson_1()
            ki.wltowl(to,"",mid)
def addbl(to,mid):
    if mid in wait["bots"]:
        ki.blinwl(to,"", mid)
    else:
        if mid not in wait["blacklist"]:
            wait["blacklist"].append(mid)
            backupjson_1()
            ki.bltobl(to,"", mid)
        else:
            ki.blinbl(to,"", mid)
def delbl(to,mid):
    try:
        wait["blacklist"].remove(mid)
        backupjson_1()
        ki.delinbl(to,"", mid)
    except:
        ki.delnobl(to,"", mid)
def delwl(to,mid):
    try:
        wait["bots"].remove(mid)
        backupjson_1()
        ki.delinwl(to,"", mid)
    except:
        ki.delnowl(to,"", mid)
def getinformation(to,mid):
    try:
        if mid in wait["bots"]:
            a = "Whitelisted: Yes"
        else:
            a = "Whitelisted: No"
        if mid in wait["blacklist"]:
            b = "Blacklisted: Yes"
        else:
            b = "Blacklisted: No"
        if mid in wait["target"]:
            c = "Mimiclisted: Yes"
        else:
            c = "Mimiclisted: No"
        zx = ""
        zxc = " 「 ID 」\nName:\n   ・"
        zx2 = []
        pesan2 = "@a"" "
        xlen = str(len(zxc))
        xlen2 = str(len(zxc)+len(pesan2)-1)
        zx = {'S':xlen, 'E':xlen2, 'M':mid}
        zx2.append(zx)
        zxc += pesan2
        zxc += "\nStatus:\n" + ki.getContact(mid).kitsuneBio + "\n\nUser ID:\n" + mid + "\n"+a+"\n"+b+"\n"+c
        contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
        ki.sendMessage(to, zxc, contentMetadata)
        ki.sendContact(to,mid)
    except:
        ginfo = ki.getGroup(to)
        try:
            gCreators = ginfo.creator.mid
            gCreator = ginfo.creator.kitsuneName
            gtime = ginfo.createdTime
        except:
            gCreators = ginfo.kitsunemembers[0].mid
            gCreator = ginfo.kitsunemembers[0].kitsuneName
            gtime = ginfo.createdTime
        if ginfo.invitee is None:
            sinvitee = "0"
        else:
            sinvitee = str(len(ginfo.invitee))
        if ginfo.kitsuneTicket == True:
            u = "Disable"
        else:
            u = "line://ti/g/" + ki.reissueGroupTicket(to)
        zx = ""
        zxc = " 「 ID 」\nGroup Name:\n" + str(ginfo.name) + "\n\nGroup ID:\n" + to + "\n\nAnggota: " + str(len(ginfo.kitsunemembers)) + "\nInvitation: " + sinvitee + "\nTicket:" + u + "\n\nCreated at:\n" + str(timeago.format(datetime.now(),gtime/1000)) + "\nby ・ "
        zx2 = []
        pesan2 = "@a"" "
        xlen = str(len(zxc))
        xlen2 = str(len(zxc)+len(pesan2)-1)
        zx = {'S':xlen, 'E':xlen2, 'M':gCreators}
        zx2.append(zx)
        zxc += pesan2
        contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
        try:
            ki.sendMessage(to, zxc, contentMetadata)
        except:
            ki.sendMessage(to, " 「 ID 」\nGroup Name:\n" + str(ginfo.name) + "\n\nGroup ID:\n" + to + "\n\nAnggota: " + str(len(ginfo.kitsunemembers)) + "\nInvitation: " + sinvitee + "\nTicket:" + u + "\n\nCreated at:\n" + str(timeago.format(datetime.now(),gtime/1000)) + "\nby ・ "+gCreator)
        ki.sendContact(to,gCreators)
def autoaddmsgclear(to,text):
    autoadd = wait["autoaddpesan"]
    msgs=" 「 Auto Add 」\nAuto add message DISABLED♪\nMessage backup:"
    msgs+="\n" + autoadd
    ki.sendMessage(to, msgs)
    wait["autoaddpesan"] = ""
    backupjson_1()
def mykeyoff(to,text):
    wait["setkey"] = ""
    backupjson_1()
    ki.sendMessage(to," 「 Mykey 」\nKey has been set to DISABLED♪")
def mykeyreset(to,text):
    wait["setkey"] = "kitsune"
    backupjson_1()
    ki.sendMessage(to," 「 Mykey 」\nKey has been set to "+wait["setkey"].title())
def autoaddoff(to,text):
    if wait['autoAdd'] == False:
        msgs=" 「 Auto Add 」\nAuto Add already DISABLED♪\nNote: Auto add message is not affected♪"
    else:
        msgs=" 「 Auto Add 」\nAuto Add set to DISABLED♪\nNote: Auto add message is not affected♪"
        wait['autoAdd']=False
    backupjson_1()
    ki.sendMessage(to,msgs)
def autoaddon(to,text):
    if wait['autoAdd'] == True:
        msgs=" 「 Auto Add 」\nAuto Add already ENABLED♪"
    else:
        msgs=" 「 Auto Add 」\nAuto Add set to ENABLED♪"
        wait['autoAdd']=True
    backupjson_1()
    ki.sendMessage(to,msgs)
def autoadd(to,text):
    if wait['autoAdd'] == True:
        if wait["autoaddpesan"] == '':
            msgs=" 「 Auto Add 」\nAdd Back: True♪\nAdd Message: False♪\n\n\n"
        else:
            msgs=" 「 Auto Add 」\nAdd Back: True♪\nAdd Message: True♪"
            msgs+="\n" + wait['autoaddpesan'] + "\n\n"
    else:
        if wait["autoaddpesan"] == '':
            msgs=" 「 Auto Add 」\nAdd Back: False♪\nAdd Message: False♪\n\n\n"
        else:
            msgs=" 「 Auto Add 」\nAdd Back: False♪\nAdd Message: True♪"
            msgs+="\n" + wait['autoaddpesan'] + "\n\n"
    ki.sendMessage(to,msgs+"\n  |Command|\n- Autoadd friend\n   Usage:"+wait["setkey"].title()+" autoadd [on|off]\n- Autoadd msg setting\n   Usage:"+wait["setkey"].title()+" autoadd msg set <text>")
def timelune(to,text):
    ki.sendMessage(to, "「 Timeline 」\n\n  |Command|\n- Timeline result\n   Usage:"+wait["setkey"].title()+" mytimeline\n- Post to timeline\n   Usage:"+wait["setkey"].title()+" mytl <query>\n- Timeline search\n   Usage:"+wait["setkey"].title()+" mytimeline <~num>\n- Timeline steal\n   Usage:"+wait["setkey"].title()+" get timeline [@]\n- Timeline steal search\n   Usage:"+wait["setkey"].title()+" get timeline [@~number]")
def set(to,text):
    try: a = ki.getGroup(to).name
    except: a = ''
    md = "「 ANBot Beta v0.1 」\n\nSettings:"
    if wait["setkey"] == '': md+="\n- Key: DISABLED"
    else: md+="\n- Key: "+ki.getProfile().kitsuneName
    md+="\n- Squad: kitsune"
    if wait["autoread"] == True: md+="\n- Auto read: ON"
    else:md+="\n- Autoread: OFF"
    md+="\n\nGroup Settings:"
    if to in wait['pname']: md+="\n- GN: "+wait['pro_name'][to]+"\n- GN Lock: ON"
    else:md+="\n- GN: "+a+"\n- GN Lock: OFF"
    if to in wait["kitsuneprotection"]: md+="\n- Protection: ON"
    else:md+="\n- Protection: OFF"
    if to in wait["autoCancel"]: md+="\n- Auto Cancel: ON"
    else:md+="\n- Auto Cancel: OFF"
    if to in wait["kitsuneurl"]: md+="\n- QR Lock: ON"
    else:md+="\n- QR Lock: OFF"
    ki.sendMessage(to,md)
def mykey(to,text):
    if wait["setkey"] == '':
        ki.sendMessage(to,"Your Key: DISABLED♪\nMykey set - Set Your Key\nMykey off - Disable Your Key\nMykey reset - Reset Your Key")
    else:
        ki.sendMessage(to,"Your Key: " + wait["setkey"].title() + "\nMykey: - Set Your Key\nMykey Off - Disable Your Key\nMykey Reset - Reset Your Key")
def debug(to,text):
    get_profile_time_start = time.time()
    get_profile = ki.getProfile()
    get_profile_time = time.time() - get_profile_time_start
    get_group_time_start = time.time()
    get_group = ki.getGroupIdsJoined()
    get_group_time = time.time() - get_group_time_start
    get_contact_time_start = time.time()
    get_contact = ki.getContact(ki1mid)
    get_contact_time = time.time() - get_contact_time_start
    ki.sendMessage(to, " 「 Debug 」\nType:\n - Get Profile\n   %.10f\n - Get Contact\n   %.10f\n - Get Group\n   %.10f" % (get_profile_time/4,get_contact_time/4,get_group_time/4))
def listpict(to,text):
    if wait["Images"] == {}:
        ki.sendMessage(to, " 「 Picture List 」\nNo Picture")
    else:
        num=1
        msgs=" 「 Picture List 」\nPicture List:"
        for a in wait["Images"]:
            msgs+="\n%i. %s" % (num, a)
            num=(num+1)
        msgs+="\n\nTotal Picture List: %i" % len(wait["Images"])
        ki.sendMessage(to, msgs)
def liststicker(to,text):
    if wait["Sticker"] == {}:
        ki.sendMessage(to, " 「 Sticker List 」\nNo Sticker")
    else:
        num=1
        msgs=" 「 Sticker List 」\nSticker List:"
        for a in wait["Sticker"]:
            msgs+="\n%i. %s" % (num, a)
            num=(num+1)
        msgs+="\n\nTotal Sticker List: %i" % len(wait["Sticker"])
        ki.sendMessage(to, msgs)
def whitelist(to,text):
    if wait["bots"] == []:
        ki.sendMessage(to, "「 Whitelist 」\n\n  |Command|\n- Add whitelist\n   Usage:"+wait["setkey"].title()+" addwl [@|~|on]\n- Delete whitelist\n   Usage:"+wait["setkey"].title()+" delwl [@|~|on]\n- Clear whitelist\n   Usage:"+wait["setkey"].title()+" clearwl")
    else:
        try:
            nama = wait['bots']
            nm1, nm2, jml = [],  [], len(nama)
            if jml <= 150:
                ki.wlmention(to,"",nama)
            if jml > 150 and jml < 500:
                for i in range(0, 150):
                    nm1 += [nama[i]]
                ki.wlmention1(to,"",nm1)
                for j in range(150, len(nama)-1):
                    nm2 += [nama[j]]
                ki.wlmention2(to,"",nm2)
        except Exception as e:
            ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
def blacklist(to,text):
    if wait["blacklist"] == []:
        ki.sendMessage(to, "「 Blacklist 」\n\n  |Command|\n- Add blacklist\n   Usage:"+wait["setkey"]+" addbl [@|~|on|repeat]\n- Delete blacklist\n   Usage:"+wait["setkey"]+" delbl [@|~|on|repeat]\n- Clear blacklist\n   Usage:"+wait["setkey"]+" clearbl")
    else:
        try:
            nama = wait['blacklist']
            nm1, nm2, jml = [],  [], len(nama)
            if jml <= 150:
                ki.blmention(to,"",nama)
            if jml > 150 and jml < 500:
                for i in range(0, 150):
                    nm1 += [nama[i]]
                ki.blmention1(to,"",nm1)
                for j in range(150, len(nama)-1):
                    nm2 += [nama[j]]
                ki.blmention2(to,"",nm2)
        except Exception as e:
            ki.sendMessage(kitsune,"「 Auto Respond 」\n"+str(e))
def mimiclisted(to,text):
    if wait["target"] == []:
        if wait['status'] == True:msgs=" 「 Mimic 」\nState: ENABLED♪\n"
        else:msgs=" 「 Mimic 」\nState: DISABLED♪\n"
        ki.sendMessage(to, msgs+"\n\n  |Command|\n- Add Mimic\n   Usage:"+wait["setkey"]+" addml [@|~]\n- Delete Mimic\n   Usage:"+wait["setkey"]+" delml [@|~]\n- ON/OFF Mimic\n   Usage:"+wait["setkey"]+" mimic [on|off]")
    else:
        try:
            if wait['status'] == True:msgs=" 「 Mimic 」\nState: ENABLED♪\n"
            else:msgs=" 「 Mimic 」\nState: DISABLED♪\n"
            ki.mcmention(to,msgs,wait['target'])
        except Exception as e:
            ki.sendMessage(to,"「 Auto Respond 」\n"+str(e))
def antimentionon(to,text):
    if to in wait["mentionChat"]:
        ki.sendMessage(to," 「 Anti Mention 」\nAnti Mention already on")
    else:
        wait["mentionChat"].append(to)
        backupjson_1()
        ki.sendMessage(to," 「 Anti Mention 」\nAnti Mention set to on")
def antimentionoff(to,text):
    if to not in wait["mentionChat"]:
        ki.sendMessage(to," 「 Anti Mention 」\nAnti Mention already off")
    else:
        wait["mentionChat"].remove(to)
        backupjson_1()
        ki.sendMessage(to," 「 Anti Mention 」\nAnti Mention set to off")
def mimicon(to):
    if wait['status'] == True:
        msgs=" 「 Mimic 」\nMimic already ENABLED♪"
    else:
        msgs=" 「 Mimic 」\nMimic set to ENABLED♪"
    wait["status"] = True
    backupjson_1()
    ki.sendMessage(to, msgs)
def mimicoff(to):
    if wait['status'] == True:
        msgs=" 「 Mimic 」\nMimic set to DISABLED♪"
    else:
        msgs=" 「 Mimic 」\nMimic already DISABLED♪"
    wait["status"] = False
    backupjson_1()
    ki.sendMessage(to, msgs)
def protecton(to,text):
    if to in wait["kitsuneprotection"]:
        ki.sendMessage(to," 「 Protection 」\nProtect already on")
    else:
        wait["kitsuneprotection"].append(to)
        backupjson_1()
        ki.sendMessage(to," 「 Protection 」\nProtect set to on")
def protectoff(to,text):
    if to not in wait["kitsuneprotection"]:
        ki.sendMessage(to," 「 Protection 」\nProtect already off")
    else:
        wait["kitsuneprotection"].remove(to)
        backupjson_1()
        ki.sendMessage(to," 「 Protection 」\nProtect set to off")
def cancelon(to,text):
    if to in wait["autoCancel"]:
        ki.sendMessage(to," 「 Cancel Invitation 」\nCancel Invitation already on")
    else:
        wait["autoCancel"].append(to)
        backupjson_1()
        ki.sendMessage(to," 「 Cancel Invitation 」\nCancel Invitation set to on")
def canceloff(to,text):
    if to not in wait["autoCancel"]:
        ki.sendMessage(to," 「 Cancel Invitation 」\nCancel Invitation already off")
    else:
        wait["autoCancel"].remove(to)
        backupjson_1()
        ki.sendMessage(to," 「 Cancel Invitation 」\nCancel Invitation set to off")
def contacton(to,text):
    if to in wait["kitsunecontact"]:
        ki.sendMessage(to," 「 Contact 」\nContact already on")
    else:
        wait["kitsunecontact"].append(to)
        backupjson_1()
        ki.sendMessage(to," 「 Contact 」\nContact set to on")
def contactoff(to,text):
    if to not in wait["kitsunecontact"]:
        ki.sendMessage(to," 「 Contact 」\nContact already off")
    else:
        wait["kitsunecontact"].remove(to)
        backupjson_1()
        ki.sendMessage(to," 「 Contact 」\nContact set to off")
def qron(to,text):
    if to in wait["kitsuneurl"]:
        ki.sendMessage(to," 「 Link Protection 」\nProtect Link already on")
    else:
        wait["kitsuneurl"].append(to)
        backupjson_1()
        ki.sendMessage(to," 「 Link Protection 」\nProtect Link set to on")
def qroff(to,text):
    if to not in wait["kitsuneurl"]:
        ki.sendMessage(to," 「 Link Protection 」\nProtect Link already off")
    else:
        wait["kitsuneurl"].remove(to)
        backupjson_1()
        ki.sendMessage(to," 「 Link Protection 」\nProtect Link set to off")
def autoreadon(to,text):
    if wait["autoread"] == True:
        ki.sendMessage(to," 「 Auto Read 」\nAuto Read already on")
    else:
        wait["autoread"] = True
        backupjson_1()
        ki.sendMessage(to," 「 Auto Read 」\nAuto Read set to on")
def autoreadoff(to,text):
    if wait["autoread"] == False:
        ki.sendMessage(to," 「 Auto Read 」\nAuto Read already off")
    else:
        wait["autoread"] = False
        backupjson_1()
        ki.sendMessage(to," 「 Link Protection 」\nAuto Read set to off")
def changedp(to,text):
    wait["ChangeDP"] = True
    backupjson_1()
    ki.sendMessage(to," 「 Profile 」\nType: Change Profile Picture\nStatus: Send the image....")
def ChangeGDP(to,text):
    wait["ChangeGDP"] = True
    backupjson_1()
    ki.sendMessage(to," 「 Group 」\nType: Change Cover Group\nStatus: Send the image....")
def setbackupprofile(to,text):
    O = ki.getProfile().picturePath
    L = ki.getProfile().kitsuneName
    U = ki.getProfile().kitsuneBio
    s = open('name.txt',"w")
    s.write(L)
    s.close()
    t = open('stat.txt',"w")
    t.write(U)
    t.close()
    p = open('photo.txt',"w")
    p.write(O)
    p.close()
    ki.sendMessage(to," 「 Backup Profil 」\nSukses Setdefault\nDisplayName:" + ki.getProfile().kitsuneName + "\n「Status 」\n" + ki.getProfile().kitsuneBio + "\n「Picture 」")
    try:
        me = ki.getProfile()
        ki.sendImageWithURL(to,"http://dl.profile.line-cdn.net/" + me.picturePath)
    except Exception as e:
        ki.sendMessage(to,"「 Auto Respond 」\n"+str(e))
def aborted(to,text):
    wait["Addimage"] = False
    wait["ChangeCover"] = False
    wait["ChangeDP"] = False
    wait["ChangeGDP"] = False
    backupjson_1()
    ki.sendMessage(to," 「 Abort 」\nType:\nAbort operation♪")
def antimentionoff(to,text):
    if to not in wait["mentionChat"]:
        return ki.sendMessage(to," 「 Anti Mention 」\nAnti Mention already off")
    else:
        wait["mentionChat"].remove(to)
        backupjson_1()
        return ki.sendMessage(to," 「 Anti Mention 」\nAnti Mention set to off")
def quote(to,text):
    r = requests.get('https://talaikis.com/api/quotes/random/')
    data = r.text
    data = json.loads(data)
    b = data['author']
    c = data['cat']
    a = data['quote']
    hasil = (" 「 Random Quote 」\nType: Quote\n   Author: "+b+"\n   Category: "+c+"\n\n   Quote: "+a)
    ki.sendMessage(to,hasil)
def wancak(to,text):
    r = requests.get("http://api-1cak.herokuapp.com/random")
    data = r.text
    data = json.loads(data)
    a = data['title'].replace('FACEBOOK Comments', ' ')
    c = data['url']
    b = data['votes']
    hasil = (" 「 1Cak 」\nType: 1Cak\n   Title: "+a+"\n   Vote: "+b+'\n   Url: '+c)
    ki.sendMessage(to,hasil)
def lurk(to):
    if to in wait2['readPoint']:
        a = "\nLurk State: ENABLED♪"
    else:
        a = "\nLurk State: DISABLED♪"
    ki.sendMessage(to," 「 Lurk 」"+a+"\nCommand:\n Lurk Point\n  Usage:"+wait["setkey"].title()+" lurk on\n Lurk Del\n  Usage:"+wait["setkey"].title()+" lurk off\n Lurk Cek\n  Usage:"+wait["setkey"].title()+" lurk result")
def profdetail(to):
    ki.sendMessage(to," 「 Profile 」\nCommand:\n Change Profile Picture\n  Usage:"+wait["setkey"].title()+" changedp\n Change Group Picture\n  Usage:"+wait["setkey"].title()+" changedp group\n Change Display Name\n  Usage:"+wait["setkey"].title()+" myname <query>\n Change Status Message\n  Usage:"+wait["setkey"].title()+" bio [enter|query]")
def lagulagu(to):
    ki.sendMessage(to," 「 Music 」\nCommand:\n Music Search\n  Usage:"+wait["setkey"].title()+" music <query>\n Music Detail\n  Usage:"+wait["setkey"].title()+" music <query|num>\n Lyric\n  Usage:"+wait["setkey"].title()+" lyric <query>")
def copy(to):
    ki.sendMessage(to," 「 Copy Profile 」\nCommand:\n Copy Profile\n  Usage:"+wait["setkey"].title()+" ikkeh on <@|~>\n Backup Profile\n  Usage:"+wait["setkey"].title()+" ikkeh off \n Set Backup Profile\n  Usage:"+wait["setkey"].title()+" ikkeh setdefault")
def steal(to):
    ki.sendMessage(to," 「 Steal 」\nCommand:\n Steal Profile Picture\n  Usage:"+wait["setkey"].title()+" steal pp [@|~]\n Steal Cover\n  Usage:"+wait["setkey"].title()+" steal cover [@|~]\n Steal Info\n  Usage:"+wait["setkey"].title()+" getid [@|~|num]\n Steal Note\n  Usage:"+wait["setkey"].title()+" get note\n Steal Note Detail\n  Usage:"+wait["setkey"].title()+" get note <|num>")
def wikipedia(to):
    ki.sendMessage(to," 「 Wikipedia 」\nCommand:\n Wikipedia Search\n  Usage:"+wait["setkey"].title()+" wikipedia <query>\n Wikipedia Detail\n  Usage:"+wait["setkey"].title()+" wikipedia <query|num>")
def movie(to):
    ki.sendMessage(to," 「 Movies 」\nCommand:\n Movies Search\n  Usage:"+wait["setkey"].title()+" movie <query>\n Movies info\n  Usage:"+wait["setkey"].title()+" movie <query|num>")
def keep(to):
    ki.sendMessage(to," 「 Keep 」\nCommand:\n Keep Search\n  Usage:"+wait["setkey"].title()+" keep <query>\n Keep cek\n Usage:"+wait["setkey"].title()+" keep <query~num>")
def image(to):
    ki.sendMessage(to," 「 Image 」\nCommand:\n Image Search\n  Usage:"+wait["setkey"].title()+" image <query>\n Deviantart Search\n  Usage:"+wait["setkey"].title()+" deviant <query>\n Deviantart detail\n  Usage:"+wait["setkey"].title()+" deviant <query|num>")
def instagram(to):
    ki.sendMessage(to, " 「 Instagram 」\nCommand:\n Instagram Search\n  Usage:"+wait["setkey"]+" instagram <username>\n Instagram post\n  Usage:"+wait["setkey"]+" instagram <username|num>")
def youtube(to):
    ki.sendMessage(to," 「 Youtube 」\nCommand:\n Youtube Search\n  Usage:"+wait["setkey"].title()+" youtube search <query>\n Youtube detail\n  Usage:"+wait["setkey"].title()+" youtube search <query|num>")
def urban(to):
    ki.sendMessage(to," 「 Urban 」\nCommand:\n Urban Search\n  Usage:"+wait["setkey"].title()+" urban <query>\n Urban detail\n  Usage:"+wait["setkey"].title()+" urban <query~num>")
def list(to):
    ki.sendMessage(to," 「 List 」\nCommand:\n List Protection\n  Usage:"+wait["setkey"]+" list protect\n List Group\n  Usage:"+wait["setkey"]+" list groups\n List Friend\n  Usage:"+wait["setkey"]+" list friends\n List Picture\n  Usage:"+wait["setkey"]+" list pict\n List Sticker\n  Usage:"+wait["setkey"]+" list sticker\n List Members\n  Usage:"+wait["setkey"]+" list groups <num>")
def help(to,text):
    a ="╔═════「 "+wait["setkey"]+ " 」═════\n║    | Command |  \n║ •  " \
    +wait["setkey"]+" help\n║ •  " \
    +wait["setkey"]+" steal\n║ •  " \
    +wait["setkey"]+" whitelist\n║ •  " \
    +wait["setkey"]+" ikkeh\n║ •  " \
    +wait["setkey"]+" whitelist\n║ •  " \
    +wait["setkey"]+" quote\n║ •  " \
    +wait["setkey"]+" mention\n║ •  " \
    +wait["setkey"]+" mimic\n║ •  " \
    +wait["setkey"]+" keep\n║ •  " \
    +wait["setkey"]+" instagram\n║ •  " \
    +wait["setkey"]+" youtube\n║ •  " \
    +wait["setkey"]+" wikipedia\n║ •  " \
    +wait["setkey"]+" music\n║ •  " \
    +wait["setkey"]+" image\n║ •  " \
    +wait["setkey"]+" 1cak\n║ •  " \
    +wait["setkey"]+" autoadd\n║ •  " \
    +wait["setkey"]+" autojoin\n║ •  " \
    +wait["setkey"]+" lurk\n║ •  " \
    +wait["setkey"]+" list\n║ •  " \
    +wait["setkey"]+" timeline\n║ •  " \
    +wait["setkey"]+" blacklist\n║ •  " \
    +wait["setkey"]+" urban\n║ •  " \
    +wait["setkey"]+" movie\n║ •  " \
    +wait["setkey"]+" profile\n║ •  " \
    +wait["setkey"]+" spam\n║ •  " \
    +wait["setkey"]+" kick\n║ •  " \
    +wait["setkey"]+" set\n║ •  " \
    +wait["setkey"]+" mayhem\n║ •  " \
    +wait["setkey"]+" abort\n║ •  " \
    +"renew\n║ •  " \
    +"mykey\n╠════════════\n"
    zx = ""
    zxc = a.title()+"║ • Creator: "
    zx2 = []
    pesan2 = "@a"" "
    xlen = str(len(zxc))
    xlen2 = str(len(zxc)+len(pesan2)-1)
    zx = {'S':xlen, 'E':xlen2, 'M':"uc11acad2da3f37a2b64e2452cbbca2c5"}
    zx2.append(zx)
    zxc += pesan2
    text = zxc+"\n║ • Selfbot Edition\n╚════════════"
    contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
    ki.sendMessage(to, text, contentMetadata)

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def backupjson_1():
    with open('1.json', 'w') as fp:
        json.dump(wait, fp, sort_keys=True, indent=4)

def backupjson_2():
    with open('2.json', 'w') as fp:
        json.dump(wait2, fp, sort_keys=True, indent=4)

def logError(text):
    with open("ki.txt","a") as b:
        b.write("%s\n%s" % (str(datetime.now()),text))

while True:
    poll.trace()
