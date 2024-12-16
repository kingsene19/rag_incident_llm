# IncidentNavigator : Système Intelligent d'Analyse d'Incidents

## Aperçu

IncidentNavigator est un système avancé alimenté par l'IA, conçu pour récupérer, analyser et fournir des insights à partir de registres d'incidents industriels. Le projet exploite les LLMs, recherche vectorielle et apprentissage automatique pour aider les organisations à comprendre et prévenir les accidents du travail.

## Fonctionnalités Principales

- **Intégration de Données Multi-Sources**
  - Combine une base de données vectorielle (Weaviate) avec un stockage de documents (MongoDB)
  - Prend en charge la récupération à travers plusieurs secteurs industriels

- **Mécanismes de Recherche Avancés**
  - Utilise des embeddings HuggingFace pour la recherche sémantique
  - Implémente une compression contextuelle avec reclassement Flashrank
  - Supporte le filtrage par types d'industries

- **Interface Conversationnelle Intelligente**
  - Utilise des modèles de langage de grande taille (LLaMA 3.3 70B)
  - Fournit des réponses détaillées et structurées sur les incidents industriels

## Pile Technologique

- **Recherche Vectorielle** : Weaviate
- **Base de Données** : MongoDB
- **Embeddings** : HuggingFace
- **Modèle de Langage** : LLaMA 3.3 70B
- **Reclassement** : Flashrank
- **Frameworks** : LangChain, Pydantic

## Composants Principaux

1. **CustomReranker** : Un compresseur de documents qui utilise Flashrank pour améliorer la qualité de la recherche
2. **Système de Récupération** : Filtre et récupère des documents d'incidents pertinents
3. **IA Conversationnelle** : Génère des réponses structurées et informatives sur les incidents industriels

## Cas d'Utilisation

- Analyse de sécurité
- Investigation d'incidents
- Évaluation des risques
- Développement de stratégies de prévention

## Pour Commencer

1. Clonez le dépôt
2. Installez les dépendances
3. Configurez les instances locales de Weaviate et MongoDB
4. Configurez les variables d'environnement
5. Exécutez le notebook Jupyter pour interagir avec IncidentNavigator

## Limitations

- Les réponses sont basées sur les données d'incidents disponibles
- Nécessite des mises à jour continues des données pour des insights complets

## Améliorations Futures

- Élargir la couverture des industries
- Implémenter des techniques de reclassement plus avancées
- Ajouter des capacités d'analytique prédictive
