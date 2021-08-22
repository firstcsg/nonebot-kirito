import nonebot;
from nonebot import on_command, CommandSession;

# on_command 装饰器将函数声明为一个命令处理器
@on_command('poke',aliases=('戳一戳','笃'))
async def poke(session:CommandSession):
    #[CQ:poke,qq=123456]
    user_info = session.current_arg.strip();
    if user_info:
        user_id = await getUser(user_info);
        if user_id != None:
            message = '[CQ:poke,qq='+str(user_id)+']';
    else:
        message = "对象不能为空";
    await session.send(message);
async def getUser(message=""):
    uid = message.replace("[CQ:at,qq=","").replace("]","");
    if uid:
        return uid;
    else:
        return None;