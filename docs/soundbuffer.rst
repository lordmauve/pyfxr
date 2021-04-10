Using Soundbuffer objects
=========================

pyfxr's :doc:`sound generation APIs <generating>` return :class:`SoundBuffer`
objects.

A soundbuffer is a packed sequence of 16-bit samples::

    >>> buf = pyfxr.explosion()
    >>> len(buf)
    32767
    >>> buf[0]
    2418

but more importantly it supports the buffer protocol, which allows it to be
passed directly to many sound playing APIs, including Pygame::

    pygame.mixer.Sound(buffer=buf)

SoundBuffers can also be used as Pyglet_ media sources::

    pyglet.media.StaticSource(buf)

You can also save a SoundBuffer to a ``.wav`` file, which is very widely
supported::

    buf.save("explosion1.wav")


.. _Pyglet: https://pyglet.readthedocs.io/

.. currentmodule:: pyfxr

.. autoclass:: SoundBuffer
    :members:

    .. attribute:: sample_rate: int

        The sample rate in samples per second. Currently, always 44100.

    .. attribute:: channels: int

        The number of channels in the sample. Currently, always 1 (mono).
