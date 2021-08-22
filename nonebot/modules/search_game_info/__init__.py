from nonebot import on_command, CommandSession
from .search_info import getLoLGameMessage,getRngGameMessage
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import time
import os
RNG_DIR = r'C:\Users\Administrator\Desktop\bot\resource\rng'
__plugin_name__ = 'LOL比赛信息查询'
__plugin_usage__ = r"""
赛事查询

赛事查询/赛程查询  [*/战队名] [日期：格式2021-07-10]
"""
# on_command 装饰器将函数声明为一个命令处理器
@on_command('search_game_info',aliases=('赛程查询','赛事查询'))
async def searchGameInfo(session: CommandSession):
    #team = session.get('team', prompt='你想查询哪个战队的赛程？');
    # 获取当天该战队的信息
    #teamGameInfo = await getLoLGameMessage(team);
    #推送
    teamName = session.current_arg_text.strip().upper()
    teamGameInfo = await getLoLGameMessage(teamName)
    # print(session);
    await session.send(teamGameInfo)
@nonebot.scheduler.scheduled_job('interval', minutes=3)
async def sendRng():
    bot = nonebot.get_bot()
    #
    try:
        fileName = RNG_DIR+'\\'+time.strftime('%Y-%m-%d', time.localtime())+'.json'
        if not os.path.exists(fileName):
            result = await getRngGameMessage()
            if result:
                path = r"C:\Users\Administrator\Desktop\bot\resource\rng\rngpengbei.jpg"
                message = "[CQ:at,qq=452034575][CQ:face,id=86][CQ:face,id=86]我们是冠军[CQ:face,id=86][CQ:face,id=86]\n[CQ:image,file=file:///"+path+"]"
                await bot.send_group_msg(group_id=488924485,message=message)
            else:
                pass
        else:
            pass
    except CQHttpError:
        pass
# search_game_info.args_parser 装饰器将函数声明为 search_game_info 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
# @search_game_info.args_parser
# async def _(session: CommandSession):
#     # 去掉消息首尾的空白符 并转成大写
#     stripped_arg = session.current_arg_text.strip().upper();
#     if session.is_first_run:
#         # 该命令第一次运行（第一次进入命令会话）
#         if stripped_arg:
#             # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
#             # 例如用户可能发送了：天气 南京
#             session.state['team'] = stripped_arg;
#         return

#     if not stripped_arg:
#         # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
#         # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
#         session.pause('要查询的战队名称不能为空呢，请重新输入');

#     # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
#     session.state[session.current_key] = stripped_arg;
