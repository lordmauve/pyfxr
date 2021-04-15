Using Soundbuffer objects
=========================

pyfxr's :doc:`sound generation APIs <generating>` return :class:`SoundBuffer`
objects.

A soundbuffer is a packed sequence of 16-bit samples::

    >>> buf = pyfxr.explosion().build()
    >>> len(buf)
    32767
    >>> buf[0]
    2418

but more importantly it supports the buffer protocol, which allows it to be
passed directly to many sound playing APIs (see below).

You can also save a SoundBuffer to a ``.wav`` file, which is very widely
supported::

    buf.save("explosion1.wav")


.. currentmodule:: pyfxr

.. autoclass:: SoundBuffer
    :members:

    .. attribute:: sample_rate: int

        The sample rate in samples per second. Currently, always 44100.

    .. attribute:: channels: int

        The number of channels in the sample. Currently, always 1 (mono).


With Pygame
-----------

Pygame_ can construct a sound from any buffer object, including SoundBuffer::

    buf = pyfxr.tone()
    pygame.mixer.Sound(buffer=buf)

.. _Pygame: https://www.pygame.org/

Be aware that as of Pygame 2.0.1, ``Sound`` objects do not have their own
sample rate and mono/stereo information; they are assumed to have the same
format as the mixer. For correct playback you must initialise the mixer to
44100 kHz mono::

    pygame.mixer.pre_init(pyfxr.SAMPLE_RATE, channels=1)
    pygame.mixer.init()


With Pyglet
-----------

SoundBuffers can also be used as Pyglet_ media sources::

    pyglet.media.StaticSource(buf)

.. _Pyglet: https://pyglet.readthedocs.io/

This does not work by the buffer protocol; SoundBuffer has special adapter
code to allow it to work like this.


With sounddevice
----------------

sounddevice_ provides access to sound devices, without being coupled to a game
or UI framework.

.. _sounddevice: https://python-sounddevice.readthedocs.io/

``sounddevice`` also supports the buffer protocol and can play SoundBuffers
directly::

    import sounddevice
    import pyfxr

    sounddevice.play(pyfxr.jump(), pyfxr.SAMPLE_RATE)
