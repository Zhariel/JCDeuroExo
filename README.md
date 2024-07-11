# JCDEuro
cle open ai
sk-proj-TjddBHxgClIVcGRup9ePT3BlbkFJj35HyubbySV75SZBGTLB

**<span style="color:red;">Suivre les instructions des sections [Prérequis](#prérequis) et [Installation](#installation) avant les ateliers du jeudi 11 juillet.</span>**

## Prérequis

### Python

Installez [Python 3.12](https://www.python.org/downloads/). Pour vérifier votre installation :

```sh
python --version
# Vous devriez voir : Python 3.12.4
```

Puis, pour la gestion des dépendances, installez [pipenv](https://pypi.org/project/pipenv/) :

```sh
pip install pipenv
```

Note : si les commandes `python`et `pip` ne fonctionnent pas, vous pouvez tester avec `python3` et `pip3`.

### Node.js

Installez la dernière version de Node.js en suivant les [instructions](https://nodejs.org/en/download/package-manager).

### Angular

Installez [Angular 18](https://angular.fr/get_started/installation) :

```sh
npm install -g @angular/cli
```

Pour vérifier votre installation :

```sh
ng version
```

### Ollama

Installez [Ollama](https://ollama.com/download/).

## Installation

### Cloner le dépôt

Naviguez vers le dossier où vous voulez installer le projet et clonez-le :

```bash
git clone https://github.com/AI-Sisters/JCDeuroExo.git
cd JCDeuroExo
```

### Configurer le Backend

```bash
cd backend
pipenv install
```

Activez l'environnement virtuel :

```bash
pipenv shell
```

### Configurer le Frontend

```bash
cd ../frontend
npm install
```

### Ollama

Si vous avez au moins 8Go de RAM disponible, vous pourrez utiliser Mistral 7B via Ollama. Téléchargez ce modèle (~4Go) :

```bash
ollama pull mistral
```

Vous pouvez également explorer d'autres [modèles](https://ollama.com/library?sort=featured), en fonction de la configuration de votre machine (comptez 1Go de RAM disponible nécessaire par milliard de paramètres).

## Exécution de l'application

### Démarrer le service Ollama

Avant de lancer le serveur backend, assurez-vous que le service Ollama est en cours d'exécution. Ouvrez un nouveau terminal et exécutez :

```bash
ollama serve
```

### Démarrer le serveur Backend

Ouvrez un nouveau terminal, naviguez dans le répertoire du backend et exécutez :

```bash
pipenv shell
uvicorn main:app --reload
```

Cela démarrera le serveur Uvicorn pour FastAPI sur `http://localhost:8000`.

### Démarrer l'application Frontend

Ouvrez un nouveau terminal, naviguez dans le répertoire du frontend et exécutez :

```bash
ng serve
```

Cela compilera l'application Angular et la servira sur `http://localhost:4200`.

## Utilisation

Ouvrez un navigateur web et naviguez vers `http://localhost:4200` pour utiliser l'application.
