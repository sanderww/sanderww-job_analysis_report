#!/bin/bash

# Stap 1: Checkout naar de dev branch
git checkout dev

# Stap 2 & 3: Alle wijzigingen committen met een bericht van de gebruiker
echo "Voer een commit message in:"
read commit_message

git add .
git commit -m "$commit_message"

# Stap 4: Checkout naar main en merge dev in main
git checkout main
git merge dev

# Stap 5: Push main naar de remote repository
git push origin main

echo "✅ Dev is succesvol gemerged in main en gepusht naar de remote!"