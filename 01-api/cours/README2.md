# Qu'est-ce qu'une API ?

Une **API** (Application Programming Interface) est un ensemble de règles et de définitions qui permet à des logiciels de communiquer entre eux. Elle joue le rôle d'intermédiaire entre différentes applications, facilitant l'échange de données et de fonctionnalités.

---

## 🧠 Définition simple

Une API est comme un **menu dans un restaurant**. Il décrit ce que vous pouvez commander, mais pas comment la cuisine prépare les plats. De même, une API vous dit quelles opérations sont disponibles, mais cache la complexité du système sous-jacent.

---

## 🧩 Pourquoi utiliser une API ?

Les APIs permettent de :
- **Connecter différents systèmes** entre eux.
- **Réutiliser des fonctionnalités** existantes (comme l'envoi d'e-mails ou le traitement de paiements).
- **Accélérer le développement** en évitant de "réinventer la roue".
- **Standardiser les échanges** de données.

---

## 📦 Types d'API

| Type d'API     | Description |
|----------------|-------------|
| **REST**       | Utilise HTTP pour accéder à des ressources, très populaire pour les applications web. |
| **SOAP**       | Basé sur XML, souvent utilisé dans les systèmes d'entreprise. |
| **GraphQL**    | Permet de récupérer exactement les données demandées, ni plus ni moins. |
| **API locales** | Interfaces internes entre modules d'une même application. |

---

## 🌐 Exemple simple d'une API REST

Imaginons une API qui gère une bibliothèque :

- `GET /livres` → Liste tous les livres.
- `POST /livres` → Ajoute un nouveau livre.
- `GET /livres/123` → Donne les détails du livre avec l'ID 123.
- `DELETE /livres/123` → Supprime le livre 123.

---

## 🛠️ Comment fonctionne une API ?

1. **Le client** (navigateur, app mobile, etc.) envoie une requête à l'API.
2. **L'API** traite la requête et interagit éventuellement avec une base de données.
3. **Le serveur** renvoie une réponse (souvent au format JSON) au client.

---

## ✅ Avantages

- Modularité du code
- Interopérabilité entre technologies
- Gain de temps
- Sécurité (grâce à l'encapsulation des fonctions)

---

## ⚠️ Points de vigilance

- Bien documenter l'API
- Gérer les erreurs proprement
- Protéger l'accès (authentification, quotas, etc.)
- Maintenir la compatibilité entre versions

---

## 📚 Ressources utiles

- [MDN Web Docs – APIs](https://developer.mozilla.org/fr/docs/Learn/JavaScript/Client-side_web_APIs/Introduction)
- [REST API Tutorial](https://restfulapi.net/)
- [GraphQL Documentation](https://graphql.org/)

---

*Document écrit en Markdown – idéal pour être affiché sur GitHub ou dans un éditeur comme Visual Studio Code.*