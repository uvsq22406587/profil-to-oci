# Projet – Générateur Profil → Image OCI → Kubernetes

## 1. Présentation

Ce projet automatise la création et le déploiement d’images conteneurisées à partir d’un **profil YAML**.  
Le pipeline complet permet :

1. Lire un profil YAML décrivant le système et les logiciels à installer.
2. Générer une image Docker/OCI correspondant à ce profil.
3. Pousser l’image sur **Docker Hub**.
4. Générer automatiquement les manifests Kubernetes (Deployment, Service, NetworkPolicy).
5. Déployer l’application dans un cluster Kubernetes.

L’objectif est de faciliter la création répétable d’environnements conteneurisés prêts à être déployés.

## 2. Structure du projet

profil-to-oci/
├─ generate.py # Script principal pour générer Dockerfile et manifests Kubernetes

├─ profiles/
│ └─ debug-ubuntu.yaml # Exemple de profil YAML

├─ templates/

│ ├─ Dockerfile.template # Template Dockerfile

│ ├─ deployment.yaml.template # Template Deployment Kubernetes

│ ├─ service.yaml.template # Template Service Kubernetes

│ └─ networkpolicy.yaml.template# Template NetworkPolicy Kubernetes

├─ output/ # Généré automatiquement : Dockerfile + manifests

├─ README.md # Ce fichier

Génération du Dockerfile

Le script generate.py :
Lit le profil YAML.
Mappe l’OS vers une image de base Docker (ubuntu:22.04, debian:12, alpine:3.18).
Injecte la liste de packages dans le Dockerfile à partir du template.
Écrit le Dockerfile final dans output/Dockerfile.

Génération des manifests Kubernetes

Le script génère également :
Deployment (output/deployment.yaml)
Service (output/service.yaml)
NetworkPolicies (output/networkpolicy.yaml)
Ces fichiers utilisent les templates Jinja2 et les variables du profil.

Déploiement

a) Construire et pousser l’image Docker
docker build -t monutilisateur/debug-ubuntu:v1 output/
docker push monutilisateur/debug-ubuntu:v1

b) Déployer sur Kubernetes
kubectl apply -f output/

--- Exemple d’exécution
python3 generate.py

Génère Dockerfile et manifests dans output/.
Construire et pousser l’image avec Docker.
Déployer avec kubectl apply -f output/.


