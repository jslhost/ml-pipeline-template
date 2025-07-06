[![publish-docker-image](https://github.com/jslhost/ml-pipeline-template/actions/workflows/prod.yml/badge.svg)](https://github.com/jslhost/ml-pipeline-template/actions/workflows/prod.yml)

# ml-pipeline-template

Un template de pipeline de données pour faire du Machine Learning (avec make). Ce template est orienté pour la classification mais peut facilement être adapté à la régression.

## Sommaire

1.  [Vue d'ensemble du projet](#vue-densemble-du-projet)
2.  [Guide d'installation de make](#guide-dinstallation-de-make)
3.  [Utilisation du template](#utilisation-du-template)
4.  [Configuration avec `params.yaml`](#configuration-avec-paramsyaml)
5.  [Tests](#tests)
6.  [Conteneurisation avec Docker](#conteneurisation-avec-docker)

## Vue d'ensemble du projet

Ce projet fournit un pipeline de Machine Learning structuré, orchestré par `make`. Le pipeline est divisé en plusieurs étapes, chacune gérée par un script Python dédié dans le répertoire `src/` :

*   `load_data.py`: Charge les données brutes.
*   `clean_data.py`: Nettoie les données chargées.
*   `preprocess_data.py`: Prétraite les données nettoyées.
*   `training.py`: Entraîne le modèle de Machine Learning.
*   `evaluate.py`: Évalue les performances du modèle (crée matrice de confusion et classification report).

Le `Makefile` définit les dépendances entre ces étapes, garantissant que chaque étape est exécutée dans le bon ordre et que seules les étapes nécessaires sont relancées lorsque les fichiers sources changent.

Les paramètres du pipeline et du modèle sont gérés via le fichier `params.yaml`.

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

    Assurez-vous que `make` est installé. Vous pouvez exécuter différentes étapes du pipeline :

    *   **Exécuter le pipeline complet et évaluer le modèle :**

        ```bash
        make evaluations
        ```

        Cette commande va exécuter toutes les étapes nécessaires : chargement des données, nettoyage, prétraitement, entraînement du modèle et évaluation.

    *   **Entraîner le modèle uniquement :**

        ```bash
        make model
        ```

    *   **Générer les données brutes :**

        ```bash
        make data/raw_dataset.csv
        ```

    *   **Nettoyer les données :**

        ```bash
        make data/clean_dataset.csv
        ```

    *   **Prétraiter les données :**

        ```bash
        make data/preprocessed_features.npz
        ```

## Configuration avec `params.yaml`

Le fichier `params.yaml` contient les paramètres configurables pour les différentes étapes du pipeline. Vous pouvez modifier ce fichier pour ajuster les hyperparamètres du modèle, les chemins de fichiers, ou d'autres configurations spécifiques à votre cas d'utilisation.

## Tests

Le projet inclut des tests dans le répertoire `tests/`. Pour exécuter les tests, assurez-vous d'avoir installé `pytest` (inclus dans `requirements.txt`) et exécutez la commande suivante à la racine du projet :

```bash
pytest
```

## Conteneurisation avec Docker

Un `Dockerfile` est fourni pour conteneuriser l'application. Cela permet de créer un environnement reproductible pour le pipeline. Pour construire l'image Docker, exécutez la commande suivante à la racine du projet :

```bash
docker build -t ml-pipeline-template .
```

Une fois l'image construite, vous pouvez l'exécuter pour tester les évaluations :

```bash
docker run --rm ml-pipeline-template
```
