# meme-o-graphy
Projet du Hackathon Shack2025

## Étapes pour lancer le programme
Sous Linux, installé simplement gpg, pour Windows, télécharger [gpg4win](https://www.gpg4win.org/) et créer vous une paire de clé GPG.
Il vous faut Python 3.14+, créer un environnement virtuel et éxécuter:
```
pip install -r requirements.txt
python3 main.py
```

Un onglet "Encode" vous permet d'encoder de l'information dans une image, choisissez une image, un fichier à encoder dans cette image et une destination.
Choisissez des destinataires et cliquer sur "Encode". Normalement, le fichier va être encrypté puis encodé dans cette image.

L'onglet decode vous permet de décoder une image. Si vous êtes dans la liste des destinataires, vous pourrez décrypter l'image et retirer l'information qui y est caché.


## Comment ça marche?
L'information est stocké dans les composantes fréquentielles de l'image. Cela permet d'offrir un minimum de résistance à la compression et le réencodage contrairement à d'autres méthodes comme modifier les bits les moins significatifs des octets.
