-- 02_test_data.sql
-- Données de test pour les utilisateurs

-- Insérer Alice avec un compte expiré (190 jours dans le passé)
INSERT INTO users (username, password_hash, mfa_secret, gendate, expired) 
VALUES (
    'alice', 
    crypt('x', gen_salt('bf', 12)), -- Hash bcrypt du mot de passe "x"
    'BASE32SECRET',                 -- Secret MFA
    SYSDATE - 190,                -- Date de génération dans le passé
    false                           -- Pas explicitement marqué comme expiré
);

-- Optionnel : Insérer d'autres utilisateurs de test
INSERT INTO users (username, password_hash, mfa_secret, gendate, expired) 
VALUES (
    'bob', 
    crypt('password123', gen_salt('bf', 12)), 
    'ANOTHERSECRET',
    SYSDATE - 30,
    false
);

-- Utilisateur explicitement marqué comme expiré
INSERT INTO users (username, password_hash, mfa_secret, gendate, expired) 
VALUES (
    'charlie', 
    crypt('test', gen_salt('bf', 12)), 
    'THIRDSECRET',
    SYSDATE - 10,
    true  -- Explicitement marqué comme expiré
);