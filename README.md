# Euromusic
Banques de données multimédia


## Objectifs

- Classer des extraits musicaux selon le type de danse.
- Se baser sur le spectrogramme de la musique.
- Cf Shazam, SoundHound


## Utilisation

- Le dossier "Main" contient l'application principale.
- `Main/main.py` suivi par un dossier qui contient les fichiers musique lance une démonstration du programme qui catalogue la collection musicale de l'utilisateur dans une base de données SQL
- `Apprentissage/train.py` suivi par le ficher `Apprentissage/songDataFull.tab` qui contient les données récupérées par les différentes bases de données utilisées montre le processus de l'apprentissage et calcule aussi une précision par le moyen de cross-validation 

## Guide d'Installation
Testé sous Ubuntu 14.04.2 LTS

### Echo Nest Remix
Cette bibliothèque est necessaire pour l'analyse des chansons.

- Suivre le [guide d'installation (anglais)](http://echonest.github.io/remix/installsource.html) officiel.
- Obtenir un [API Key](http://echonest.github.io/remix/keysetup.html).

-  Ajouter cette ligne au ficher `~/.profile` (pour Ubuntu)
   ```
   export ECHO_NEST_API_KEY="ton API Key"
   ```

4. Redémarrer la console

5. Il y a beaucoup d'examples dans `/usr/local/share/echo-nest-remix-examples`.  
   Pour tester, on peut par exemple aller dans ce dossier et taper:
   ```
   python one/one.py music/Karl_Blau-Gnos_Levohs.mp3 AllOnTheOne.mp3
   ```

### SoX
    Ce programme est utilisé pour extraire 30 secondes de chaque chansons avant le téléchargement au serveur de Echo Nest Remix
    ```
    sudo apt-get install sox
    ```

### Chromaprint
    Cet outil est necessaire pour calculer le "fingerprint" d'une chanson pour l'envoyer à MusicBrainz
    ```
    sudo apt-get install libchromaprint-tools
    ```

### scikit-learn
    Une bibliothèque qui implémente beaucoup d'algos d'apprentissage
    ```
    sudo apt-get install python-sklearn
    ```


## Références

[Gizmodo](https://gizmodo.com/5647458/how-shazam-works-to-identify-nearly-every-song-you-throw-at-it)  
[Columbia University (New York)](https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf)  
[So, you code ?)](https://www.soyoucode.com/2011/how-does-shazam-recognize-song)  

### Articles

[Classification of dance music by periodicity patterns](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.414.9917&rep=rep1&type=pdf)  
[Characterisation of music via rhythmic patterns](http://mtg.upf.edu//ismir2004/review/CRFILES/paper165-b28308914f720be8d4c5f00bf2a5c9aa.pdf)  
[Fast and robust meter and tempo recognition for the automatic discrimination of ballroom dance styles](https://mediatum.ub.tum.de/doc/1138560/1138560.pdf)

### Software
[Echo Nest Remix - Python API to analyse sound](https://echonest.github.io/remix/)  
[Musicbrainz - Web Service (with Python API) to get song title from fingerprint](https://musicbrainz.org/doc/python-musicbrainz2)  
[youtube-dl - Python Library to download videos/songs from youtube](https://github.com/rg3/youtube-dl/)  
[scikit-learn - Python Library for machine learning](http://scikit-learn.org/stable/)

### Data
[(German) crowd sourced database of song-dance-correspondencies](https://www.tanzmusik-online.de/)  
[French Single Charts](http://www.lescharts.com/weekchart.asp?cat=s)
