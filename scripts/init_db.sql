CREATE SCHEMA IF NOT EXISTS app;
CREATE TABLE IF NOT EXISTS app.personas (
  id serial PRIMARY KEY,
  identificacion varchar(64) UNIQUE NOT NULL,
  nombre text NOT NULL,
  email text NOT NULL,
  created_at timestamptz DEFAULT now()
);
