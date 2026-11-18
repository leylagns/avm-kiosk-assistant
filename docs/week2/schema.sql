-- AVM Rehber Kiosk: PostgreSQL şeması (Hafta 2 taslağı; Hafta 4'te migration'a dönüştürülecek)

CREATE TABLE floors (
    floor_no INT PRIMARY KEY CHECK (floor_no BETWEEN 0 AND 10),
    name     TEXT NOT NULL
);

CREATE TABLE graph_nodes (
    node_id  SERIAL PRIMARY KEY,
    floor_no INT NOT NULL REFERENCES floors(floor_no),
    kind     TEXT NOT NULL CHECK (kind IN ('corridor','store','facility','elevator','escalator','entrance','kiosk')),
    x        REAL NOT NULL,
    y        REAL NOT NULL
);

CREATE TABLE graph_edges (
    edge_id   SERIAL PRIMARY KEY,
    from_node INT NOT NULL REFERENCES graph_nodes(node_id),
    to_node   INT NOT NULL REFERENCES graph_nodes(node_id),
    weight_m  REAL NOT NULL CHECK (weight_m > 0),
    edge_type TEXT NOT NULL DEFAULT 'walk' CHECK (edge_type IN ('walk','elevator','escalator')),
    CHECK (from_node <> to_node)
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE
);

CREATE TABLE category_aliases (
    alias_id    SERIAL PRIMARY KEY,
    category_id INT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    alias       TEXT NOT NULL,
    UNIQUE (category_id, alias)
);

CREATE TABLE facility_types (
    type_id SERIAL PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE facility_aliases (
    alias_id SERIAL PRIMARY KEY,
    type_id  INT NOT NULL REFERENCES facility_types(type_id) ON DELETE CASCADE,
    alias    TEXT NOT NULL,
    UNIQUE (type_id, alias)
);

CREATE TABLE stores (
    store_id    TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    category_id INT NOT NULL REFERENCES categories(category_id),
    node_id     INT REFERENCES graph_nodes(node_id),
    zone        TEXT,
    opens_at    TIME NOT NULL,
    closes_at   TIME NOT NULL
);

CREATE TABLE facilities (
    facility_id TEXT PRIMARY KEY,
    type_id     INT NOT NULL REFERENCES facility_types(type_id),
    node_id     INT REFERENCES graph_nodes(node_id),
    description TEXT
);

CREATE TABLE admin_users (
    user_id       SERIAL PRIMARY KEY,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'admin' CHECK (role IN ('admin','viewer'))
);

CREATE TABLE model_versions (
    model_id     SERIAL PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    kind         TEXT NOT NULL CHECK (kind IN ('E1','E2','E3')),
    val_macro_f1 REAL,
    is_active    BOOLEAN NOT NULL DEFAULT FALSE,
    activated_by INT REFERENCES admin_users(user_id)
);
CREATE UNIQUE INDEX one_active_model ON model_versions ((is_active)) WHERE is_active;

CREATE TABLE query_logs (
    log_id     BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    query_text TEXT,              -- log kapalıysa NULL tutulur (R9)
    intent     TEXT,
    confidence REAL,
    model_id   INT REFERENCES model_versions(model_id),
    latency_ms INT
);
