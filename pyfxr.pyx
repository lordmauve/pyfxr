#cython: language_level=3

from libc.stdint cimport int16_t, uint32_t
from libc.math cimport sin, pi, floor

from cpython.mem cimport PyMem_Malloc, PyMem_Free


cdef float AMPLITUDE = (1 << 15) - 1


cdef int16_t samp(float v) nogil:
    """Convert a float in [-1, 1] to an int16_t sample."""
    return <int16_t> floor(v * AMPLITUDE)


cdef class Waveform:
    cdef int16_t[1024] waveform

    def __init__(self, gen):
        cdef int i
        for i, val in enumerate(gen):
            self.waveform[i] = samp(val)
            if i == 1023:
                return

        if i != 1023:
            raise ValueError(
                "Waveform generator generated too few values."
            )

    @staticmethod
    def sine():
        cdef Waveform w
        cdef size_t i
        w = Waveform.__new__(Waveform)
        with nogil:
            for i in range(1024):
                w.waveform[i] = samp(
                    sin(pi * 2.0 * i / 1023.0)
                )
        return w

    @staticmethod
    def triangle():
        cdef Waveform w
        cdef size_t i
        cdef float v
        w = Waveform.__new__(Waveform)
        with nogil:
            for i in range(1024):
                if i < 256:
                    v = i / 256
                elif i < 768:
                    v = 1.0 - (i - 255) / 256
                else:
                    v = (i - 768) / 256 - 1.0
                w.waveform[i] = samp(v)
        return w

    @staticmethod
    def saw():
        cdef Waveform w
        cdef size_t i
        cdef float v
        w = Waveform.__new__(Waveform)
        with nogil:
            for i in range(1024):
                w.waveform[i] = samp(i / 512.0 - 1.0)
        return w

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        cdef Py_ssize_t itemsize = sizeof(int16_t)

        buffer.buf = self.waveform
        buffer.format = 'h'                     # double
        buffer.internal = NULL                  # see References
        buffer.itemsize = itemsize
        buffer.len = sizeof(self.waveform)
        buffer.ndim = 1
        buffer.obj = self
        buffer.readonly = 0
        buffer.shape = NULL
        buffer.strides = NULL
        buffer.suboffsets = NULL                # for pointer arrays only

    def __releasebuffer__(self, Py_buffer *buffer):
        pass


cdef class Tone:
    cdef size_t n_samples
    cdef int16_t *samples

    def __cinit__(self, size_t n_samples):
        self.samples = <int16_t*> PyMem_Malloc(n_samples * sizeof(int16_t))
        self.n_samples = n_samples
        if not self.samples:
            raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self.samples)

    @property
    def duration(Tone self):
        return self.n_samples / <float> SAMPLE_RATE

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        cdef Py_ssize_t itemsize = sizeof(int16_t)

        buffer.buf = self.samples
        buffer.format = 'h'                     # double
        buffer.internal = NULL                  # see References
        buffer.itemsize = itemsize
        buffer.len = sizeof(int16_t) * self.n_samples
        buffer.ndim = 1
        buffer.obj = self
        buffer.readonly = 0
        buffer.shape = NULL
        buffer.strides = NULL
        buffer.suboffsets = NULL                # for pointer arrays only

    def __releasebuffer__(self, Py_buffer *buffer):
        pass


cdef float SAMPLE_RATE = 44100


def tone(
    Waveform waveform,
    double pitch=440.0,  # Hz, default = A
    uint32_t attack=4000,
    uint32_t decay=4000,
    uint32_t sustain=30000,
    uint32_t release=20000
):
    cdef uint32_t time = 0
    cdef size_t n_samples, i
    cdef Tone t
    cdef int16_t *samples
    cdef uint32_t omega   # angular velocity
    cdef int16_t v
    cdef float amplitude

    # time and omega will be fixed point where time in real samples
    # is time >> 10

    time = 0
    omega = <uint32_t> (pitch * 1024 / SAMPLE_RATE * 1024)

    n_samples = attack + decay + sustain + release
    t = Tone(n_samples)
    samples = t.samples

    with nogil:
        for i in range(n_samples):
            time += omega
            v = waveform.waveform[(time >> 10) & 0x3ff]

            if i < attack:
                amplitude = (i / <float> attack)
            elif i < attack + decay:
                amplitude = (1.0 - (i - attack) / <float> decay * 0.3)
            elif i < attack + decay + sustain:
                amplitude = 0.7
            else:
                amplitude = (n_samples - i) / release * 0.7

            samples[i] = <int16_t> (amplitude * v)

    return t
