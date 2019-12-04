from FortiOSAPI import FClient
import time
Forti = FClient()

#定义设备的管理ip和账号密码
host = "192.168.4.29"
username = "api"
password = "api"

login = Forti.login(host=host, username=username, password=password)

with open ("D:addr.txt", 'r') as f:
    addr = f.read().splitlines()

start = time.time() #计时
for i in range(2):
    addAddr = Forti.add_address(vdom="root", name="addr"+str(i), subnet=addr[i])
    #delAddr = Forti.del_address(vdom="Suning-Test", name="addr"+str(i))
    addpolicy = Forti.add_firewall_policy(vdom="root", name="p"+str(i), srcaddr=addr[i], action="accept")

end = time.time() #计时
TotalTime = end - start #计算读取使用的时间
print("一共用了"+str(round(TotalTime,2))+"秒")
# a = addAddr.text
# p = addpolicy.text
# print(a)
# print(p)



########增加VIP############
#从txt文本从读取external ip和mapped ip，并分别给到不同的变量，默认是列表
# with open ("D:vipex.txt",'r') as f:
#     vipex = f.read().splitlines()
# with open ("D:vipmap.txt","r") as f1:
#     vipmap = f1.read().splitlines()
# # print(vipex)
# # print(vipmap)
# start = time.time() #计时
# #在add_vip函数的参数中使用变量，并从上面生成的列表中取值，然后通过for循环执行add_vip即可实现匹配生成配置
# for i in range(0,5000):
#     Forti.add_vip(vdom="Suning-Test", name="test"+str(i), extip=vipex[i], extintf="any", mappedip=vipmap[i])
#
# end = time.time() #计时
# TotalTime = end - start #计算读取使用的时间
# print("一共用了"+str(round(TotalTime,2))+"秒")
########增加VIP############

########删除VIP############
# start = time.time() #计时
# for i in range(5000):
#     Forti.del_vip(vdom="Suning-Test", name="test"+str(i))
# end = time.time() #计时
# TotalTime = end - start #计算读取使用的时间
# print("一共用了"+str(round(TotalTime,2))+"秒")
########删除VIP############


########读取配置############
# start = time.time() #计时
# get_policy = Forti.get_firewall_policy(vdom="Suning-Test")
# get_route_static = Forti.get_route_static(vdom="Suning-Test") #读取静态路由
# get_addr = Forti.get_address(vdom="Suning-Test") #读取firewall address
# # get_addrgrp = Forti.get_address_group(vdom="Suning-Test") #读取address group
# get_service = Forti.get_service(vdom="Suning-Test") #读取service
# get_servicergrp = Forti.get_service_group(vdom="Suning-Test") #读取service group
# #
# end = time.time() #计时
# TotalTime = end - start #计算读取使用的时间

#打印出读取使用的时间
# print(TotalTime)
#
#读取的结果写入到文件中
# policy = get_policy.text
# f = open("D:policy.txt","w")
# f.write(policy)
# f.close()
########读取配置############



#get = Forti.get_traffic_shaper(vdom="root")
#print get.text

#addint=Forti.add_int(name="nat-gateway", vlanid=10, type="vlan", interface="port5", vdom="root")


Forti.logout()