# Cours : Bases de Données SQL
## Introduction aux Bases de Données Relationnelles

### Qu'est-ce qu'une base de données ?
Une base de données (en anglais database) est un ensemble structuré d’informations ou de données, 
généralement stockées de manière électronique dans un système informatique. 

Elle permet à des applications ou utilisateurs d’accéder à ces données, de les modifier, 
de les interroger ou de les supprimer, souvent à l’aide d’un système de gestion de base de données (SGBD).

* Structure organisée :
  - Les données sont souvent structurées en tables (dans les bases relationnelles), ou en documents, graphe, ou objets (dans les bases non relationnelles ou NoSQL). 
  - Exemple (relationnelle) : une table Clients avec les colonnes Nom, Prénom, Adresse.
* Système de gestion de base de données (SGBD) :
  - Logiciel qui permet de créer, modifier, administrer et interroger une base de données.
  - Exemples : MySQL, PostgreSQL, Oracle, MongoDB, SQLite.
* Langage de requête :
  -	Le plus courant est le SQL (Structured Query Language), utilisé pour manipuler des bases relationnelles.
  - Il en existe de nombreux d'autres comme MQL (Mongo Query Language), CQL (Cassandra Query Language), utiles pour les bases de données NoSQL
* Intégrité des données :
  - Les bases de données assurent la cohérence, fiabilité, et exactitude des données à travers des règles (contraintes d’intégrité).
* Sécurité et droits d’accès :
  - Gestion des utilisateurs et de leurs droits pour protéger les données.
* Transactions :
  - Suite d’opérations exécutées comme une unité, respectant les propriétés ACID (Atomicité, Cohérence, Isolation, Durabilité) pour garantir l’intégrité des données même en cas de panne.

### Modèle relationnel (Edgar F. Codd, 1970)
Le modèle relationnel est l’un des concepts les plus fondamentaux en base de données. 
Il a été introduit par Edgar F. Codd en 1970 et reste encore aujourd’hui la base de la majorité des systèmes de gestion de base de données (SGBD) modernes, 
comme MySQL, PostgreSQL, Oracle, SQL Server, etc.

Le modèle relationnel est une méthode pour organiser les données sous forme de relations (ou tables), 
où chaque relation est une collection d’entités (lignes ou enregistrements) ayant les mêmes attributs (colonnes).
Une table n'est alors rien d'autre qu'un tableau à double entrée ligne/colonne, de la même manière qu'une feuille excel ou Google Sheet

Exemple de table Etudiant :
id	nom	    prenom	age
1	Darand	Alice	23
2	Dupont	Marc	24

### Composants d’un SGBD (Système de Gestion de Base de Données)
Un SGBD est un logiciel qui permet de créer, gérer, interroger et sécuriser une base de données.
Il fournit des commandes pour effectuer ces opérations.

Voici les commandes principales :
  - Définition des données: CREATE, ALTER, DROP
  - Manipulation des données: SELECT, INSERT, UPDATE, DELETE
  - Contrôle des données: GRANT, REVOKE
  - Contrôle des transactions: BEGIN, COMMIT, ROLLBACK

Parmi les SGBD les plus connus, on peut citer: PostgreSQL, MySQL, MariaDB...

### Avantages du modèle relationnel

Le modèle relationnel présente de nombreux avantages qui expliquent pourquoi il reste le modèle le plus utilisé dans les systèmes de gestion de bases de données (SGBD) traditionnels.

Voici les principaux avantages :

1. Simplicité conceptuelle
- Les données sont organisées sous forme de tables (relations), ce qui est facile à comprendre, même pour des non-informaticiens.
- La structure tabulaire est proche d’un tableau Excel : lignes = enregistrements, colonnes = champs.
- Il est facile d’ajouter ou supprimer des colonnes, des lignes, ou même des relations sans perturber l’ensemble.

2. Intégrité des données: 
Le modèle relationnel permet de définir et d’appliquer des règles d’intégrité :
- Clé primaire : garantit l’unicité des enregistrements.
- Clé étrangère : assure la cohérence entre les tables liées.
- Contraintes (ex: NOT NULL, UNIQUE, CHECK, etc.).

3. Langage standardisé : SQL
- SQL est un langage déclaratif largement adopté et standardisé.
- Permet des requêtes complexes, des jointures, des regroupements, des analyses, etc.

4. Efficacité
  - Reduction de la duplication des données.
  - Prévention des anomalies de mise à jour.
  - Amélioration la cohérence globale.

5. Transactions fiables
- Atomicité : tout ou rien.
- Cohérence : les données respectent les règles d’intégrité.
- Isolation : les transactions ne se perturbent pas entre elles.
- Durabilité : les données sont conservées même après une panne.

