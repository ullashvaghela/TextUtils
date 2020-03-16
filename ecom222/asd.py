# import re, uuid
# # after each 2 digits, join elements of getnode().
# # using regex expression
# print ("The MAC address in expressed in formatted and less complex way : ")
# print (':'.join(re.findall('..', '%012x' % uuid.getnode())))
#==================================================
# import subprocess as sub
# import re

# def findWholeWord(w):
#     return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
# p = sub.Popen(('sudo', 'tcpdump', '-l', '-s 0', '-vvv', '-n', '((udp port 67) and (udp[8:1] = 0x1))'), stdout=sub.PIPE)
# for row in iter(p.stdout.readline, b''):
#     if findWholeWord('requested-ip')(row):
#         print(row.split(' ')[-1])
#     elif findWholeWord('client-id')(row):
#         print(row.split(' ')[-1])