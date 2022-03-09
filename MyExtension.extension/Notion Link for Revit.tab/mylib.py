# encoding: UTF-8

# ライブラリをロード
import time
from System.Net import WebRequest
from System.Text import UTF8Encoding
from System.IO import StreamReader
from System.Net import ServicePointManager
from System.Net import SecurityProtocolType
from System.Net import WebException
from rpw.ui.forms import *
from rpw import db, ui

def http(method, url, data_string=None, header={}, retry=3):
    ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls11 | SecurityProtocolType.Tls12
    request = WebRequest.Create(url)
    request.UseDefaultCredentials = True
    request.Method = method
    request.ContentLength = 0
    
    for k,v in header.items():
        request.Headers.Add(k,v)
    
    if data_string:
        request.ContentType = "application/json"
        encoding = UTF8Encoding()
        data = encoding.GetBytes(data_string)
        request.ContentLength = data.Length
        stream = request.GetRequestStream()
        stream.Write(data, 0, data.Length)
        stream.Close()

    try:
        response = request.GetResponse()
        print (response.StatusDescription)
        dataStream = response.GetResponseStream()
        reader = StreamReader(dataStream)
    
        responseFromServer = reader.ReadToEnd()
            
        reader.Close()
        dataStream.Close()
        response.Close()
        return responseFromServer

    except WebException as e : 
        if e.Response.StatusDescription == "Not Found" and retry>0:
            time.sleep(10)
            return http(method, url, data_string, header, retry-1)

        print (e.Response.StatusDescription)
        dataStream = e.Response.GetResponseStream()
        reader = StreamReader(dataStream)
    
        responseFromServer = reader.ReadToEnd()
        print (responseFromServer)
    
        reader.Close()
        dataStream.Close()

# ファミリIDからパラメータとパラメータ名のリストを取得
def GetParam(id):
    elem = db.Element.from_int(int(id))
    #paramnames = db.ParameterSet(elem)
    paramnames = ["基準レベル", "基準レベル オフセット", "上部レベル", "上部レベル オフセット"]
    params = []
    for pname in paramnames:
        p = elem.parameters[pname].value
        if type(p)==str:
            params.append(p)
        elif type(p)==float:
            params.append(str(ft2mm(p)))
        else:
            element = db.Element.from_id(p)
            name = element.name
            params.append(str(name))
    return params, paramnames

def mm2ft(mm):
    ft = mm / 304.8
    return ft

def ft2mm(ft):
    mm = round(ft * 304.8)
    return mm