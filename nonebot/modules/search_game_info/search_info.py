import requests;
import json;
import time;
STATS_URL= 'https://lpl.qq.com/es/stats.shtml?bmid=';#數據
VIDEO_URL= 'https://lpl.qq.com/es/video_detail.shtml?nid=';#視頻
LIVE_URL= 'https://lpl.qq.com/es/live.shtml?';#直播
RNG_DIR = r'C:\Users\Administrator\Desktop\bot\resource\rng'
def returnMsectime():
    return str(int(time.time()*1000));
def returnDayTime():
    todayStartTime = time.strftime('%Y-%m-%d', time.localtime())+'%2000:00:00';
    todayEndTime = time.strftime('%Y-%m-%d', time.localtime())+'%2023:59:59';
    return [todayStartTime,todayEndTime];
def checkTeam(teamName = '*'):
    teamList = {
        '*' :'%C8%AB%B2%BF',
        'EDG' : 1,
        'IG' : 2,
        '杭州LGD' : 4,
        'LGD' : 4,
        'OMG' : 6,
        'FPX' : 7,
        'RNG' : 8,
        'LNG' : 9,
        'RA' : 11,
        'WE' : 12,
        'JDG' : 29,
        'SN' : 41,
        'TES' : 42,
        'BLG' : 57,
        'RW' : 422,
        'TT' : 438,
        'V5' : 587,
        'UP' : 685,
    };
    if(teamName in teamList):
        return teamList[teamName];
    else:
        return False;
async def getLoLGameMessage(teamName = ""):
    if(teamName == ""):#默認檢索當天比賽信息
        teamId = checkTeam();
        day = returnDayTime();
    else:
        listArr = teamName.split(' ',2);
        teamId = checkTeam(listArr[0]);
        if(len(listArr) >= 2):#有戰隊信息和日期
            day = [listArr[1]+"%2000:00:00",listArr[1]+"%2023:59:59"];
        else:#只有戰隊信息
            if listArr[0] == "*":
                day = returnDayTime();
            else:
                day = ["",""];
    if(teamId == False):
        #return {'code':100,'message':'战队不存在'};
        return "战队不存在";
    #[CQ:face,id=86][CQ:face,id=86] 吼
    
    getLolGameInfoUrl = "https://apps.game.qq.com/lol/match/apis/searchBMatchInfo_bak.php?p8=5&p1=148&p4=&p2="+str(teamId)+"&p9="+day[0]+"&p10="+day[1]+"&p6=3&p11=&p12=&page=1&pagesize=66&_="+returnMsectime();
    result = requests.get(getLolGameInfoUrl);
    data = result.json();
    message = '[CQ:face,id=86][CQ:face,id=86]赛程信息：\n';
    if(data['status'] == '0'):
        for team in data['msg']['result']:
            if team['GameTypeName'] == '夏季赛常规赛':
                if team['MatchStatus'] == "1":
                    message += "[CQ:face,id=86]"+team['GameName']+team['GameTypeName']+team['GameProcName']+team['bMatchName']+"，时间:"+team['MatchDate']+";\n";
                elif team['MatchStatus'] == "2":
                    message += "[CQ:face,id=86]"+team['GameName']+team['GameTypeName']+team['GameProcName']+team['bMatchName']+"，正在進行：\n直播地址："+LIVE_URL+"bgid="+str(team['GameId'])+"&bmid="+str(team['bMatchId'])+"\n";
                else:
                    message += "[CQ:face,id=86]"+team['GameName']+team['GameTypeName']+team['GameProcName']+team['bMatchName']+"，\n比賽結果："+str(team['ScoreA'])+":"+str(team['ScoreB'])+"\n";
                    if team['NewsId'] != '0':
                        message += "視頻地址："+VIDEO_URL+str(team['NewsId'])+"\n";
                    else:
                        message += "視頻更新中\n";
                    message += "賽後數據："+STATS_URL+str(team['bMatchId'])+"\n";
                    #return {'code':0,'message': message};
            else:
                message += ""
        return message;
    else:
        #return {'code':100,'message': ''};
        return "无比赛信息";
async def getRngGameMessage():
    teamId = checkTeam('RNG');
    day = returnDayTime();
    getLolGameInfoUrl = "https://apps.game.qq.com/lol/match/apis/searchBMatchInfo_bak.php?p8=5&p1=148&p4=&p2="+str(teamId)+"&p9="+day[0]+"&p10="+day[1]+"&p6=3&p11=&p12=&page=1&pagesize=66&_="+returnMsectime();
    result = requests.get(getLolGameInfoUrl);
    data = result.json();
    if(data['status'] == '0'):
        if data['msg']['result'][0]['MatchStatus'] == '3':
            gameInfo = {}
            gameInfo[int(data['msg']['result'][0]['TeamA'])] = int(data['msg']['result'][0]['ScoreA']) 
            gameInfo[int(data['msg']['result'][0]['TeamB'])] = int(data['msg']['result'][0]['ScoreB'])
            teamInfo = {}
            for key,val in gameInfo.items():
                if key == 8:
                    teamInfo['rng']  = val
                else:
                    teamInfo['other'] = val
            if teamInfo['rng'] > teamInfo['other']:
                fileName = RNG_DIR+'\\'+time.strftime('%Y-%m-%d', time.localtime())+'.json'
                with open(fileName,"w") as f:
                    json.dump(data['msg']['result'][0],f)
                return True
            else:
                return False
    else:
        return False