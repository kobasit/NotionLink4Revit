# encoding: UTF-8

# ライブラリをロード
import clr
from rpw.ui.forms import *

# Import RevitAPI
clr.AddReference("RevitAPI")
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
doc = __revit__.ActiveUIDocument.Document


# 集計表を取得
def GetSchedules(doc):
    views = List[Element]()
    for v in FilteredElementCollector(doc).OfClass(View).ToElements():
        if not v.IsTemplate and v.ViewType == ViewType.Schedule:
            views.Add(v)
    return views


# 集計表のデータを取得
def GetScheduleItems(view):
    schedule = view
    # 集計表の行と列を数える
    table = schedule.GetTableData().GetSectionData(SectionType.Body)
    nRows = table.NumberOfRows
    nColumns = table.NumberOfColumns
    # 行・列ごとにデータを取り出す
    props, items = [], []
    for row in range(nRows):
        dataListColumn = []
        if row == 0:
            for column in range(nColumns):
                data = str(TableView.GetCellText(schedule, SectionType.Body, row, column))
                props.append(data)
        elif row > 1:
            for column in range(nColumns):
                data = str(TableView.GetCellText(schedule, SectionType.Body, row, column))
                dataListColumn.append(data)
            items.append(dataListColumn)
    return props, items


# 入力フォーム
def Inputform():
    # 集計表を取得
    views = GetSchedules(doc)
    # フォームを表示
    components = [Label('アップロードする集計表を選択してください'),
        Separator(),
        CheckBox('checkboxAll', '全て選択'),
        Separator()]
    for i, view in enumerate(views, 1):
        components.append(CheckBox('checkbox' + str(i), view.Title))
    components.append(Separator())
    components.append(Button('Upload'))
    form = FlexForm('Upload Schedules', components)
    form.show()
    # 集計表をフィルタ
    ScheduleViews, ScheduleTitles = [],[]
    for i, view in enumerate(views, 1):
        if form.values['checkbox' + str(i)] or form.values['checkboxAll']:
            ScheduleViews.append(view)
            ScheduleTitles.append(view.Title.replace('集計: ', ''))
    form.close
    # 集計表のデータを取得
    ScheduleProps, ScheduleItems = [],[]
    for view in ScheduleViews:
        props, items = GetScheduleItems(view)
        ScheduleProps.append(props)
        ScheduleItems.append(items)

    return ScheduleTitles, ScheduleProps, ScheduleItems