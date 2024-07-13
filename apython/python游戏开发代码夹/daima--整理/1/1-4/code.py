letter_list='ABCDEFGHIJKLMNOPQRSTUVWXYZ';

#加密函数
def Encrypt(plaintext,key):
    ciphertext='';
    for ch in plaintext:  #遍历明文
        if ch.isalpha():
            #明文是否为字母，如果是，判断大小写，分别进行加密
            if ch.isupper():
                ciphertext+=letter_list[(ord(ch)-65+key) % 26]
            else:
                ciphertext+=letter_list[(ord(ch)-97+key) % 26].lower()
        else:
            #如果不为字母，直接添加到密文字符里
            ciphertext+=ch
    return ciphertext

#解密函数
def Decrypt(ciphertext,key):
    plaintext='';
    for ch in ciphertext:
        if ch.isalpha():
            if ch.isupper():
                plaintext+=letter_list[(ord(ch)-65-key) % 26]
            else:
                plaintext+=letter_list[(ord(ch)-97-key) % 26].lower()
        else:
            plaintext+=ch
    return plaintext


#Ö÷º¯Êý
user_input=input('加密请按D，解密请按E：');
while(user_input!='D' and user_input!='E'):
    user_input=input('输入有误，请重新输入：')

key=input('请输入密钥：')
while(int(key.isdigit()==0)):
    key=input('输入有误，密钥为数字，请重新输入：')

if user_input =='D':
    plaintext=input('请输入明文：')
    ciphertext=Encrypt(plaintext,int(key))
    print ('密文为：\n%s' % ciphertext )
else:
    ciphertext=input('请输入密文：')
    plaintext=Decrypt(ciphertext,int(key))
    print ( '明文为:\n%s\n' % ciphertext )
