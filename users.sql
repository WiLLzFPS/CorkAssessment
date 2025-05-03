```SQL schema for submission```
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    origin TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    idempotency_key TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);