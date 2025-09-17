# 01 - API

## Qu'est-ce qu'une API ?

Une **API** (Application Programming Interface) est un ensemble de règles et de définitions qui permet à des logiciels de communiquer entre eux. Elle joue le rôle d'intermédiaire entre différentes applications, facilitant l'échange de données et de fonctionnalités.
Très souvent, un système a besoin de communiquer avec d'autres systèmes qui ne sont pas forcément écrit dans le même langage de programmation. L'exemple le plus répandu est la communication entre une interface utilisateur - frontend - (la plupart du temps écrit en JavaScript pour les applications Web) 
et un serveur qui effectue des opérations plus complexes - backend - (écrit en Python, Rust, Go...).

Pour se faire, un format standard d'échange de données est utilisé, c'est le format JSON. Il existe d'autres format de données mais nous nous concentrerons sur le JSON qui est de loin le plus répandu.

### JSON

JSON (JavaScript Object Notation) est un format léger d’échange de données, lisible par les humains et facilement exploitable par les machines. Il représente les données sous forme de paires clé-valeur.
On y retrouve tous les types primitifs présent dans Python, à savoir, des entiers, des floats, des booléens, des chaines de caractères ainsi que des listes et des dictionaires. Le format JSON est une combinaison de tous ces types la

Voici un exemple d'un Objet Utilisateur au format JSON.

```` Un objet Utilisateur au format JSON
{
    "id": 1,
    "first_name": "Morgan", 
    "last_name": "Courivaud", 
    "email": "morgan.courivaud@esiee.fr
}
````

## Pourquoi ?

Les APIs permettent de :
- **Connecter différents systèmes** entre eux.
- **Réutiliser des fonctionnalités** existantes (comme l'envoi d'e-mails ou le traitement de paiements).
- **Accélérer le développement** en évitant de "réinventer la roue".
- **Standardiser les échanges** de données.

![test](../../docs/modern_web_app.png)

## Comment fonctionne une API ? 

1. **Le client** (navigateur, app mobile, etc.) envoie une requête à l'API.
2. **L'API** traite la requête et interagit éventuellement avec une base de données.
3. **Le serveur** renvoie une réponse (souvent au format JSON) au client.

Une requête est une demande d'une application d'effectuer une opération par un autre service. Dans notre cas, les communications sont effectuées par le protocol HTTP.
Pour plus d'information, referez-vous à ce [document](ARCHITECURE.md).

## Avantages

