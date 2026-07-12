@echo off
REM === Initialisation du dépôt Git ===
git init

REM === Renommer la branche principale en main ===
git branch -M main

REM === Ajouter le dépôt GitHub comme remote ===
git remote add origin https://github.com/mahafouzmaiga2019-star/projet-8-abm.git

REM === Vérifier le remote ===
git remote -v

REM === Ajouter tous les fichiers et faire un commit ===
git add .
git commit -m "Initial commit : structure ABM, scripts de simulation et documentation"

REM === Pousser vers GitHub ===
git push -u origin main

pause
