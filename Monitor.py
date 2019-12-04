from FortiOSAPI import FClient
import time
Forti = FClient()

#定义设备的管理ip和账号密码
host = "101.76.160.89"
username = "api"
password = "api"

login = Forti.login(host=host, username=username, password=password)

########读取配置############
start = time.time() #计时
get_session = Forti.get_session(vdom="VD1",count=10)
#get_interface = Forti.get_inteface_status()
#get_userange = Forti.get_system_userange()
#get_policy_statistics = Forti.get_policy_statistics(vdom="Suning-Test")
end = time.time() #计时
TotalTime = end - start #计算读取使用的时间
#打印出读取使用的时间
print("一共用了"+str(round(TotalTime,2))+"秒")
#
#读取的结果写入到文件中
session = get_session.text
f = open("D:session.txt","w")
f.write(session)
f.close()
########读取配置############



#get = Forti.get_traffic_shaper(vdom="root")
#print get.text

#addint=Forti.add_int(name="nat-gateway", vlanid=10, type="vlan", interface="port5", vdom="root")


Forti.logout()