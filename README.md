# EOLConverterApplication
This windows console based app can convert EOL for a file from LF to CRLF &amp; vice-versa

## How to Use it ?
1) Open your console & type the command in the following way:
```bash
#!usr/bin/bash
python eol_converter_app.py -f mypath/to/file.some_ext -e CRLF -rcz 5
```
-f --> filepath

-e --> Desired Line Ending

-rcz --> Read chunk size(In multiples of 1024 B)

## Special Feature
Handles large files in an efficient and quick manner by making use of lazy-read & write

##### Output for large files

.proto file 327753 KB -> 6.55064 sec with 8kb read-chunk while converting to LF

.proto file 327753 KB -> 6.44263 sec with 8kb read-chunk while converting to CRLF

.proto file 327753 KB -> 6.10634 sec with 16kb read-chunk while converting to LF

.proto file 327753 KB -> 6.10655 sec with 8kb read-chunk while converting to CRLF