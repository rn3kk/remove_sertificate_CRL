import subprocess
import sys
import time
from queue import Queue, Empty
from threading import Thread

END_FIND_CRL = 'CertUtil: -store — команда успешно выполнена'
HASH_STR = 'Хеш(sha1) списка отзыва сертификатов (CRL): '
HASH_STR_LENGTH = len(HASH_STR)

hash_list=[]

def enqueueOutput(out):
    for line in iter(out.readline, b''):
        if line.find(END_FIND_CRL) == 0:
            break
        if line.find(HASH_STR) == 0:
            h = line[HASH_STR_LENGTH:]
            h = h.replace('\n', '')
            hash_list.append(h)
    out.close()

def deleteCert(cert_id):
    p = subprocess.Popen(["certutil", "-user", "-delstore", "CA", cert_id], shell=True, stdout=sys.stdout, text=True)
    p.communicate(timeout=1000)


ps = subprocess.Popen(["certutil", "-user", "-store", "CA"], shell=True, stdout=subprocess.PIPE, text=True)

ps_thread = Thread(target=enqueueOutput, args=(ps.stdout,))
ps_thread.start()
ps_thread.join()


for i in hash_list:
    deleteCert(i)
    print("Deleted", i)

print("Questions to mail rn3kk@mail.ru")


