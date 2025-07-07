# Utilise une image Python 3.9 comme base
FROM python:3.9-slim-buster

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Installe make
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

# Copie le fichier requirements.txt et installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code source du projet dans le conteneur
COPY . .
RUN chmod +x /app/run.sh

# Commande par défaut pour exécuter le pipeline
# CMD ["sh", "-c", "make evaluations ; cat reports/classification-report.txt"] - ancienne version
CMD ["bash", "-c", "./app/run.sh"]
