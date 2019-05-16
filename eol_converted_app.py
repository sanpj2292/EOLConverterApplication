import re
from os import listdir, path
from argparse import ArgumentParser
from time import time

class ArgInitializer(ArgumentParser):

    def __init__(self):
        super(ArgInitializer, self).__init__()

    def addOptions(self):
        self.add_help = True
        self.description = 'EOL Converter Application'
        group = self.add_mutually_exclusive_group()
        group.add_argument('-d','--dir',type=str,
                help='Folder Path where the conversion needs to take place')
        group.add_argument('-f','--file',type=str,
                help='File Path where the conversion needs to take place')
        self.add_argument('-e','--eol',type=str,required=True
                ,help='End of line for files in folder / single file')


def readInChunks(fileObj, chunkSize=4096):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 4kB.
    """
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        yield data

if __name__ == "__main__":
    parser = ArgInitializer()
    parser.addOptions()
    cmd_args = parser.parse_args()
    st = time()
    if cmd_args.file:
        
        with open(path.abspath(cmd_args.file), 'rb') as _file:
            print('Inside It!!')
            for line in readInChunks(_file):
                print(line)
                print(re.sub(b'(?<!\r)\n|\r(?!\n)',b'\r\n',line,0, re.DOTALL))
                # a = re.finditer(b'(?<!\r)\n|\r(?!\n)',line,re.DOTALL)
                # for i in a:
                #     print(i)
                # print(a)
                

                if len(line) > 1 and line[-3] == b'\r\n':
                    print('CRLF')
                elif line[-1] == b'\n':
                    print('LF')
                else:
                    print('None')
        
        end = time()
        print('Execution Time %.8f' % (end - st))