import re
from os import listdir, path
from argparse import ArgumentParser
from time import time

class ArgInitializer(ArgumentParser):

    def __init__(self):
        super(ArgInitializer, self).__init__()
        self._add_options()

    def _add_options(self):
        self.add_help = True
        self.description = 'EOL Converter Application'
        group = self.add_mutually_exclusive_group()
        group.add_argument('-d','--dir',type=str,
                help='Folder Path where the conversion needs to take place')
        group.add_argument('-f','--file',type=str,
                help='File Path where the conversion needs to take place')
        self.add_argument('-e','--eol',type=str,required=True
                ,help='End of line for files in folder / single file')
        self.add_argument('-rcsz','--readChunkSz',type=int,
                help='Multiple of 1024 Bytes while reading the data(Helpful in LazyRead of large data)')
        self.add_argument('-wcsz','--writeChunkSz',type=int,
                help='Multiple of 1024 Bytes while writing the data(Helpful in LazyRead of large data)')




class EOLConverter(object):

    def __init__(self, arg_init):
        self.MATCH_REGEX = b'(?<!\r)\n|\r(?!\n)' if arg_init.eol == 'CRLF' else b'(?<=\r)\n|\r(?=\n)'
        self.REPLACE_REG = b'\r\n' if arg_init.eol == 'CRLF' else b'\n'
        self.wcz = 1024*(arg_init.writeChunkSz if arg_init.writeChunkSz else 16)
        self.rcz = 1024*(arg_init.writeChunkSz if arg_init.readChunkSz else 4)
        self.file = arg_init.file
        self.eol = arg_init.eol
        self._ext = path.splitext(self.file)[1][1:].strip()
    
    def readInChunks(self, fileObj, chunkSize=4096):
        """
        Lazy function to read a file piece by piece.
        Default chunk size: 4kB.
        """
        while True:
            data = fileObj.read(chunkSize)
            if not data:
                break
            yield data

    def read_file(self):
        st = time()
        mreg, rpreg = self.MATCH_REGEX, self.REPLACE_REG
        with open(path.abspath(self.file), 'rb') as _file:
            with open('converted.'+self._ext,'wb') as _wf:
                for line in self.readInChunks(_file,chunkSize=self.rcz):
                    wline = []
                    wline.append(re.sub(mreg, rpreg, line, 0, re.DOTALL))
                    print(wline)
                    _wf.write(b''.join(wline))
        end = time()
        print('Execution Time For Reading & Writing in new File %.8f' % (end - st))

    def write_file(self):
        st = time()
        with open('converted.'+self._ext,'rb') as _rf:
            with open(path.abspath(self.file), 'wb') as _wf:
                for line in self.readInChunks(_rf, chunkSize=self.wcz):
                    _wf.write(line)
            _rf.flush()

        end = time()
        print('Execution Time in Writing the Read File in the earlier Read File %.8f' % (end - st))

    def convert_EOL(self):
        self.read_file()
        self.write_file()



if __name__ == "__main__":
    parser = ArgInitializer()
    cmd_args = parser.parse_args()
    converter = EOLConverter(cmd_args)
    converter.convert_EOL()