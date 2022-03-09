# encoding: UTF-8

# ライブラリをロード
from rpw.ui.forms import *
from rpw import db, ui


def GetObject():
    ref = ui.Pick.pick_element()
    elem = ref.get_element()
    id = ref.id
    fname = elem.get_family().name
    sname = elem.get_symbol().name
    return id, fname, sname


# 入力フォーム1
def Inputform():
    id, fname, sname = GetObject()

    components = [Label('From：ゾエ'),
        Label('To：'),
        ComboBox('combobox1', {'zoe': "zoe", 'ゾエ': "ゾエ", '全員': "全員"}),
        Label('タイトル：'),
        TextBox('textbox1', Text=""),
        Label('指摘事項：'),
        TextBox('textbox2', Text=""),
        Label('回答期限：'),
        TextBox('textbox3', Text="2022-02-DD"),
        Separator(),
        Label('ファミリ：' + fname),
        Label('タイプ：' + sname),
        Label('ファミリID：' + str(id)),
        Separator(),
        CheckBox('checkbox1', 'パラメータ：拘束（インスタンス）'),
        CheckBox('checkbox2', 'パラメータ：寸法（インスタンス）'),
        CheckBox('checkbox3', 'パラメータ：識別情報（インスタンス）'),
        CheckBox('checkbox4', 'パラメータ：構造（タイプ）'),
        Separator(),
        Button('Post')]

    form = FlexForm('入力フォーム', components)
    form.show()

    to = form.values['combobox1']
    title = form.values['textbox1']
    issue = form.values['textbox2']
    family_id = str(id)
    deadline = form.values['textbox3'] + "T24:00:00.000Z"
    rest_param = form.values['checkbox1']
    size_sparam = form.values['checkbox2']
    ident_param = form.values['checkbox3']
    form.close

    return family_id, title, issue, deadline, to, fname, sname, rest_param, size_sparam, ident_param