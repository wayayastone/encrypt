# -*- coding: utf-8 -*-
import sys
import pyDes
from pyDes import *
import binascii

#凯撒加密
def Caesar(text, x):
    x = int(x)
    encode = ''
    for ch in text:
        encode = encode + chr((ord(ch) - ord('a') + x) % 26 + ord('a'))
    print(('右移'+str(x)+'位，Caesar密文为：'+encode).decode('utf-8'))
#凯撒解密
def DeCaesar(text):
    i = 1
    decode = ''
    file = open(text[0:3] + '.txt', 'w+')
    while i < 26:
        decode = ''
        for ch in text:
            decode = decode + chr((ord(ch) - ord('a') - i + 26) % 26 + ord('a'))
        file.write(decode + '\n')
        i = i + 1
    file.close()
    print(('解密数据已写入文件' + text[0:3] + '.txt').decode('utf-8'))

#Virginia加密
def Virginia(text, x):
   
    if len(text) != len(x):
        print(('Error! Message:明文密钥长度不匹配').decode('utf-8'))
    encode = ''
    i = 0
    while i < len(text):
        encode = encode + chr((ord(x[i]) - ord('a') + ord(text[i]) - ord('a')) % 26 + ord('a'))
        i = i + 1
    print(('密钥：' + x + ', Virginia密文为：' + encode ).decode('utf-8'))

#Virginia解密
def DeVirginia(text, x):
    if len(text) != len(x):
        print(('Error! Message:密文密钥长度不匹配').decode('utf-8'))
    code = ''
    i = 0
    while i < len(text):
        code = code + chr((ord(text[i]) - ord(x[i]) + 52) % 26 + ord('a'))
        i = i + 1
    print(('密钥：' + x + ', Virginia明文为：' + code ).decode('utf-8'))


