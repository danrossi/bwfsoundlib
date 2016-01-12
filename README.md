bwfsoundlib
===========

bwfsoundlib is an extension of `PySoundFile <https://github.com/bastibe/PySoundFile>`__ using the C library `libsndfile <http://www.mega-nerd.com/libsndfile/>`__ to implement broadcast wave bext chunk and iXML chunk parsing.

This requires new functions in libsndfile 1.0.26 to implement reading chunks in wav files. 1.0.26 is not currently available as binaries and requires compiling.

| (Copyright (c) 2016 Daniel Rossi Electroteque Media <electroteque@gmail.com>

Installation
------------

Please follow the guide on `PySoundFile <https://github.com/bastibe/PySoundFile>`__ for Python building and dependancies.

`libsndfile <http://www.mega-nerd.com/libsndfile/>`__ can be downloaded with compiling instructions.

`libsndfile binaries <https://github.com/bastibe/libsndfile-binaries>`__ for OSX and Windows may be updated in the future for libsndfile version 1.0.26.