# JCDEuro

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

# TEST TECHNIQUE - AI SISTERS

### **Objectif**

Le but de ce test est d'évaluer la capacité à implémenter une solution backend et frontend intégrant :

1. La génération d’un quiz basé sur deux LLMs (Ollama en local et OpenAI API).
2. Une pipeline RAG (Retrieval-Augmented Generation) exploitant des données issues de Wikipedia pour enrichir les prompts des modèles.
3. Une interface utilisateur permettant de saisir des paramètres pour générer le quiz.

---

### **Étapes à réaliser**

#### **1. Implémentation de la génération de quiz avec 2 LLMs**

-   Connectez **Ollama** (modèle local) et **l’API OpenAI** (GPT).
-   Ajoutez une logique dans le backend pour générer un JSON contenant 5 questions liées à l’**Euro** (le championnat de football) de l'année sélectionnée par l'utilisateur.
    -   Le JSON génére doit correspondre au format de `mockQuestions.json`.
-   Les modèles doivent être appelés avec un **prompt structuré** pour générer ces questions.
-   Gérer les erreurs en cas de réponse incorrecte des modèles ou d'indisponibilité de l’un des services.

#### **2. Pipeline RAG pour enrichir le quiz**

-   Implémentez une pipeline RAG (Retrieval-Augmented Generation) pour récupérer des informations depuis **Wikipedia** sur l’année sélectionnée (par exemple, événements marquants de l’Euro cette année-là).
-   Enrichissez les prompts envoyés aux LLMs avec les données récupérées pour des réponses plus précises et contextualisées.
    -   Exemple de prompt enrichi :
        ```
        {data_from_wikipedia}
        Prompt here
        ```
-   Implémentez un cache pour stocker les résultats RAG afin d’éviter des requêtes répétées (optionnel mais recommandé).

#### **3. Modification du front-end**

-   Ajoutez un **champ d’entrée (input)** permettant à l’utilisateur de sélectionner une année pour le quiz.
-   Ajoutez une option pour inclure ou non les données RAG dans la génération du quiz.

---

### **Critères d'évaluation**

1. **Frontend/Backend**

    - Fonctionnalité pour sélectionner l’année et inclure/exclure RAG.

    - Fonctionnement correct de la génération de quiz avec les deux LLMs.
    - Intégration et utilisation de la pipeline RAG.
    - Gestion des erreurs et validation JSON Schema.

2. **Prompting**

    - Structure et clé de chaque partie du prompt.
    - Utilisation de variables pour inclure dynamiquement les données RAG et l'année sélectionnée par l'utilisateur.

3. **Code**

    - Propreté et lisibilité.
    - Structure modulaire et réutilisable.

4. **Optionnel**
    - Implémentation du cache pour les données RAG.
    - Faire un json schema pour l'output d'openai.
