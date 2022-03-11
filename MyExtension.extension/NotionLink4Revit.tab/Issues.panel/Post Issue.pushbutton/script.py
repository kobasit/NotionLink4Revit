# encoding: UTF-8

# ライブラリをロード
import json, os, sys
from rpw.ui.forms import Alert
# pythonファイルをロード
import gui
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
import mylib

__doc__ = "指摘事項をNotionにアップロードします"
__title__ = "Post Issue"
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


# #====================
# # ユーザ情報取得
# #====================
# # URL
# url = "https://api.notion.com/v1/users"
# # webAPIを実行
# print("Connecting to Notion...")
# res = mylib.http("GET", url, "", headers)
# # idを抽出
# objects = json.loads(res)["results"]
# # 接続失敗時「エラー」フォーム表示
# if objects.count == 0:
#     Alert("Check the Notion API Token", title="ERROR", header="Could not connect to Notion", exit=True)
# # ユーザを取得
# users = []
# for object in objects:
#     users.append(object.name)

#====================
# タスクアップロード
#====================
# id
database_id = config.Notion_Issues_DB_ID
# URL
url = "https://api.notion.com/v1/pages"
# ステータス
status = "未着手"
# 対象のファミリID、タイトル、質問内容、回答期限
family_id, title, issue, deadline, to, fname, sname, rest_param, size_sparam, ident_param = gui.Inputform()
# jsonへ入力
values = {
    "parent": {"database_id": database_id},
    "properties": {
        "タイトル": {
            "title":[{
                "text":{
                    "content":title
                }
            }]
        },
        "ステータス": {
            "select":{
                "name":status
            }
        },
        "from": {
            "people":[{
                "id": "93ce9bff-fcec-48b1-a316-2a02acde824c",
                "person": {
                    "email": "dz19166@shibaura-it.ac.jp"
                }
            }]
        },
        "to": {
            "people":[{
                "id": "24910fa1-9c57-4d15-b504-df0c2455774b",
                "person": {
                    "email": "shotarotakazoe2000@gmail.com"
                }
            }]
        },
        "回答期限": {
            "date":{
                "start":deadline
            }
        },
        "ファミリID": {
            "multi_select":[{
                "name":family_id
            }]
        }
    }
    }
# bodyを文字列化
data = json.dumps(values, ensure_ascii=False)
# webAPIを実行
print("Uploading Issue...")
mylib.http("POST", url, data, headers)


#====================
# ページID取得
#====================
# URL
url = "https://api.notion.com/v1/databases/{}/query/".format(database_id)
# jsonへ入力
values = {
    "filter": {
        "property": "タイトル",
        "text": {
            "equals": title
        }
    }
    }
# bodyを文字列化
data = json.dumps(values, ensure_ascii=False)
# webAPIを実行
print("Get Page ID...")
res = mylib.http("POST", url, data, headers)
# 接続失敗時「エラー」フォーム表示
if "results" not in res:
    Alert("Check the Notion API Token", title="ERROR", header="Could not Uppload Issue", exit=True)
objects = json.loads(res)["results"]
page_id = objects[0]["id"]


# #====================
# # ページ書き込み
# #====================
# # URL
# url = "https://api.notion.com/v1/blocks/{}/children".format(page_id)
# # jsonへ入力
# values = {
#     "children": [		
#         {
# 			"object": "block",
# 			"type": "child_database",
# 			"child_database": {
#                 "title": "ファミリパラメータ",
#                 'properties': {
#                     'Grocery item': {
#                         'type': 'title',
#                         'title': [{
#                             'type': 'text',
#                             'text': {
#                                 'content': 'Tomatoes'
#                             }
#                         }]
#                     },
#                 }
#             }
# 		},        
#         {
# 			"object": "block",
# 			"type": "heading_1",
# 			"heading_1": {
# 				"text": [{
#                     "type": "text",
#                     "text": {
#                         "content": "指摘事項"
#                     }
#                 }]
# 			}
# 		},
# 		{
# 			"object": "block",
# 			"type": "paragraph",
# 			"paragraph": {
# 				"text": [{
#                     "type": "text",
#                     "text": {
#                         "content": issue
# 					}
# 				}]
# 			}
# 		}
# 	]
#     }
# # bodyを文字列化
# data = json.dumps(values, ensure_ascii=False)
# # webAPIを実行
# print("Uploading Family Data...")
# res = http("PATCH", url, data, headers)


#====================
# ファミリアップロード
#====================
# id
database_id = config.Notion_Family_DB_ID
# URL
url = "https://api.notion.com/v1/pages"
# パラメータ名
params, paramnames = mylib.GetParam(family_id)
# jsonへ入力
for p, pname in zip(params, paramnames):
    values = {
        "parent": {"database_id": database_id},
        "properties": {
            "ファミリタイプ": {
                "title":[{
                    "text":{
                        "content":sname
                    }
                }]
            },
            "ファミリカテゴリ": {
                "multi_select":[{
                    "name":fname
                }]
            },
            "ファミリID": {
                "multi_select":[{
                    "name":family_id
                }]
            },
            "パラメータ名": {
                "rich_text":[{
                    "text":{
                        "content":pname
                    }
                }]
            },
            "パラメータ": {
                "rich_text":[{
                    "text":{
                        "content":p
                    }
                }]
            },
            "ロック": {
                "checkbox":False
            },
            "タスク": {
                "relation":[{
                    "id":page_id
                }]
            }
        }
        }  
    # bodyを文字列化
    data = json.dumps(values, ensure_ascii=False)
    # POST
    print("Uploading Family Data...")
    mylib.http("POST", url, data, headers)
