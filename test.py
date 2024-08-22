import json
import time

import requests

##Select Languages and Obtain the conversion table.
language = input("Language/语言(type 'EN'/输入'CN'):")

if language in ["en", "En", "EN"]:
    data_path = input("the file that need to be converted(json)：")
    Hutao_version = input("The version of Snap Hutao(Default:1.11.0.0)：")
    ##Obtain the conversion table.
    url = "https://api.uigf.org/dict/genshin/en.json"
    file = requests.get(url)
    open("en-us.json", "wb").write(file.content)
    with open("en-us.json", "r", encoding="utf-8") as f:
        data_json = f.read()
        # data_json = data_json.replace("\n", "").replace("\r", "")
    print("Translation file 'en-us.json' downloaded successfully.")

elif language in ["cn", "Cn", "CN"]:
    data_path = input("需要转换的文件(json)：")
    Hutao_version = input("Snap Hutao 版本(默认:1.11.0.0)：")
    ##Obtain the conversion table.
    url = "https://api.uigf.org/dict/genshin/chs.json"
    file = requests.get(url)
    open("zh-cn.json", "wb").write(file.content)
    with open("zh-cn.json", "r", encoding="utf-8") as f:
        data_json = f.read()
        # data_json = data_json.replace("\n", "").replace("\r", "")
    print("Translation file 'zh-cn.json' downloaded successfully.")

else:
    print("The language you entered is not supported.")
    exit()

##Set Snap Hutao version. If it's empty, use the default version:1.11.0.0
##Default version:1.11.0.0
if not Hutao_version:
    Hutao_version = "1.11.0.0"
##Load uigf-json
data_json = json.loads(data_json)

##Obtain 'data',the file that need to be converted
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

##Head,A Declaration of time/app/app_version
data_head = {
    "info": {
        "export_timestamp": 0,
        "export_app": "Snap Hutao",
        "export_app_version": "0",
        "version": "v4.0",
    },
    "hk4e": [{"uid": "", "timezone": 0}],
}

##Obtain timestamp and timezone.
tz = time.strftime("%z", time.localtime())
for i in tz:
    if i.isdigit():
        if int(i) == 0:
            tz = tz.replace(i, "")
real_tz = int(tz) - 8
ts = int(time.time())  # 时间戳

data_list = data["list"]
for i in data_list:
    item_name = i["name"]
    i["item_id"] = data_json[item_name]
    item_name.encode("unicode_escape").decode("unicode_escape")
data_head["hk4e"][0].update({"list": data["list"]})
data_head["info"]["export_timestamp"] = int(ts)
data_head["info"]["export_app_version"] = Hutao_version
data_head["hk4e"][0]["uid"] = str(data["info"]["uid"])
data_head["hk4e"][0]["timezone"] = str(real_tz)
fild_newName = data["list"][0]["uid"] + "UIGF.json"

with open(fild_newName, "w", encoding="utf-8") as file:
    json.dump(data_head, file, ensure_ascii=False)

print(f"Conversion file '{fild_newName}' generated successfully.")
