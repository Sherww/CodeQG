# pip install fairseq
# pip install moses
# pip install 
# requires "torch", "regex", "requests", "tqdm", "sacremoses", "subword-nmt", fastBPE
import socket
import torch
from threading import Thread

print("Torch version: " + torch.__version__)

#torch.hub.list('pytorch/fairseq')  # [..., 'transformer.wmt16.en-de', ... ]

print("Starting to load English to German Translation Model:")
en2de = torch.hub.load('pytorch/fairseq:main','transformer.wmt16.en-de', tokenizer='moses', bpe='subword_nmt')
en2de = en2de.cuda()
print(type(en2de)) #transformer.wmt19.en-de	11 gb
# transformer.wmt19.de-en
print("Completed loading English to German Translation Model.\n")
print("Starting to load German to English Translation Model:")
de2en = torch.hub.load('pytorch/fairseq:main', 'transformer.wmt19.de-en.single_model', tokenizer='moses', bpe='fastbpe')
de2en = de2en.cuda()
print("Completed loading German to English Translation Model.\n")

host = '0.0.0.0'        # Symbolic name meaning all available interfaces
port = 12389     # Arbitrary non-privileged port

def process(conn):
    data = (conn.recv(4096 * 4))

    if not data: return
    try:
        en = data.decode().strip()
        en = en.split("\n")
        
        de=en2de.translate(en)
        #print("Translated German     : "+de)
        results = de2en.translate(de)

        for i in range(len(results)):
            print("\nReceived              :"+en[i])
            print("BackTranslated English: "+results[i])

    except UnicodeDecodeError:
        print("Unicode Decode error")
        results="UnicodeDecodeError" # a very high number
    conn.sendall(("\n".join(results) + '\n').encode('utf8'))

g_socket_server = None  # 负责监听的socket
 
g_conn_pool = []  # 连接池

def message_loop(conn):
    while True:
        try:
            process(conn)
        except ConnectionResetError:
            print("Connection Reset Error")
            break
    conn.close()
    g_conn_pool.remove(conn)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
while True:
    conn, addr = s.accept()
    print('Connected by', addr)

    g_conn_pool.append(conn)
    # 给每个客户端创建一个独立的线程进行管理
    thread = Thread(target=message_loop, args=(conn,))
    # 设置成守护线程
    thread.setDaemon(True)
    thread.start()
    

