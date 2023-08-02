from django.shortcuts import render
from django.http import HttpResponse
from Crypto.Cipher import AES
import json
import pymysql
import requests
import time
import random
import urllib3
from wordcloud import WordCloud
#import matplotlib.pyplot as plt
# Create your views here.

var link=""
var convid=""
def index(request):
    link=request.path
    convid=link.split('?')[1]
    return HttpResponse(convid)

cyp_key = bytes([0x82, 0xC8, 0xA9, 0xC3, 0xD2, 0xE1, 0xF0, 0x3F, 0x28, 0x2d, 0x3c, 0x4b, 0x5a, 0x69, 0x78, 0x87])
aad = bytes([0x38, 0xA6, 0xB7, 0x08, 0xC9, 0xDA, 0x91, 0x82, 0x73, 0x64, 0x5B, 0x4C, 0x3D, 0x2E])
nonce = bytes([0xF6, 0xE7, 0xD8, 0xC9, 0xB1, 0xA2, 0x93, 0x84, 0x75,  0x6A, 0x5B, 0x5C])  # 기본 12(96bit)byte이며 길이 변경 가능.

def binary_to_dict(the_binary):
    #jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    jsn = the_binary.decode("utf-8")
    d = json.loads(jsn)
    return d

def dec(key, aad, nonce, cipher_data, mac):
    #print('\nenter dec function ---------------------------------')
    # 암호화 라이브러리 생성
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    # aad(Associated Data) 추가
    cipher.update(aad)

    try:
        # 복호화!!!
        plain_data = cipher.decrypt_and_verify(cipher_data, mac)
        # 암호화된 데이터 출력
        #print_hex_bytes('plain_data', plain_data)
        #print('exit dec function ---------------------------------')
        # 복호화 된 값 리턴
        return plain_data

    except ValueError:
        # MAC Tag가 틀리다면, 즉, 훼손된 데이터
        print ("Key incorrect")
        print('exit dec function ---------------------------------')
        # 복호화 실패
        return None


def get_gs_cmk(host,port,user,passwd,db,id):
    conn=pymysql.connect(host='113.198.137.208',user='root',password='root',db='root', port=30001)
    cur=conn.cursor()
    cur.execute('select gs_cmk from interviews_interviews where id=%s;',(id))
    res=cur.fetchall()
    conn.commit()
    mackey=res[0][0]
    return mackey

def get_faj(host,port,user,passwd,db,id):
    conn=pymysql.connect(host='113.198.137.208',user='root',password='root',db='root', port=30001)
    cur=conn.cursor()
    cur.execute('select content_div from interviews_interviews where id=%s;',(id))
    res=cur.fetchall()
    conn.commit()
    content_div=res[0][0]
    return content_div



def get_data(content_div,mackey):
    content_div=content_div[28:]
    content_div='/root/django-main'+content_div
    with open(content_div,'rb') as file:
        rdata=file.read()
        data=dec(cyp_key,aad,nonce,rdata,mackey)
    sent_data=binary_to_dict(data)

    payload=dict()
    text=""
    for i in sent_data:
      text+=i['sentence']
      text+='\n'

    payload["text"]=text
    print(payload)

    with open('/root/project/nginx/html/wdx/payload.txt','w') as file:
      json.dump(payload,file)

mackey=get_gs_cmk('113.198.137.208',30001,'root','root','root',convid)
content_div=get_faj('113.198.137.208',30001,'root','root','root',convid)
get_data(content_div,mackey)

http=urllib3.PoolManager()
response=http.request(
  "POST",
   "http://113.198.137.208:30000/wdx/index.php"
)
print(response.status)

with open('/root/project/nginx/html/wdx/result.txt','r') as res:
  r=json.load(res)
  r=r['word_index']
  wc=WordCloud(random_state=123, font_path="/usr/share/fonts/nanum/NanumMyeongjoExtraBold.ttf",width=400, height=400, background_color='white')
  gen=wc.generate_from_frequencies(r)
  gen.to_file('/root/project/nginx/html/wdx/wc.jpg')
