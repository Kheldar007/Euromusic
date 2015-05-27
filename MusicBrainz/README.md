# Installer MusicBrainz

Sous Ubuntu:

1. Installer Python.

2. Installer libdiscid.

```
apt-get install python-libdiscid (Python 2) ou apt-get install python3-libdiscid (Python 3)
```

3. Telecharger le [programme d'installation](http://ftp.musicbrainz.org/pub/musicbrainz/python-musicbrainz2/python-musicbrainz2-0.7.4.tar.gz).

4. Dans le dossier d'installation,

```
python setup.py install --install-layout=deb
```


# Installer AcousID (fingerprinting).

1. Installer cmake.

```
apt-get install cmake
```

2. Installer qt.

```
apt-get install libqt4-dev
```

3. Installer [chromaprint](https://acoustid.org/chromaprint).
