"""bwfsoundlib is an extension of PySoundFile using the C library libsndfile to implement broadcast wave bext chunk and iXML chunk parsing.

This requires new functions in libsndfile 1.0.26 to implement reading chunks in wav files. 1.0.26 is not currently available as binaries and requires compiling.

For further information, see http://pysoundfile.readthedocs.org/ and http://www.mega-nerd.com/libsndfile/.

"""

__version__ = "0.8.1"

from soundfile import SoundFile, _snd, _ffi
from bwfutils import samples_to_time, format_audio_duration

"""The Cffi cdef instructions required for the broadcast wave bext chunk info struct and the chunk info struct."""

_ffi.cdef("""
enum
{
    SFC_SET_BROADCAST_INFO  = 0x10F1,
    SFC_GET_BROADCAST_INFO  = 0x10F0

} ;


typedef struct SF_BROADCAST_INFO
{
                char		description [256];
				char		originator [32] ;
				char		originator_reference [32] ;
				char		origination_date [10] ;
				char		origination_time [8] ;
				uint32_t	time_reference_low ;
				uint32_t	time_reference_high ;
				short		version ;
				char		umid [64] ;
				char		reserved [190] ;
				uint32_t	coding_history_size ;
				char		coding_history [2048] ;
} SF_BROADCAST_INFO ;

struct SF_CHUNK_INFO
{	char		id [64] ;	/* The chunk identifier. */
	unsigned	id_size ;	/* The size of the chunk identifier. */
	unsigned	datalen ;	/* The size of that data. */
	void		*data ;		/* Pointer to the data. */
} ;

typedef struct SF_CHUNK_INFO SF_CHUNK_INFO ;

struct SF_CHUNK_ITERATOR
{	uint32_t	current ;
	int64_t		hash ;
	char		id [64] ;
	unsigned	id_size ;
	SNDFILE		*sndfile ;
} ;

typedef	struct SF_CHUNK_ITERATOR SF_CHUNK_ITERATOR ;

SF_CHUNK_ITERATOR * sf_get_chunk_iterator (SNDFILE *sndfile, const SF_CHUNK_INFO *chunk_info) ;
int sf_get_chunk_size (const SF_CHUNK_ITERATOR * it, SF_CHUNK_INFO * chunk_info) ;
int sf_get_chunk_data (const SF_CHUNK_ITERATOR * it, SF_CHUNK_INFO * chunk_info) ;


""")

class BwfSoundFile(SoundFile):
    def __init__(self, *args, **kwargs):
        super(BwfSoundFile, self).__init__(*args, **kwargs)

        self.ixml_info = None
        self.bext_info = {}

        # create a dict map for the bit depth subtype info
        self.bit_depth_map = {
            "PCM_24": 24,
            "PCM_16": 16,
            "PCM32": 32
        }

    def get_ixml(self):

        """Collects an iXML chunk string if the chunk is available.
        Attempt to get an iterator for an iXML chunk. If the generated chunk length
        is set, attempt to read the iXML chunk data and convert the chunk info pointer to a string.

        """

        # set the chunk info struct
        chunk_info = _ffi.new("SF_CHUNK_INFO*")
        # set the chunk id to obtain
        chunk_info.id = b'iXML'
        chunk_info.id_size = 4;

        # get the chunk iterator
        iterator = _snd.sf_get_chunk_iterator(self._file, chunk_info)

        # get the chunk size to generate the data length
        err = _snd.sf_get_chunk_size(iterator, chunk_info)

        # if the chunk has data read it to a string
        if (chunk_info.datalen > 0):
            # allocate memory to the chunk data
            chunk_data = _ffi.new("char[]", 1024)
            chunk_info.data = chunk_data
            _snd.sf_get_chunk_data(iterator, chunk_info)
            #convert the chunk data pointer to a string
            self.ixml_info = _ffi.buffer(chunk_info.data, chunk_info.datalen)[:].decode()


    def ffi_string(self, value):
        """Format cffi strings."""
        return _ffi.string(value).decode()


    def get_core_info(self):
        """A helper method to attempt to return useful core information from wav files to a dict."""

        return {
            "samplerate": self._info.samplerate,
            "channels": self._info.channels,
            #format the audio duration from the frames and samplerate to a time string
            "duration": format_audio_duration(self._info.frames, self._info.samplerate),
            #"format": self._info.format,
            "bit_depth": self.bit_depth_map[self.subtype],
            #"endian": self.endian,
            #"format_info": self.format_info,
            "bit_depth_info": self.subtype_info
            #"sections": self._info.sections,
            #"extra_info": self.extra_info
        }

    def get_bext(self):
        """Retrieve the broadcast wave bext chunk metadata from a libsndfile command and return the converted data to a dict."""
        info = _ffi.new("SF_BROADCAST_INFO*")
        _snd.sf_command(self._file, _snd.SFC_GET_BROADCAST_INFO,
                        info, 1024)

        #return the broadcast wave metadata to a dict after formatting ffi bytes to strings, formatted seconds from midnight to time string
        self.bext_info = {
            "description": self.ffi_string(info.description),
            "originator": self.ffi_string(info.originator),
            "originator_reference": self.ffi_string(info.originator_reference),
            "origination_date":  self.ffi_string(info.origination_date),
            "origination_time":  self.ffi_string(info.origination_time),
            "timereference_translated": samples_to_time(info.time_reference_low, self.samplerate),
            "timereference": info.time_reference_low,
            "version": info.version,
            "umid": self.ffi_string(info.umid),
            "coding_history": self.ffi_string(info.coding_history)


        }

    def read_metadata(self):
        """Retrieve the broadcast wave bext and iXML chunk metadata """
        self.get_bext()
        self.get_ixml()