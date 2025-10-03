# Utilise une image Python 3.9 comme base
FROM python:3.11-slim-bookworm

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Installe make
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

# Copie le fichier requirements.txt et installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code source du projet dans le conteneur
COPY . .

# Remplace les fins de ligne CRLF vers LF (règle bug de permission)
RUN apt-get update \
  && apt-get install -y dos2unix \
  && dos2unix /app/app/run.sh

RUN chmod +x /app/app/run.sh

# Commande par défaut pour exécuter le pipeline
# CMD ["sh", "-c", "make evaluations ; cat reports/classification-report.txt"] - ancienne version
# CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["bash", "-c", "./app/run.sh"]
