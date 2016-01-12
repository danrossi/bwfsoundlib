bwfsoundlib
===========

bwfsoundlib is an extension of [PySoundFile](https://github.com/bastibe/PySoundFile)  using the C library [libsndfile](http://www.mega-nerd.com/libsndfile/) to implement broadcast wave bext chunk and iXML chunk parsing.

This requires new functions in libsndfile 1.0.26 to implement reading chunks in wav files. 1.0.26 is not currently available as binaries and requires compiling.

> (Copyright (c) 2016 Daniel Rossi Electroteque Media <electroteque@gmail.com>

Installation
------------

Please follow the guide on [PySoundFile](https://github.com/bastibe/PySoundFile) for Python building and dependancies.

[libsndfile](http://www.mega-nerd.com/libsndfile/) can be downloaded with compiling instructions.

[libsndfile binaries](https://github.com/bastibe/libsndfile-binaries) for OSX and Windows may be updated in the future for libsndfile version 1.0.26.

Example
-------

```
file = BwfSoundFile("/path/to/file.wav", "r")
file.read_metadata()

print (file.ixml_info)
print (file.bext_info)
print (file.get_core_info())
```