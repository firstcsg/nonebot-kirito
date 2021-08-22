import requests
import os
API_KEY = '4312149460b89a1c797928=2'
R = 0
NUM = 1
SEARCH_URL = 'http://api.lolicon.app/setu/'
DIR = r'C:\Users\Administrator\Desktop\bot\resource\pornography'
async def getPornographyInfo(keyword=""):
    params = {'apikey':API_KEY,'r18':R,'keyword':None,'num':NUM}
    if keyword != "":
        listArr = keyword.split(' ',2)
        params['keyword'] = listArr[0]
    result = requests.get(SEARCH_URL,params=params)
    data = result.json()
    if data['code'] == 0:
        
        fileName = str(data['data'][0]['uid'])+'.jpg'
        fileRes = getFile(fileName)
        if fileRes == True:
            data['data'][0]['url'] = DIR+'\\'+str(data['data'][0]['uid'])+'.jpg'
            return {'code':0,'message':'成功','data':data['data']}
            #return {'code':0,'message':'成功','data':data['data']}
        else:
            fileInfo = setFile(data['data'][0])
            if fileInfo == True:
                data['data'][0]['url'] = DIR+'\\'+str(data['data'][0]['uid'])+'.jpg'
                return {'code':0,'message':'成功','data':data['data']}
            else:
                return {'code':1,'message':'缓存图片失败','data':data['data']}
    else:
        return {'code':100,'message':'获取涩图失败','data':None}
def setFile(fileInfo=""):
    try:
        file = requests.get(fileInfo['url'])
        fileName = DIR+'\\'+str(fileInfo['uid'])+'.jpg'
        open(fileName, 'wb').write(file.content)
        fileJson = fileInfo
        fileJsonName =  DIR+'\\'+str(fileInfo['uid'])+'.json'
        with open(fileJsonName,"w") as f:
            json.dump(fileJson,f)
        return True
    except:
        return False
    
def getFile(fileName=""):
    fileList = os.listdir(DIR)
    if fileName in fileList:
        return True
    else:
        return False