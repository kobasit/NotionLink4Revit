# encoding: UTF-8

# ライブラリをロード
import json, os, sys
# rpwフォーム
from rpw.ui.forms import Alert
# pythonファイルをロード
import gui
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
import mylib

__doc__ = "集計表をNotionにアップロードします"
__title__ = "Upload Schedule"
__author__ = "shotaro takazoe"
__persistentengine__ = True

# 設定ファイル（config.json）から設定情報を取得
class Config:
    # カレントディレクトリを設定
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # iniファイルの絶対パスを取得
    json_file = open("../../config.json", "r")
    json_data = json.load(json_file)
    # 各設定情報を読込
    Notion_token = json_data["Notion_Token"]
    Notion_Schedule_Page_ID = json_data["Notion_Schedule_Page_ID"]


#====================
# ヘッダー作成
#====================
config = Config()
# Token
token = "Bearer " + str(config.Notion_token)
# headers
headers = {
            "Authorization": token,
            "Notion-Version": "2021-08-16",
            }


#====================
# 集計表作成
#====================
# id
page_id = config.Notion_Schedule_Page_ID
# 集計表データ
ScheduleTitles, ScheduleProps, ScheduleItems = gui.Inputform()
# 集計表ごとに処理
for title, props in zip(ScheduleTitles, ScheduleProps):

    # URL
    url = "https://api.notion.com/v1/databases/"
    # プロパティ名を入力
    properties = {}
    for prop in props:
        properties[prop] = {
            "rich_text":{}
        }
    properties["dummy"] = {
        "title":{}
    }
    # jsonへ入力
    values = {
        "parent": {
            "type": "page_id",
            "page_id": page_id
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": title
                }
            }
        ],
        "properties": properties
        }
    # bodyを文字列化
    data = json.dumps(values, ensure_ascii=False)
    # webAPIを実行
    print("Create Schedule...")
    res = mylib.http("POST", url, data, headers)


#====================
# ページID取得
#====================
# URL
url = "https://api.notion.com/v1/blocks/{}/children?page_size=100".format(page_id)
# webAPIを実行
print("Get Page ID...")
res = mylib.http("GET", url, "", headers)
# 接続失敗時「エラー」フォーム表示
if "results" not in res:
    Alert("Check the Notion API Token", title="ERROR", header="Could not Uppload Issue", exit=True)
# idを抽出
objects = json.loads(res)["results"]
database_ids = {}
for obj in objects:
    if obj["type"] == "child_database":
        database_ids[obj["child_database"]["title"]] = obj["id"]


#====================
# データアップロード
#====================
# 集計表ごとに処理
for title, props, items in zip(ScheduleTitles, ScheduleProps, ScheduleItems):
    # id
    database_id = database_ids[title]
    # URL
    url = "https://api.notion.com/v1/pages"
    # 
    for item in items:
        # プロパティ名を入力
        properties = {}
        for prop, i in zip(props, item):
            properties[prop] = {
                "rich_text":[{
                    "text":{
                        "content":i
                    }
                }]
            }
        # jsonへ入力
        values = {
            "parent": {"database_id": database_id},
            "properties": properties
            } 
        # bodyを文字列化
        data = json.dumps(values, ensure_ascii=False)
        # POST
        print("Uploading Schedule Data...")
        mylib.http("POST", url, data, headers)
