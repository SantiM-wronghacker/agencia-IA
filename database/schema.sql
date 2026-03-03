-- ═══════════════════════════════════════════════════════════════
-- Agencia IA - Database Schema (PostgreSQL 15)
-- ═══════════════════════════════════════════════════════════════

-- ─── Agent Registry ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS agent_registry (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL UNIQUE,
    category        VARCHAR(100) NOT NULL,
    subcategory     VARCHAR(100),
    description     TEXT,
    module_path     VARCHAR(500) NOT NULL,
    capabilities    TEXT[],
    version         VARCHAR(20) DEFAULT '1.0.0',
    status          VARCHAR(20) DEFAULT 'active',
    preferred_model VARCHAR(50) DEFAULT 'groq',
    config          JSONB DEFAULT '{}',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agent_category ON agent_registry(category);
CREATE INDEX idx_agent_status ON agent_registry(status);
CREATE INDEX idx_agent_capabilities ON agent_registry USING GIN(capabilities);
CREATE INDEX idx_agent_name ON agent_registry(name);

-- ─── Agent Execution Tracking ────────────────────────────────

CREATE TABLE IF NOT EXISTS agent_execution (
    id              SERIAL PRIMARY KEY,
    agent_id        INTEGER REFERENCES agent_registry(id),
    started_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at     TIMESTAMP,
    duration_ms     INTEGER,
    status          VARCHAR(20) DEFAULT 'running',
    input_summary   TEXT,
    output_summary  TEXT,
    error_message   TEXT,
    model_used      VARCHAR(50),
    tokens_used     INTEGER DEFAULT 0,
    trace_id        VARCHAR(64)
);

CREATE INDEX idx_execution_agent ON agent_execution(agent_id);
CREATE INDEX idx_execution_status ON agent_execution(status);
CREATE INDEX idx_execution_started ON agent_execution(started_at);

-- ─── Agent Dependencies ──────────────────────────────────────

CREATE TABLE IF NOT EXISTS agent_dependencies (
    id              SERIAL PRIMARY KEY,
    agent_id        INTEGER REFERENCES agent_registry(id),
    depends_on_id   INTEGER REFERENCES agent_registry(id),
    dependency_type VARCHAR(50) DEFAULT 'requires',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_id, depends_on_id)
);

CREATE INDEX idx_deps_agent ON agent_dependencies(agent_id);
CREATE INDEX idx_deps_depends_on ON agent_dependencies(depends_on_id);

-- ─── Agent Health ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS agent_health (
    id              SERIAL PRIMARY KEY,
    agent_id        INTEGER REFERENCES agent_registry(id),
    checked_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_healthy      BOOLEAN DEFAULT TRUE,
    response_ms     INTEGER,
    error_count     INTEGER DEFAULT 0,
    success_rate    DECIMAL(5,2) DEFAULT 100.00,
    details         JSONB DEFAULT '{}'
);

CREATE INDEX idx_health_agent ON agent_health(agent_id);
CREATE INDEX idx_health_checked ON agent_health(checked_at);

-- ─── Agent Versions ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS agent_versions (
    id              SERIAL PRIMARY KEY,
    agent_id        INTEGER REFERENCES agent_registry(id),
    version         VARCHAR(20) NOT NULL,
    changelog       TEXT,
    module_path     VARCHAR(500),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_versions_agent ON agent_versions(agent_id);
CREATE INDEX idx_versions_active ON agent_versions(is_active);

-- ─── Sessions (migrated from SQLite) ─────────────────────────

CREATE TABLE IF NOT EXISTS sessions (
    id              SERIAL PRIMARY KEY,
    session_id      VARCHAR(100) UNIQUE NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata        JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS messages (
    id              SERIAL PRIMARY KEY,
    session_id      VARCHAR(100) REFERENCES sessions(session_id),
    role            VARCHAR(20) NOT NULL,
    content         TEXT NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata        JSONB DEFAULT '{}'
);

CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_messages_created ON messages(created_at);
