import re
from os import listdir, path, remove, rename
from argparse import ArgumentParser
from time import time

class ArgInitializer(ArgumentParser):

    # Constructor for ArgInitializer
    def __init__(self):
        super(ArgInitializer, self).__init__()
        self._add_options()
    
    '''
        Read the command line argument and store it in the attributes of ArgInitializer Class
    '''
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
        self.add_argument('-rcz','--readChunkSz',type=int,
                help='Multiple of 1024 Bytes while reading the data(Helpful in LazyRead of large data)')

'''
EOLConverter class is used as an object to enable the conversion of line endings in a file

Parameters:
    file - Target File path relative/absolute including the Filename
    eol - The desired line-ending to which the file needs to be converted to
    rcz - To enable efficient reading of large files we need to specify this
          This would help the program execute the reading of contents of file in
          lazy manner(type:int)
          For ex: if rcz is given as 10, then 10 kb data will be read in a single go
'''
class EOLConverter(object):

    # Constructor for EOLConverter class
    def __init__(self, arg_init):
        # BugFix in regex matching
        self.MATCH_REGEX = b'(\n)' if arg_init.eol == 'CRLF' else b'(\r\n)'
        self.REPLACE_REG = b'\r\n' if arg_init.eol == 'CRLF' else b'\n'
        self.rcz = 1024*(arg_init.readChunkSz if arg_init.readChunkSz else 4)
        self.file = arg_init.file
        self.eol = arg_init.eol
        self._ext = path.splitext(self.file)[1][1:].strip()
        self._should_write = True
    
    '''
        Generator for lazy read of large files
    '''
    def lazy_read(self, fileObj, chunkSize=4096):
        while True:
            data = fileObj.read(chunkSize)
            if not data:
                break
            yield data
    
    '''
        Get folder name of the pseudo target-file
    '''
    def _get_pseud_conv_fDet(self):
        ex_fnm = self.file.split(path.sep)[-1]
        f_nm = ex_fnm.split('.')[0]
        return self._get_folder_name(), f_nm + '_conv.'+self._ext
    '''
        Reads the existing content from the target file    
    '''
    def read_file(self):
        st = time()
        fo_nm, cf_nm = self._get_pseud_conv_fDet()
        mreg, rpreg = self.MATCH_REGEX, self.REPLACE_REG
        with open(path.abspath(self.file), 'rb') as _file:
            with open(path.join(fo_nm, cf_nm),'wb') as _wf:
                for line in self.lazy_read(_file,chunkSize=self.rcz):
                    wline = []
                    # Changing the flag to Multiline
                    if re.search(mreg, line, re.M):
                        wline.append(re.sub(mreg, rpreg, line, 0,  re.M))
                        _wf.write(b''.join(wline))
                    else:
                        print('The file with name {file} has desired EOL {eol}'.format(
                            file=self.file,
                            eol =self.eol
                        ))
                        self._should_write = False
                        break
        # Pseudo File deletion when file is already in desired EOL
        if not self._should_write:
            conv_abs_path = path.abspath(path.join(fo_nm, cf_nm))
            remove(conv_abs_path)
        end = time()
        print('Execution Time For Reading & Writing in new File %.8f' % (end - st))
    
    '''
        Gets the folder name of the target file
    '''
    def _get_folder_name(self):
        return self.file.split(path.sep)[-2]

    '''
        Writes to the original file
    '''
    def write_file(self):
        if self._should_write:
            st = time()
            # Delete the original file
            remove(self.file)
            fo_nm, cf_nm = self._get_pseud_conv_fDet()
            abs_fpath = path.abspath(path.join(fo_nm, cf_nm))
            # Rename the converted file 
            rename(abs_fpath, path.abspath(self.file))
            end = time()
            print('Execution Time in Writing the Read File in the earlier Read File %.8f' % (end - st))
    
    '''
        Converts to the desired EOL for the target-file
    '''
    def convert_EOL(self):
        self.read_file()
        self.write_file()



if __name__ == "__main__":
    parser = ArgInitializer()
    cmd_args = parser.parse_args()
    converter = EOLConverter(cmd_args)
    converter.convert_EOL()