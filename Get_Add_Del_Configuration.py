from FortiOSAPI import FClient
import time
Forti = FClient()

#定义设备的管理ip和账号密码
host = "your_fortigate_management_ip"
username = "api"
password = "api"

login = Forti.login(host=host, username=username, password=password)



#从txt文本从读取external ip和mapped ip，并分别给到不同的变量，默认是列表
with open ("D:vipex.txt",'r') as f:
    vipex = f.read().splitlines()
with open ("D:vipmap.txt","r") as f1:
    vipmap = f1.read().splitlines()
    
start = time.time() #计时
#在add_vip函数的参数中使用变量，并从上面生成的列表中取值，然后通过for循环执行add_vip即可实现匹配生成配置
for i in range(0,5000):
    Forti.add_vip(vdom="root", name="test"+str(i), extip=vipex[i], extintf="any", mappedip=vipmap[i])

end = time.time() #计时
TotalTime = end - start #计算读取使用的时间
print("一共用了"+str(round(TotalTime,2))+"秒")
#同样循环name参数即可批量删除配置
start = time.time() #计时
for i in range(5000):
    Forti.del_vip(vdom="root", name="test"+str(i))
end = time.time() #计时
TotalTime = end - start #计算读取使用的时间
print("一共用了"+str(round(TotalTime,2))+"秒")


# start = time.time() #计时
#
# get_route_static = Forti.get_route_static(vdom="VD1") #读取静态路由
# # get_addr = Forti.get_address(vdom="Suning-Test") #读取firewall address
# # get_addrgrp = Forti.get_address_group(vdom="Suning-Test") #读取address group
# # get_service = Forti.get_service(vdom="Suning-Test") #读取service
# # get_servicergrp = Forti.get_service_group(vdom="Suning-Test") #读取service group
#
# end = time.time() #计时
# TotalTime = end - start #计算读取使用的时间
#
# #打印出读取使用的时间
# print(TotalTime)
#
# #读取的结果写入到文件中
# route = get_route_static.text
# f = open("D:routeVD1.txt","w")
# f.write(route)
# f.close()



# add = Forti.add_vip(vdom="root", name="test", extip="211.10.10.100", extintf="any", mappedip="192.168.10.100")
# vip = add.text
# print(vip)

#get = Forti.get_traffic_shaper(vdom="root")
#print get.text

#addint=Forti.add_int(name="nat-gateway", vlanid=10, type="vlan", interface="port5", vdom="root")


Forti.logout()
