# ml_pipeline_template
Un template de pipeline de données pour faire du Machine Learning (avec make).<br><br>

## Guide d'installation de make
Pour commencer, il faut d'abord installer make sur sa machine. Voici un guide d'installation :
### Sous macOS :

Dans le terminal, lancer la commande suivante :

```bash
brew install make 
```

### Sous Windows :

1. **Ouvrir PowerShell en mode administrateur**
    
    Cliquez sur le bouton Démarrer, tapez « PowerShell », faites un clic droit sur « Windows PowerShell » et sélectionnez « Exécuter en tant qu’administrateur ».
    
2. **Vérifier (et ajuster si nécessaire) la politique d’exécution**
    
    Dans la fenêtre PowerShell, tapez :
    
    ```powershell
    Get-ExecutionPolicy
    ```
    
    Si le résultat est `Restricted`, vous devez autoriser temporairement l’exécution de scripts en lançant :
    
    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force;
    ```
    
3. **Exécuter le script d’installation de Chocolatey**
    
    Dans PowerShell (toujours en mode administrateur), lancez la commande suivante qui télécharge et exécute le script d’installation depuis le site officiel de Chocolatey :
    
    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```
    
    L’installation se déroulera automatiquement. Attendez quelques instants jusqu’à ce que le script ait terminé.
    
4. **Vérifier l’installation**
    
    Fermez puis rouvrez PowerShell (en mode normal suffit désormais) et tapez :
    
    ```powershell
    choco --help
    ```
    
    Si Chocolatey est correctement installé, vous verrez s’afficher l’aide de la commande.
    
5. **Utiliser Chocolatey**
    
    Une fois installé, vous pouvez installer make en utilisant la commande :
    
    ```powershell
    choco install make
    ```
<br><br>
## Utilisation du template
Ouvrez un nouveau dossier dans votre IDE puis ouvrez votre terminal.

Pour utiliser ce template, veuillez d'abord construire un environnement virtuel: 

```bash
python -m venv <my-env> # modifier le nom de l'environnement

source <my-env>/bin/activate # avec git bash
```

Puis installer les dépendances: 
```bash
pip install pandas

pip install -U scikit-learn
```

Enfin, on clone le repo:
```bash
git clone git@github.com:jslhost/ml_pipeline_template.git # ou avec HTTPS

cd ml_pipeline_template
```

Veillez à ce que make soit installé, et vous pouvez maintenant lancer la commande suivante:
```bash
make predictions
```
