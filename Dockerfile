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

# Commande par défaut pour exécuter le pipeline
CMD ["make", "evaluations"]
CMD ["cat", "reports/classification-report.txt"]
