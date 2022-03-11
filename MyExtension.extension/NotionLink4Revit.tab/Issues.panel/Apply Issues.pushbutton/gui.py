# encoding: UTF-8

# ライブラリをロード
import clr, json
from rpw.ui.forms import *


# 入力フォーム
def Displayform(objects):
    # フォームを表示
    components = [Label('Revitへ適用するタスクを選択してください'),
        Separator(),
        CheckBox('checkboxAll', '完了したタスクを全て選択'),
        Separator()]
    for i, obj in enumerate(objects, 1):
        props = obj["properties"]
        title = props["タイトル"]["title"][0]["plain_text"]
        status = props["ステータス"]["select"]["name"]
        if status == "完了":
            components.append(CheckBox('checkbox' + str(i), "[" + status + "] " + title))
        else:
            components.append(Label("　 [" + status + "] " + title))
    components.append(Separator())
    components.append(Button('Apply'))
    form = FlexForm('Check Issues List', components)
    form.show()
    # 集計表をフィルタ
    objects_to_apply = []
    for i, obj in enumerate(objects, 1):
        props = obj["properties"]
        status = props["ステータス"]["select"]["name"]
        if status == "完了":
            if form.values['checkbox' + str(i)] or form.values['checkboxAll']:
                objects_to_apply.append(obj)
    form.close
    return objects_to_apply