# Anonymisation de documents PDFS

> Cette branche représente une version modifiée, plus propre, de l'application développée durant le Hackathon, visant à anonymiser des documents PDFS et en bonus pouvoir les reconstruire.

## Description détaillé

### Anonymisation

- Récupération d'un fichier PDF
- Détection des données définies comme étant sensibles (ex: nom, prénom, numéro de téléphone ...)
- Remplacement de ces données dans deux formats possible, tout en gardant la même logique dans les caractères (un mot avec accent, contiendra un accent):
  - Sématiquement similaire (un nom sera remplacé par un nom)
  - Même type (même longueur, même type de caractère à la même position , Bonjour3 -> Ckjbvpl0)
- Génération du PDF résultant ainsi que d'un id de reconnaissance

### Reconstruction

- Récupération d'un id de reconnaissance
- Récupération des données associées
- Remplacement des éléments anonymisés par ceux d'origine
- Génération du PDF résultant (devant ressembler le plus possible à celui d'origine)

![](./architecture/architecture.png)

## Technologies utilisées

- Python comme langage de traitement
- Spacy
- Bert
- Camembert
- FastApi
- Faker

## Manuel d'intégration