- Modularité du code
- Interopérabilité entre technologies
- Gain de temps
- Sécurité (grâce à l'encapsulation des fonctions)


## Points de vigilance

- Bien documenter l'API
- Gérer les erreurs proprement
- Protéger l'accès (authentification, quotas, etc.)
- Maintenir la compatibilité entre versions

## Différents types d'API

- REST
- WebSocket
- GraphQL

### REST

REST est un ensemble de contraintes architecturales. Il ne s'agit ni d'un protocole, ni d'une norme. Les développeurs d'API peuvent mettre en œuvre REST de nombreuses manières.

Lorsqu'une application émet une requête par le biais d'une API RESTful, celle-ci se charge de partager l'état actuel de la ressource demandée.
Cette information, ou représentation, est fournie via le protocole HTTP souvent au format JSON  (JavaScript Object Notation), cat il ne dépend pas d'un langage et peut être lu aussi bien par les humains que par les machines.

Autre point à retenir : les en-têtes (headers) et paramètres jouent également un rôle majeur dans les d'une requête HTTP d'API REST. Il peuvent contenir de nombreuses informations importantes :

- métadonnées
- autorisation
- URI
- mise en cache
- cookies
- etc.

Il existe des en-têtes de requête et des en-têtes de réponse. Chacun dispose de ses propres informations de connexion HTTP.

Une API RESTful doit remplir les critères suivants :

- Une architecture client-serveur constituée de clients, de serveurs et de ressources, avec des requêtes gérées via HTTP
- Des communications client-serveur stateless, c'est-à-dire que les informations du client ne sont jamais stockées entre les requêtes GET, qui doivent être traitées séparément, de manière totalement indépendante. Le serveur ne doit pas garder de notion d'état ou de statut dans le temps.
- La possibilité de mettre en cache des données afin de rationaliser les interactions client-serveur
- Une interface uniforme entre les composants qui permet un transfert standardisé des informations Cela implique que :
  - les ressources demandées soient identifiables et séparées des représentations envoyées au client ;
  - les ressources puissent être manipulées par le client au moyen de la représentation reçue, qui contient suffisamment d'informations ;
  - les messages autodescriptifs renvoyés au client contiennent assez de détails pour décrire la manière dont celui-ci doit traiter les informations ;
  - l'API possède un hypertexte/hypermédia, qui permet au client d'utiliser des hyperliens pour connaître toutes les autres actions disponibles après avoir accédé à une ressource.
- Un système à couches, invisible pour le client, qui permet de hiérarchiser les différents types de serveurs (pour la sécurité, l'équilibrage de charge, etc.) impliqués dans la récupération des informations demandées

Bien que l'API REST doive répondre à l'ensemble de ces critères, elle est considérée comme étant plus simple à utiliser qu'un protocole tel que SOAP (Simple Object Access Protocol), qui est soumis à des contraintes spécifiques, dont la messagerie XML, la sécurité intégrée et la conformité des transactions, ce qui le rend plus lourd et moins rapide.

### WebSocket

L'API WebSocket est une technologie évoluée qui permet d'ouvrir un canal de communication bidirectionnelle entre un navigateur (côté client) et un serveur. Avec cette API vous pouvez envoyer des messages à un serveur et recevoir ses réponses de manière événementielle sans avoir à aller consulter le serveur pour obtenir une réponse.

### GraphQL

GraphQL est un langage de requête pour les API  qui permet de répondre à des requêtes sur les données existantes. GraphQL fournit une description complète et compréhensible des données de votre API, donne aux clients le pouvoir de demander exactement ce dont ils ont besoin et rien de plus. GraphQL permet aussi de faciliter l'évolution des APIs au fil du temps.

## Les frameworks

Les frameworks sont des outils, ou plutôt des environnements logiciels utilisés pour faciliter et accélérer le développement de certaines briques. Ici nous verrons plusieurs framework web permettant aux developpeurs de créer des API ou des applications Web très facilement sans avoir besoin de tout recoder à la main. Ces frameworks sont souvent accompagnés de modules développés par la communauté et disponible très facilement.
Nous allons voir quelques frameworks les plus connus et ensuite nous concentrer sur celui que nous allons détailler dans le cours : FastAPI.

### Django

Django est un framework python Open Source permettant de créer des API et des sites web. Il a été initialement développé par Adrian Holovaty et Simon Willison en 2003. Django est basé sur le pattern Model Vue Template.
Django est très populaire dans les entreprises pour sa robustesse et sa complétude. Il est utilisé par de nombreux géants américains comme Instagram ou  Youtube mais aussi par de nombreuses entreprises françaises comme Drivy, Blablacar ou encore Deezer.

#### Avantages

- La structure d'un projet Django est très complète, très bien découpée et modulaire, cela permet très facilement d'ajouter ou d'enlever des ensembles de fonctionnalités.
- En plus de la partie purement web, Django propose une solution DRF (Django Rest Framework) qui permet assez facilement de générer des APIs. Comme pour la partie web, la partie REST de Django est très modulaire.
- Django propose aussi par défaut une interface de sécurité qui peut protéger les sites web d'injections SQL par exemple.

#### Inconvénients

- La complexité de la structure et la grande taille  d'un projet Django peuvent entrainer des lenteurs de développement. L'utilisation des modules nécessite de faire très attention aux non-régressions.
- Django est très peu flexible, il est très dépendant des bases SQL, et ne permet pas facilement d'utiliser d'autres types de stockage. 

### Flask

 Flask a été créé par Armin Ronacher, c’ est aussi un framework web écrit en Python, on appelle ça un micro-framework par sa légèreté et sa facilité d'utilisation. Flask permet de développer très facilement et rapidement des applications Web, que ce soit des sites ou des APIs. 
Flask possède une grande communauté et de nombreux packages sont développés par celle-ci. Ces packages permettent de gérer des bases de données, l'authentification, etc.

#### Avantages

- Flask est très simple à comprendre et permet très facilement même pour des débutants  de créer des applications web sans efforts.
- Flask est flexible, ce qui lui permet, contrairement à Django, de changer et d’itérer très facilement. 

#### Inconvénients

- Flask utilise de nombreux modules développés par des personnes tiers, ce qui peut engendrer des failles de sécurité. 
- Flask est un framework synchrone qui va dépiler les requêtes les unes après les autres. Cela peut entraîner des longueurs importantes lorsque des opérations sont longues. 

#### Example

 ```python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return {"message": "Hello World"}

```

### FasAPI

Fast API est un tout nouveau framework web Python, open source et très performant.

#### Avantages

- Il est basé uniquement sur des standars comme JsonSchema (pour la validation des modèles), OAuth2 (pour l’authentification) ou Open API (pour la définition d’interfaces)
- Fast API met en place des méthodes de validation très poussées.
- FastAPI permet aussi de créer des API GraphQL très facilement. 
- Il permet aussi de générer de la documentation technique automatiquement. 

#### Inconvénients

- La jeunesse de ce nouveau framework fait que la communauté est assez récente et assez jeune. Il existe donc que très peu de cours ou tutoriels.


#### Example

```python

from fastapi import FastAPI
app = FastAPI()   
@app.get("/") 
async def root():
     return {"message": "Hello World"}

```

## [Suite](ARCHITECURE.md)
