# libyaz0 v0.2
A library for compressing/decompressing Yaz0/1 compression formats.

By MasterVermilli0n / AboodXD.  
Decompression algorithm based on wszst's.  
Special thanks to RoadrunnerWMC for helping with looking up matches for the compression algorithm.

## `main.py` usage:

 * `main [option...] input`

### Options:
 * `-o <output>`: Output file, if not specified, the output file will have the same name as the intput file
 * `-c`: Compress (Will try to decompress if not specified)

### Compression options:
 * `-level <level>`: compression level (1-9) (1 is the default)  
0: No compression (Fastest)  
9: Best compression (Slowest)

 * `-unk <unk>`: the unknown value that will be located at 0x8-0xC (0x00000000 is the default)