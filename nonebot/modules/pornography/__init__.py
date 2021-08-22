from nonebot import on_command, CommandSession
from .pornography import getPornographyInfo

# on_command 装饰器将函数声明为一个命令处理器
@on_command('pornography',aliases=('涩图','色图'))
async def pornography(session: CommandSession):
    #team = session.get('team', prompt='你想查询哪个战队的赛程？');
    # 获取当天该战队的信息
    #teamGameInfo = await getLoLGameMessage(team);
    #推送
    keyword = session.current_arg_text.strip().upper()
    get_pornography_info = await getPornographyInfo(keyword)
    if get_pornography_info['code'] == 0:
        for pornography_info in get_pornography_info['data']:
            message = 'title: '+str(pornography_info['title'])+'\nauthor: '+str(pornography_info['author'])+'\npid:'+str(pornography_info['uid'])+'\n[CQ:image,type=show,id=40004,file=file:///'+pornography_info['url']+']'
    elif get_pornography_info['code'] == 1:
         for pornography_info in get_pornography_info['data']:
            message = 'title: '+str(pornography_info['title'])+'\nauthor: '+str(pornography_info['author'])+'\npid:'+str(pornography_info['uid'])+'\n[CQ:image,type=show,id=40004,file='+pornography_info['url']+']'
    else:
        message = get_pornography_info['message']
    # print(session);
    await session.send(message);
