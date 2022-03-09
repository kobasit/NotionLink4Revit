# encoding: UTF-8

# ライブラリをロード
import json, os, sys
# pythonファイルをロード
import gui
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
import mylib
# RPW
from rpw.ui.forms import *
from rpw import db, DB


__doc__ = "指摘事項を表示・Revitに反映します"
__title__ = "Apply Issues"
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
    Notion_Issues_DB_ID = json_data["Notion_Issues_DB_ID"]
    Notion_Family_DB_ID = json_data["Notion_Family_DB_ID"]

# # ファミリパラメータを取得
# def GetFamilyParam(objects):

# # ファミリを変更
# def ApplyFamilyParam(id):


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
# タスクを取得
#====================
# id
database_id = config.Notion_Issues_DB_ID
# URL
url = "https://api.notion.com/v1/databases/{}/query/".format(database_id)
# jsonへ入力
values = {
    "sorts": [{
        "property": "ステータス",
        "direction": "ascending"
    }]
    }
# bodyを文字列化
data = json.dumps(values, ensure_ascii=False)
# webAPIを実行
print("Get Issues Data...")
res = mylib.http("POST", url ,data, headers)
Issues = json.loads(res)["results"]


#====================
# ファミリDBをダウンロード
#====================
# id
database_id = config.Notion_Family_DB_ID
# URL
url = "https://api.notion.com/v1/databases/{}/query/".format(database_id)
# webAPIを実行
res = mylib.http("POST", url ,"", headers)
objects = json.loads(res)["results"]


#====================
# 選択したタスクのファミリパラメータを取得・反映
#====================
# タスクを選択
Issues = gui.Displayform(Issues)
# タスクごとに処理
with db.Transaction('Apply Issues'):
    for Issue in Issues:
        # ファミリDBの要素IDを取得
        family_id = Issue["properties"]["ファミリID"]["multi_select"][0]["name"]
        # id
        database_id = config.Notion_Family_DB_ID
        # 対象のファミリパラメータを取得
        familys = []
        for obj in objects:
            if obj["properties"]["ファミリID"]["multi_select"][0]["name"] == family_id:
                familys.append(obj)
        # ファミリのパラメータを変更
        element = db.Element.from_int(int(family_id))

        for family in familys:
            param_name = family["properties"]["パラメータ名"]["rich_text"][0]["plain_text"]
            param = family["properties"]["パラメータ"]["rich_text"][0]["plain_text"]
            value_type = type(element.parameters[param_name].value)
            if value_type == str:
                element.parameters[param_name].value = param
            elif value_type == float:
                element.parameters[param_name].value = mylib.mm2ft(float(param))
            # elif value_type == DB.ElementId:
            #     element.parameters[param_name].value = param
            elif value_type == int:
                element.parameters[param_name].value = mylib.mm2ft(int(param))