#DES加密，使用BCB模式
def DES(text, x):
    data = text

    #参数依次为，密钥，模式，iv，pad，pad模式
    k = pyDes.des(x, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    
    d = k.encrypt(data)
    print(('密钥为：' + x + '，DES（CBC）密文为：' + binascii.hexlify(d)).decode('utf-8'))

#DES解密
def DeDES(text, x):
    
    d = binascii.unhexlify(text)
    k = pyDes.des(x, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    encode = k.decrypt(d)
    print(('密钥为：' + x + '，DES（CBC）明文为：' + encode).decode('utf-8'))

#加密模块，统一加密入口
#参数分别为，待加密字符串，是否加密，加密方式，密钥和待加密字符串所在文件

def encrypt(text, isencypt, fun, x, filename):
    
    if filename != '':  #若待加密字符串为空，则从文件中获取
        with open(filename, 'r') as f:
            text = f.readline().strip()
    if fun == '0' and isencypt:
        Caesar(text, x)
    elif fun == '0' and isencypt == False:
        DeCaesar(text)
    elif fun == '1' and isencypt:
        Virginia(text, x)
    elif fun == '1' and isencypt == False:
        DeVirginia(text, x)
    elif fun == '2' and isencypt:
        DES(text, x)
    elif fun == '2' and isencypt == False:
        DeDES(text, x)

#交互模式
def mutual():
    
    fun = ''
    text = ''
    is_encrypt = True
    x = ''
    print("<========================MyEncrypt==============================>")
    print("<===============================================================>")
    print("<=========================Welcome!==============================>")
    print("<===============================================================>")
    print("<========================Now Begin!=============================>")
    print("<===============================================================>")
    print("_____________________________说明_________________________________".decode('utf-8'))
    print("____此程序由来自NUIST的学生姜斐和张向阳共同完成，实现了凯撒加密，维吉尼".decode('utf-8'))
    print("亚加密和DES加密功能及其对应的解密功能。完成时间2018年5月14日。".decode('utf-8'))
    print("____本软件有命令行和交互模式两种测试方式，命令行模式提供文件的读入，具体".decode('utf-8'))
    print("操作请在命令行模式下使用‘-h’参数查看。键入‘quit’或者‘bye’可退出交互。".decode('utf-8'))
    while True:
        fun = ''
        text = ''
        is_encrypt = True
        x = ''

        #等待输入加解密方式，三种分别对应0，1，2
        while True:
            
            fun = raw_input("请输入加解密方式（Caesar:0; Virginia:1; DES:2）:".decode('utf-8').encode('gbk'))
            if fun == '0' or fun == '1' or fun == '2':
                break
            if fun == 'bye' or fun == 'quit':
                return

        #等待选择加密或者解密，分别对应0，1
        while True:    
            str_temp = raw_input("请选择加密或者解密：（加密:0; 解密:1）".decode('utf-8').encode('gbk'))
            if str_temp == '0':
                is_encrypt = True
                break
            elif str_temp == '1':
                is_encrypt = False
                break
            if str_temp == 'bye' or fun == 'quit':
                return

        #等待输入加解密字符串
        while True:
            text = raw_input("请输入待加解密字符串：".decode('utf-8').encode('gbk'))
            if text is not None:
                break
            if text == 'bye' or fun == 'quit':
                return
        
        #等待输入加解密所需密钥
        while True:
            x = raw_input("请输入密钥：".decode('utf-8').encode('gbk'))
            if x is not None:
                break
            if x == 'bye' or fun == 'quit':
                return
        
        #交互模式不支持文件读取，置空
        filename = ''
        encrypt(text, is_encrypt, fun, x, filename)  

#main方法
def main():
    i = 1#用作外部参数下标
    comm_list = sys.argv#获取外部参数列表
    fun = '0'   #表示加解密方式
    text = ''   #存放待加解密字符串
    is_encrypt = True   #标识是否加密或解密，true为加密，false为解密
    x = '3'     #存放密钥，此处3为凯撒加密的位移量，也可存放其他两种加密方式的密钥
    filename = ''   #指定从文件读取时的文件名

    #交互模式
    if len(comm_list) == 1:
        mutual()
    
    #命令行模式
    else:
        while i < len(comm_list):
            

            if comm_list[i] == '-e':    #加密，后面跟字符串
                is_encrypt = True
                text = comm_list[i+1]
            elif comm_list[i] == '-x':  #用于指定密钥，后跟字符串
                x = comm_list[i+1]
            elif comm_list[i] == '-d':  #解密，后跟字符串
                is_encrypt = False
                text = comm_list[i+1]
            elif comm_list[i] == '-t':  #用于指定加解密方式，后跟数字
                fun = comm_list[i+1]
            elif comm_list[i] == '-ef': #加密，从文件中读取待操作字符串，后跟文件路径
                is_encrypt = True
                filename = comm_list[i+1]
            elif comm_list[i] == '-df': #解密，从文件中读取待操作字符串，后跟文件路径
                is_encrypt = False
                filename = comm_list[i+1]
            elif comm_list[i] == '-h':  #帮助
                if i == len(comm_list) - 1:
                    print('语法：myencrypt.py -[edh] parameter [-t] type'.decode('utf-8'))
                    print('\t-e\t对一串字符进行加密，参数为需要加密的字符'.decode('utf-8'))
                    print('\t-d\t对一串字符进行解密，参数为需要解密的字符'.decode('utf-8'))
                    print('\t-t\t指定加、解密所使用的方式'.decode('utf-8'))
                    print('\t\t0\t凯撒加密'.decode('utf-8'))
                    print('\t\t1\t维吉尼亚加密'.decode('utf-8'))
                    print('\t\t2\tDES加密'.decode('utf-8'))
                    print('\t-h\t获取帮助'.decode('utf-8'))
                return
            i = i + 2
        #从命令行获取参数后，进入加密模块
        encrypt(text, is_encrypt, fun, x, filename)

    

if __name__ == '__main__':
    main()