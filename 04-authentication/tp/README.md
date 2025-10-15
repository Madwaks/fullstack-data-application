# Exercice 

## Partie 1
- Ajoutez une expiration dans le token JWT encodé par l'endpoint `/auth/token`
  - Lors du décodage du token, vérifiez que le token n'est pas expiré avant d'autorisation l'accès aux différentes ressources

## Partie 2
- Ajoutez un système de role pour les utilisateurs
  - Un utilisateur peut être admin, contributor, anonymous...
  - Chaque endpoint pourra être accessible en fonction du rôle de l'utilisateur qui demande accès a la ressource
    - Par exemple, supprimer tous les Posts du site web ne peut être accessible que par un administrateur

## Partie 3
- Appliquez ces nouvelles fonctionnalités de sécurité à votre projet

