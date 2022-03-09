# encoding: UTF-8

# ライブラリをロード
import json, os, sys
# pythonファイルをロード
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
import mylib


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
# DBをダウンロード
#====================
# id
database_id = config.Notion_Family_DB_ID
# URL
url = "https://api.notion.com/v1/databases/{}/query/".format(database_id)
# webAPIを実行
res = mylib.http("POST", url ,"", headers)
objects = json.loads(res)["results"]
# 結果を表示
print(res)