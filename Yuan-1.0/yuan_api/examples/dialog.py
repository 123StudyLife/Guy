import os
import sys
sys.path.append(os.path.abspath(os.curdir))

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
    yuan.add_example(Example(inp=data[i], out=data[i+1]))


print("====夸夸机器人====")

while(1):
    print("输入Q退出")
    prompt = input("我：")
    if prompt.lower() == "q":
        break
    response = yuan.submit_API(prompt=prompt,trun="”")
    print(response+"”")