6. Large écosystème et maturité
- Le modèle relationnel est mature, éprouvé, et très bien documenté.
- De nombreux outils, bibliothèques, frameworks et experts sont disponibles.

## À retenir
Les bases relationnelles sont la norme depuis 40+ ans

SQL est le langage universel pour manipuler ces bases

Le modèle relationnel est basé sur la logique des ensembles et les mathématiques relationnelles

Un SGBD garantit performance, intégrité, sécurité et concurrence

## Exemple
Nous avons ici deux tables représentant un système simple de Base de données pour une gestion minimaliste d'un blog internet:
- User
  - id
  - first_name
  - last_name
  - email
- BlogPost
  - id
  - title
  - content
  - created_at
  - author_id

Lorsque l'on s'inscrit sur le site internet, des informations sont enregistrées comme le nom, le prénom ainsi que l'email de l'utilisateur pour lui permettre
de retrouver son compte lors d'une connexion ultérieure.
Chaque article de blog doit également être sauvegardé.

Dans cette table, nous devons enregistrer le lien vers l'utilisateur qui a publié un article, c'est le champ `author_id`.
Ce sera notre clé étrangère vers la table `User`. Cela nous permettra de retrouver les informations de l'auteur du post

![schema_tables.png](img/schema_tables.png)

## Commandes SQL de base

Voici quelques commandes fondamentales en SQL :

- **Créer une table**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
```

- **Insérer des données**
Insérer une nouvelle ligne dans la table :
```sql
INSERT INTO users (nom, email)
VALUES ('Alice Dupont', 'alice.dupont@example.com');
```

- **Lire des données**
Lire toutes les lignes de la table :
```sql
SELECT * FROM users;
```

- **Mettre à jour des données**
Modifier une information pour une ligne spécifique :
```sql
UPDATE users
SET email = 'alice.new@example.com'
WHERE id = 1;
```

- **Supprimer des données**
Supprimer une ligne selon un critère :
```sql
DELETE FROM users
WHERE id = 1;
```

## Exécuter un script SQL dans un conteneur Postgres

Pour exécuter un fichier `.sql` directement dans une base de données PostgreSQL qui tourne dans un conteneur Docker, vous pouvez utiliser la commande suivante depuis votre terminal :

```bash
docker exec -i <nom_du_conteneur_postgres> psql -U <utilisateur> -d <base_de_donnees> < script.sql
```

Dans cette commande, on utilise un operateur `<` qui permet d'injecter le contenu d'un fichier directement dans l'entrée standard (le terminal) du container.

Cette commande permet d'appliquer rapidement des migrations, des créations de tables ou d'autres instructions SQL sur votre base de données Postgres dans Docker.

## 🚀 Index et Optimisation des Performances

### Qu'est-ce qu'un index ?

Un index est une structure de données qui améliore la vitesse des opérations de recherche sur une table. Il fonctionne comme l'index d'un livre : au lieu de parcourir toutes les pages pour trouver un mot, on utilise l'index pour aller directement à la bonne page.

**Avantages :**
- Accélère considérablement les requêtes SELECT avec WHERE, ORDER BY, JOIN
- Améliore les performances des contraintes UNIQUE et PRIMARY KEY
- Optimise les opérations de tri et de regroupement

**Inconvénients :**
- Ralentit les opérations INSERT, UPDATE, DELETE (l'index doit être mis à jour)
- Consomme de l'espace disque supplémentaire
- Peut ralentir les performances si mal utilisé

### Types d'index

**1. Index B-Tree (par défaut)**
- Structure arborescente équilibrée
- Idéal pour les recherches par égalité, plages de valeurs, et tri
- Utilisé par défaut dans la plupart des SGBD

**2. Index Hash**
- Basé sur une fonction de hachage
- Très rapide pour les recherches par égalité exacte
- Ne supporte pas les plages de valeurs

**3. Index partiel**
- Index créé seulement sur un sous-ensemble de lignes
- Économise l'espace et améliore les performances pour des cas spécifiques

![schema_index.png](img/schema_index.png)

### Création et gestion des index

**Créer un index simple :**
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Créer un index composé :**
```sql
CREATE INDEX idx_blogpost_author_date ON BlogPost(author_id, created_at);
```

**Créer un index partiel :**
```sql
CREATE INDEX idx_active_users ON users(email) WHERE active = true;
```

**Créer un index unique :**
```sql
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

**Supprimer un index :**
```sql
DROP INDEX idx_users_email;
```

### Stratégies d'indexation

**1. Colonnes fréquemment utilisées dans WHERE**
```sql
-- Si on fait souvent : SELECT * FROM users WHERE email = ?
CREATE INDEX idx_users_email ON users(email);
```

