from nonebot import on_command, CommandSession
import datetime
import typing
import json
from .search_net_or_cloud_music import search as search163
from .search_qq_music import search as searchqq
__plugin_name__ = '点歌'
__plugin_usage__ = r"""
点歌


"""
cool_down = datetime.timedelta(minutes=3)  # 冷却时间
expire = datetime.timedelta(minutes=2)

temp = {}
last_check = {}
# on_command 装饰器将函数声明为一个命令处理器
@on_command('music',aliases=('点歌'))
async def music(session: CommandSession):
    music_name = session.current_arg_text.strip();
    if not music_name:
        music_name = session.get('music', prompt='你想点什么歌？')
    music_info = await search163(music_name);
    if music_info['code'] == 0:
        music_message = '音乐信息：\n';
        # for music_arr in music_info['data']:
        #     music_message += str(music_arr['id']) + str(music_arr['name']) + str(music_arr['artists'])+";\n";
        for idx,song in enumerate(music_info['data']):
            music_message += f'{idx}. {song["name"]} - {song["artists"]}\n'
            temp[str(idx)] = song
    else:
        music_message = music_info['messsage']
    await session.send(music_message);
# search_game_info.args_parser 装饰器将函数声明为 search_game_info 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@music.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符 并转成大写
    stripped_arg = session.current_arg_text.strip().upper();
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['music'] = stripped_arg;
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('请输入音乐名称');

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg;
# on_command 装饰器将函数声明为一个命令处理器
@on_command('select',aliases=('选择'))
async def music(session: CommandSession):
    select_name = session.current_arg_text.strip();
    message = "";
    if temp[select_name]:
        message = f'[CQ:music,type=163,id={temp[select_name]["id"]}]';
    await session.send(message);