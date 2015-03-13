# Possible Features

- [ ] récuperation automatique des métadonnées
	- [ ] danse
		- [ ] _peut-être_ basé sur des règles (Tempo, Meter; cf. Dixon et all. 2003; les règles ne sont pas trop bonnes)
		- [ ] basé sur un algo d'apprentissage (scikit-learn)
			- [ ] Trouver des traits distinctifs (Tempo, Meter, motif rythmique, ...?) (Echo Nest Remix)
			- [ ] Construire une base de chansons (lescharts.com, tanzmusik-online.de, youtube-dl)
		- [ ] évaluation (matrice de confusion)

	- [ ] titre, interprète (Musicbrainz)
	- [ ] genre (???)

- [ ] Indexation
	Metric trees: R-tree ...

- [ ] implementation (et testes) des requêtes
	- [ ] ensemble de chansons d'une certaine danse
	- [ ] ensemble de chansons d'un certain genre
	- [ ] combinaison des critères
	- [ ] chansons similaire à une chanson donnée
		- [ ] k plus proches voisines (traits distinctifs -> distance)
		- [ ] chanson du genre similaire, mais danse différente (?)
	- [ ] générer des "sets" de chansons
