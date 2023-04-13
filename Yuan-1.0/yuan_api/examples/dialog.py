import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.curdir))

from urllib.parse import quote

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

from yuan_api.inspurai import Yuan, set_yuan_account,Example

# 1. set account
set_yuan_account("S_Y_Deng", "17378325521")  # 输入您申请的账号和手机号

# 2. initiate yuan api
# 注意：engine必需是['base_10B','translate','dialog','rhythm_poems']之一，'base_10B'是基础模型，'translate'是翻译模型，'dialog'是对话模型，'rhythm_poems'是古文模型
yuan = Yuan(engine='dialog',
            input_prefix="问：“",
            input_suffix="”",
            output_prefix="答：“",
            output_suffix="”",
            append_output_prefix_to_query=True,
            topK=5,
            temperature=1,
            topP=0.8,
            frequencyPenalty=1.2)
# 3. add examples if in need.

with open('greet.txt', 'r', encoding='utf-8') as f:
    data = [line.strip() for line in f.readlines() if line.strip()]

for i in range(0, len(data), 2):
    yuan.add_example(Example(inp=data[i], out=data[i + 1]))
#Wechaty

async def on_message(msg: Message):
    """
    Message Handler for the Bot
    """
    text = msg .text()
    prompt = text
    response = yuan.submit_API(prompt=prompt, trun="”")
    await msg.say(response)

    file_box = FileBox.from_url(
        'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
        'u=1116676390,2305043183&fm=26&gp=0.jpg',
        name='test.jpg'
    )
    await msg.say(file_box)


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    """
    Scan Handler for the Bot
    """
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + quote(qrcode))


async def on_login(user: Contact):
    """
    Login Handler for the Bot
    """
    print(user)
    # TODO: To be written

async def main():
    """
    Async Main Entry
    """

    os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_padlocal_34bb70653e194842a29a425e3629625f'
    os.environ['WECHATY_PUPPET'] = 'wechaty-puppet-padlocal'

    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

asyncio.run(main())
