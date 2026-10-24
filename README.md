# L-System Fractal Generator

Générateur de fractals utilisant des L-systèmes. Il combine un moteur d'expansion symbolique pur en **Haskell** et un moteur de rendu vectoriel en **Python** produisant des GIF animés.

---

## Architecture du Pipeline

```text
rules/*.txt ──> [ Haskell (Main.hs) ] ──(stdout / pipe)──> [ Python (graphics.py) ] ──> animations/*.gif
```

* **Haskell (`Main.hs`)** : Lit le fichier de grammaire, extrait l'angle, la graine et les règles de réécriture, calcule les $N$ itérations, puis envoie le flux sur `stdout`.
* **Python (`graphics.py`)** : Lit les chaînes sur `stdin` et assemble l'animation sous forme de GIF dans le dossier `animations/` avec des graphiques de tortues.

---

## Prérequis

- **GHC / Haskell**
- **Python 3** avec la bibliothèque **Pillow** :
  ```bash
  pip install pillow

---

## Commandes d'exécution

### 1. Syntaxe générale

```bash
runhaskell Main.hs <chemin_regle> <nombre_iterations> | python3 graphics.py <nom_fichier_gif>
```

### 2. Exemples prêts à l'emploi

* **Barnsley Fern** :
  ```bash
  runhaskell Main.hs rules/barnsley_fern.txt 6 | python3 graphics.py barnsley.gif
  ```

---

## Format d'un fichier de règles (`rules/*.txt`)

```text
#Comment
angle: ANGLE
seed: SEED
X -> EXPENSION_X
Y -> EXPENSION_X
...
```
- `angle:` Angle de rotation de la tortue en degrés pour `+` et `-`.
- `seed:` Chaîne de départ.
- `A -> B:` Règle de remplacement de chaque caractère `A` par `B`. `A` doit être un seul caractère. `B` peut être une chaine de caractères.

**Caractères spéciaux**
- `+` Tourne de `angle` degrés dans le sens antihoraire.
- `-` Tourne de `angle` degrés dans le sens horaire.
- `F` Trace dans la direction orientée.
- `[` Push la postition et l'orientation actuelle dans le stack.
- `]` Pop une postition et une orientation du stack.

---

## Utilisation de l'IA

Une IA a été utilisée en colaboration avec moi-même pour effectuer les parties suivantes du projet:

- L'utilisation de la bibliotèque *Pillow* et la génération de graphique
- La lecture de fichiers depuis Haskell
- La création du README

Les exemples ont étés adaptés depuis la page Wikipédia des [systèmes de Lindenmayer](https://en.wikipedia.org/wiki/L-system).