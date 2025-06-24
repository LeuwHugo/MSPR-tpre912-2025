-- CREATE EXTENSION IF NOT EXISTS pgcrypto; -- Not valid in Oracle

CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username    VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  mfa_secret  TEXT NOT NULL,
  gendate     TIMESTAMP NOT NULL DEFAULT NOW(),
  expired     BOOLEAN   NOT NULL DEFAULT FALSE
);
