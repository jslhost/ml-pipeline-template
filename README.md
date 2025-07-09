[![CI/CD Pipeline](https://github.com/jslhost/ml-pipeline-template/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jslhost/ml-pipeline-template/actions/workflows/ci.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/jslhostdocker/ml-pipeline-template.svg)](https://hub.docker.com/r/jslhostdocker/ml-pipeline-template)

# ml-pipeline-template

Un template de pipeline de données pour faire du Machine Learning (avec make). Ce template est orienté pour la classification mais peut facilement être adapté à la régression.

Une version en ligne du pipeline est disponible [ici](https://jslhost.github.io/ml-pipeline-template/) (l'API peut être momentanément indisponible).

## Sommaire

1.  [Vue d'ensemble du projet](#vue-densemble-du-projet)
2.  [Structure du projet](#structure-du-projet)
3.  [Guide d'installation de make](#guide-dinstallation-de-make)
4.  [Utilisation du template](#utilisation-du-template)
5.  [Configuration avec `params.yaml`](#configuration-avec-paramsyaml)
6.  [Tests](#tests)
7.  [Conteneurisation avec Docker](#conteneurisation-avec-docker)
8.  [Licence](#licence)
9.  [Contributions](#contributions)

## Vue d'ensemble du projet

Ce projet fournit un pipeline de Machine Learning structuré, orchestré par `make`. Le pipeline est divisé en plusieurs étapes, chacune gérée par un script Python dédié dans le répertoire `src/` :

*   `load_data.py`: Charge les données brutes.
*   `clean_data.py`: Nettoie les données chargées.
*   `preprocess_data.py`: Prétraite les données nettoyées.
*   `training.py`: Entraîne le modèle de Machine Learning.
*   `evaluate.py`: Évalue les performances du modèle (crée matrice de confusion et classification report).

Le `Makefile` définit les dépendances entre ces étapes, garantissant que chaque étape est exécutée dans le bon ordre et que seules les étapes nécessaires sont relancées lorsque les fichiers sources changent.

Les paramètres du pipeline et du modèle sont gérés via le fichier `params.yaml`.

## Structure du projet

```
.
├── .github/workflows/ci.yml   # Workflow CI/CD pour l'intégration continue
├── data/                        # Données (générées par le pipeline)
├── reports/                     # Rapports d'évaluation (générés par le pipeline)
├── src/                         # Scripts Python du pipeline
│   ├── __init__.py
│   ├── load_data.py
│   ├── clean_data.py
│   ├── preprocess_data.py
│   ├── training.py
│   └── evaluate.py
├── tests/                       # Tests unitaires et d'intégration
│   └── test_pipeline.py
├── .gitignore                   # Fichiers et dossiers à ignorer par Git
├── Dockerfile                   # Conteneurisation de l'application
├── LICENSE                      # Licence du projet
├── Makefile                     # Orchestration du pipeline
├── params.yaml                  # Paramètres du projet
└── requirements.txt             # Dépendances Python
```

## Guide d'installation de make

Pour commencer, il faut d'abord installer make sur sa machine. Voici un guide d'installation :

### Sous macOS :

Dans le terminal, lancer la commande suivante :

```bash
brew install make
```

### Sous Windows :

1.  **Ouvrir PowerShell en mode administrateur**

    Cliquez sur le bouton Démarrer, tapez « PowerShell », faites un clic droit sur « Windows PowerShell » et sélectionnez « Exécuter en tant qu’administrateur ».

2.  **Vérifier (et ajuster si nécessaire) la politique d’exécution**

    Dans la fenêtre PowerShell, tapez :

    ```powershell
    Get-ExecutionPolicy
    ```

    Si le résultat est `Restricted`, vous devez autoriser temporairement l’exécution de scripts en lançant :

    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force;
    ```

3.  **Exécuter le script d’installation de Chocolatey**

    Dans PowerShell (toujours en mode administrateur), lancez la commande suivante qui télécharge et exécute le script d’installation depuis le site officiel de Chocolatey :

    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

4.  **Vérifier l’installation**

    Fermez puis rouvrez PowerShell (en mode normal suffit désormais) et tapez :

    ```powershell
    choco --help
    ```

    Si Chocolatey est correctement installé, vous verrez s’afficher l’aide de la commande.

5.  **Installer Maker**
   
    Vous pouvez installer make en utilisant la commande :

    ```powershell
    choco install make
    ```

## Utilisation du template

Pour utiliser ce template, suivez les étapes ci-dessous :

1.  **Cloner le dépôt :**

    ```bash
    git clone git@github.com:jslhost/ml-pipeline-template.git # ou avec HTTPS
    cd ml-pipeline-template
    ```

2.  **Créer et activer un environnement virtuel :**

    ```bash
    python -m venv <my-env> # modifier le nom de l'environnement
    source <my-env>/bin/activate # Sous Linux/macOS
    # Pour Windows (PowerShell):
    # .\<my-env>\Scripts\Activate.ps1
    ```

3.  **Installer les dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Exécuter le pipeline avec `make` :**

    Le `Makefile` inclut une commande `help` pour lister toutes les cibles disponibles :

    ```bash
    make help
    ```

    *   **Exécuter le pipeline complet et évaluer le modèle :**

        ```bash
        make all
        ```

        Cette commande exécute toutes les étapes et génère les fichiers suivants :
        - `reports/classification_report.txt`
        - `reports/confusion_matrix.png`
        - `model.pkl`

    *   **Nettoyer les fichiers générés :**

        ```bash
        make clean
        ```

## Configuration avec `params.yaml`

Le fichier `params.yaml` contient les paramètres configurables pour les différentes étapes du pipeline. Vous pouvez modifier ce fichier pour ajuster les hyperparamètres du modèle, les chemins de fichiers, ou d'autres configurations spécifiques à votre cas d'utilisation.

## Tests

Le projet inclut des tests dans le répertoire `tests/`. Pour exécuter les tests, utilisez la commande `make` :

```bash
make tests
```

## Conteneurisation avec Docker

Un `Dockerfile` est fourni pour conteneuriser l'application.

*   **Construire l'image Docker localement :**

    ```bash
    docker build -t ml-pipeline-template .
    ```

*   **Utiliser l'image pré-construite depuis Docker Hub :**

    ```bash
    docker pull jslhostdocker/ml-pipeline-template:latest
    ```

*   **Exécuter le pipeline via Docker :**

    ```bash
    docker run --rm jslhostdocker/ml-pipeline-template:latest
    ```

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) for plus de détails.

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une *issue* ou une *pull request*.



