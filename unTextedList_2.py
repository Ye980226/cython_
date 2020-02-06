import datetime
import json
import requests
import re
import pandas as pd
import threading
# 多线程如何返回值
class MyThread(threading.Thread):
 
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
        self.result = self.func(*self.args)
 
    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def foo(classname,Session,headers,data,Field,current_datetime):
    # data['condition']='{"cond":{"likeC":[{"Type":"DATE","Compare":"=","Field":"%s","FieldName":"报送日期","ConditionValue":"%s"},{"Field":"SID","Type":"text","ConditionValue":"%s 00:00:00-601-20170036-%s-学生","Compare":"=","url":true}]},"tcond":{"qk":""}}'%(Field,current_datetime,current_datetime,classname)
    data['condition']='{"cond":{"likeC":[{"Type":"DATE","Compare":"=","Field":"%s","FieldName":"报送日期","ConditionValue":"%s"},{"Field":"SID","Type":"text","ConditionValue":"%s 00:00:00-601-20170036-%s-学生","Compare":"=","url":true}]},"tcond":{"qk":""}}'%(Field,current_datetime,current_datetime,classname)
    results=[]
    result=""
    for i in range(1,4):
        data['pageNow']=str(i)
        r=Session.post("http://mcenter.lixin.edu.cn/r/jd",data=data,headers=headers)
        content=r.json()
        print(content)
        results.extend(content['data']['maindata']['items'])
    
    XMS=[]
    for xm in results:
        XMS.append(xm['XM'])
    # print(XMS)
    classmates=set()
    with open("./classname/%s.txt"%classname,"r") as f:
        # for xm in XMS:
            # f.write(xm+"\n")
        for line in f:
            classmates.add(line.replace("\n",""))
            
    XMS=set(XMS)
    diff=classmates-XMS
    # print(XMS)
    j=1
    result+=classname+"\n"
    for classmate in diff:
        result+=str(j)+"."+classmate+"\n"
        j+=1
    result+="完成度%d/%d"%(len(XMS),len(classmates))
    result+="\n"+"-"*10+"\n"
    return result

def unTextedList(classnames):
    cookies={}
    current_datetime=datetime.datetime.now().strftime("%Y-%m-%d")
    Session=requests.session()
    
    headers = {"Host": "sso.lixin.edu.cn",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"Pragma": "no-cache",
"Cache-Control": "no-cache"}
    data={"username":"20170036","password":"290027"}
    params={"client_id":"ufsso_mry_linshi","redirect_uri":"http://mcenter.lixin.edu.cn/callback2.jsp"}
    r=Session.get("https://sso.lixin.edu.cn/authorize.php",params=params,headers=headers,verify=False)
    cookies['PHPSESSID']=(dict(r.cookies))['PHPSESSID']
    
    r=Session.post("https://sso.lixin.edu.cn/authorize.php?client_id=ufsso_mry_linshi&response_type=code&redirect_uri=http%3A%2F%2Fmcenter.lixin.edu.cn%2Fcallback2.jsp",allow_redirects=False,headers=headers,data=data,verify=False)
    url=(r.headers)['Location']
    code=url.replace("http://mcenter.lixin.edu.cn/callback2.jsp?code=","")
    r=Session.get(url,headers=headers,verify=False)
    cookies['JSESSIONID']=(dict(r.cookies))['JSESSIONID']
    
    headers = {"Host": "mcenter.lixin.edu.cn",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
"Referer":"http://mcenter.lixin.edu.cn/callback2.jsp?code=%s"%code
}
    r=Session.post("http://mcenter.lixin.edu.cn/r/jd?cmd=com.awspaas.user.apps.datamanager_getLiXinUser&code=%s"%code,headers=headers,verify=False)
    # print(r.json())

    r=Session.get("http://mcenter.lixin.edu.cn/r/or?cmd=com.awspaas.user.apps.datamanager_enter&appId=com.awspaas.user.apps.onlineoffice&html=vsindex.html&oauthName=soapceshi&uid=20170036",headers=headers,verify=False)
    sid=dict(r.headers)
    sid=sid['Set-Cookie'].replace("AWSSESSIONID=","")
    sid=sid.split(";")[0]
    data={"cmd":"com.awspaas.user.apps.datamanager_enter",
    "uid":"20170036",
    "oauthName"	:"soapceshi",
    "appId":"com.awspaas.user.apps.onlineoffice",
    "html":	"vsindex.html",
    "sid":sid}
    # r=Session.post("http://mcenter.lixin.edu.cn/r/or",data=data,headers=headers)
    # r=Session.post("http://mcenter.lixin.edu.cn/r/jd",headers=headers,verify=False)
    # print(r.text)

    
    # data={}
    # data["processGroupId"]="obj_ec4bd8e555f6430c9d406cbd7349fa6b"
    # data["dwViewId"]="obj_a34321d51a4247a3a85eb99cac1f7f65"
    # data['sid']=sid
    # data['cmd']='CLIENT_DW_PORTAL'
    # data['processGroupName']='每日一报'
    # data['hideTitle']='true'
    # r=Session.get("http://mcenter.lixin.edu.cn/r/w",params=data,headers=headers)
    # # print(r.text)
    data={}
    
    # current_datetime="2020-02-04"
    # compiler=re.compile("cmd=CLIENT_DW_PORTAL&processGroupId=(.*?)&appId=com.awspaas.user.apps.dailyreport&dwViewId=(.*?)&hideTitle=true")
    # content=compiler.search(r.text)
    # data["processGroupId"]=content.group(1)
    # data["dwViewId"]=content.group(2)
    # data['sid']=sid
    # data['cmd']='CLIENT_DW_PORTAL'
    # data['appId']="com.awspaas.user.apps.dailyreport"
    # data['hideTitle']="true"
    # r=Session.get("http://mcenter.lixin.edu.cn/r/w",params=data)
    # compiler=re.compile("'Type':'DATE','Compare':'=','Field':'(.*?)','FieldName':'报送日期','ConditionValue'")
    # content=compiler.search(r.text)
    # Field=content.group(1)
    
    Field="BSRQOBJ_A0D4AF89DB3A45009E5B7BC2C02DDCCD"
    # print(sid)
    data={
    "cmd":"CLIENT_DW_DATA_GRIDJSON",
    "sid":sid,
    "appId":"com.awspaas.user.apps.dailyreport",
    "pageNow":"1",
    "dwViewId":"obj_8a7c291ac65241559257603877fa5d63",
    "processGroupId":"obj_f1d4842f8d0d4748b0853e47302a8b7e",
    "processGroupName":"核查明细名单：测试",
    "limit":"0"}
    
    headers={"X-Requested-With":"XMLHttpRequest",
                "Host": "mcenter.lixin.edu.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
            }

    ts=[]
    for classname in classnames:            
        t=MyThread(func=foo,args=(classname,Session,headers,data,Field,current_datetime))
        ts.append(t)
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    result=""
    for t in ts:
        result+=t.get_result()
    
    return result
            
    # print(r.text)
if __name__=="__main__":
    print(unTextedList(["2016级审计学（注册会计师方向）1班","2016级审计学（注册会计师方向）2班","2016级会计学9班","2016级会计学7班","2016级会计学8班","2016级会计学A班"]))
    # unTextedList(["2016级审计学（注册会计师方向）1班","2016级审计学（注册会计师方向）2班","2016级会计学9班","2016级会计学7班","2016级会计学8班","2016级会计学A班"])
