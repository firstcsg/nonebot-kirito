from nonebot import logger
import requests


class NetEase:
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) '
            + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 '
            + 'Safari/537.36',
            'X-Real-IP': '39.156.69.79',
            'X-Forwarded-For': '39.156.69.79',
        }
        self.cookies = {
            'appver': '1.5.2'
        }

    def httpRequest(self, action, query=None):
        resp = requests.post(
        #resp = await requests.post(
            action,
            data=query,
            headers=self.header,
            timeout=3
        )
        data = resp.json()
        #data = await resp.json()
        return data

    def search(self, s, stype=1, offset=0, total='true'):
        action = 'http://music.163.com/api/search/get/web'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': 60
        }
        return self.httpRequest(action, data)
        #return await self.httpRequest(action, data)


async def search(keyword: str, result_num: int = 3):
    n = NetEase()
    song_list = []
    #data = await n.search(keyword)
    data = n.search(keyword)
    if data and data['code'] == 200:
        try:
            for item in data['result']['songs'][:result_num]:
                song_list.append(
                    {
                        'name': item['name'],
                        'id': item['id'],
                        'artists': ' '.join(
                            [artist['name'] for artist in item['artists']]
                        ),
                        'type': '163'
                    }
                )
            return {'code':0,'message':'??????','data':song_list}
        except Exception as e:
            return {'code':100,'message':'???????????????????????????, ????????????data={data}, ????????????error={e}','data':None}
    return {'code':100,'message':'??????','data':song_list}