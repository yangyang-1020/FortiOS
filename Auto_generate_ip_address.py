import time

time_start = time.time()
#参数：number-生成条数；start-开始ip
def get_ip(number='10', start='13.1.1.1'):
    file = open('D:ip_list1.txt', 'w')
    starts = start.split('.')
    A = int(starts[0])
    B = int(starts[1])
    C = int(starts[2])
    D = int(starts[3])
    for A in range(A, 256):
        for B in range(B, 256):
            for C in range(C, 256):
                for D in range(D, 256):
                    ip = "%d.%d.%d.%d" % (A, B, C, D)

                    if number > 1:
                        file.write(ip + '\n')
                        number -= 1
                    elif number == 1:  # 解决最后多一行回车问题
                        file.write(ip)
                        number -= 1
                    else:
                        file.close()
                        print
                        ip
                        return
                D = 0
            C = 0
        B = 0

get_ip(20000, '13.1.1.1')
time_end = time.time()
time = time_end - time_start
print('耗时%s秒' % time)