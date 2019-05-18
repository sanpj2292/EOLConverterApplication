# EOLConverterApplication
This windows console based app can convert EOL for a file from LF to CRLF &amp; vice-versa

## How to Use it ?
1) Open your console & type the command in the following way:
```bash
#!usr/bin/bash
python eol_converter_app.py -f mypath/to/file.some_ext -e CRLF -rcz 5 -wcz 6
```
-f --> filepath
-e --> Desired Line Ending
-rcz --> Read chunk size(In multiples of 1024 B)
-wcz --> Write Chunk Size(In multiples of 1024 B)

###### Special Feature
Handles large files in an efficient and quick manner by making use of lazy-read & write

##### Output for large files
.proto file 282701 KB -> 1.23 sec with 8kb read-chunk with 4kb write-chunk
.proto file 282701 KB -> 7.37 sec with 2kb read-chunk with 4kb write-chunk
.proto file 282701 KB -> 4.07 sec with 4kb read-chunk with 4kb write-chunk
