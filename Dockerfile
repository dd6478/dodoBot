# Utiliser une image Python officielle comme base
FROM python:3.8

# Installer les paquets nécessaires pour la configuration locale
RUN apt-get update && apt-get install -y locales

# Générer le réglage local fr_FR.UTF-8
RUN sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY bot/requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les autres fichiers du bot dans le conteneur
COPY bot /app/bot/
COPY asset /app/asset/

# Définir la commande pour exécuter le bot
CMD ["python", "./bot/__main__.py"]
