from nonebot import on_command, CommandSession,MessageSegment
from .create_voice import create_new_voice
# on_command 装饰器将函数声明为一个命令处理器
@on_command('repeater',aliases=('复读'))
async def repeater(session:CommandSession):
    #[CQ:poke,qq=123456]
    content = session.current_arg_text.strip();
    if content !="":
        # result = await create_new_voice(content)
        # if result['code'] == 0:
        #     message = "[CQ:record,file=file:///"+result['data']+"]"
        message = '[CQ:tts,text='+content+']';
        # else:
        #     message = "你有点不对劲";
    else:
        message = "不能为空"
    
    await session.send(message);