**2. Colonnes de jointure**
```sql
-- Pour optimiser les JOIN entre BlogPost et User
CREATE INDEX idx_blogpost_author_id ON BlogPost(author_id);
```

**3. Colonnes utilisées pour le tri**
```sql
-- Pour optimiser : ORDER BY created_at DESC
CREATE INDEX idx_blogpost_created_at ON BlogPost(created_at DESC);
```

### Analyser les performances

**Utiliser EXPLAIN pour analyser une requête :**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';
```

**Lister les index d'une table (PostgreSQL) :**
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users';
```

## 🔧 Triggers et Procédures Stockées

### Triggers (Déclencheurs)

Un trigger est un bloc de code SQL qui s'exécute automatiquement en réponse à certains événements sur une table ou une vue.

**Types de triggers :**
- **BEFORE** : s'exécute avant l'opération (INSERT, UPDATE, DELETE)
- **AFTER** : s'exécute après l'opération
- **INSTEAD OF** : remplace l'opération (principalement pour les vues)

### Cas d'usage des triggers

**1. Audit et historique**
```sql
-- Table d'audit
CREATE TABLE user_audit (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(10),
    old_values JSONB,
    new_values JSONB,
    changed_at TIMESTAMP DEFAULT NOW(),
    changed_by VARCHAR(50)
);

-- Trigger d'audit
CREATE OR REPLACE FUNCTION audit_user_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO user_audit (user_id, action, old_values, changed_at)
        VALUES (OLD.id, 'DELETE', to_jsonb(OLD), NOW());
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO user_audit (user_id, action, old_values, new_values, changed_at)
        VALUES (NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), NOW());
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO user_audit (user_id, action, new_values, changed_at)
        VALUES (NEW.id, 'INSERT', to_jsonb(NEW), NOW());
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Attacher le trigger à la table
CREATE TRIGGER trigger_audit_users
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_user_changes();
```

**2. Validation automatique et mise à jour de champs**
```sql
-- Trigger pour mettre à jour automatiquement updated_at
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_modified_column();
```

**3. Validation des données**
```sql
-- Trigger pour valider l'email
CREATE OR REPLACE FUNCTION validate_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Email invalide: %', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_user_email
    BEFORE INSERT OR UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION validate_email();
```

### Procédures Stockées

Une procédure stockée est un ensemble d'instructions SQL précompilées et stockées dans la base de données.

**Avantages :**
- Performance améliorée (code précompilé)
- Sécurité renforcée (encapsulation de la logique)
- Réutilisabilité du code
- Réduction du trafic réseau

**Exemple de procédure stockée :**
```sql
-- Procédure pour créer un utilisateur avec validation
CREATE OR REPLACE FUNCTION create_user_with_validation(
    p_nom VARCHAR(50),
    p_email VARCHAR(100),
    p_age INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    new_user_id INTEGER;
BEGIN
    -- Validation
    IF p_nom IS NULL OR LENGTH(p_nom) < 2 THEN
        RAISE EXCEPTION 'Le nom doit contenir au moins 2 caractères';
    END IF;

    IF p_email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Email invalide';
    END IF;

    IF p_age IS NOT NULL AND (p_age < 0 OR p_age > 150) THEN
        RAISE EXCEPTION 'Age invalide';
    END IF;

    -- Insertion
    INSERT INTO users (nom, email, age, created_at)
    VALUES (p_nom, p_email, p_age, NOW())
    RETURNING id INTO new_user_id;

    -- Log
    RAISE NOTICE 'Utilisateur créé avec ID: %', new_user_id;

    RETURN new_user_id;
END;
$$ LANGUAGE plpgsql;

-- Utilisation
SELECT create_user_with_validation('Jean Dupont', 'jean@example.com', 30);
```

**Fonction avec gestion d'erreurs :**
```sql
CREATE OR REPLACE FUNCTION get_user_posts_count(p_user_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    posts_count INTEGER;
BEGIN
    -- Vérifier que l'utilisateur existe
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = p_user_id) THEN
        RAISE EXCEPTION 'Utilisateur avec ID % non trouvé', p_user_id;
    END IF;

    -- Compter les posts
    SELECT COUNT(*) INTO posts_count
    FROM BlogPost
    WHERE author_id = p_user_id;

    RETURN posts_count;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erreur lors du comptage des posts: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
```

### Gestion des triggers et procédures

**Lister les triggers :**
```sql
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public';
```

**Supprimer un trigger :**
```sql
DROP TRIGGER IF EXISTS trigger_audit_users ON users;
```

**Lister les fonctions/procédures :**
```sql
SELECT proname, pronargs
FROM pg_proc
WHERE pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public');
```

**Supprimer une fonction :**
```sql
DROP FUNCTION IF EXISTS create_user_with_validation(VARCHAR, VARCHAR, INTEGER);
```