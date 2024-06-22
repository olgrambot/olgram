-- upgrade --
CREATE TABLE IF NOT EXISTS "promo" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "code" UUID NOT NULL,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "owner_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_promo_code_9b981a" ON "promo" ("code");
-- downgrade --
DROP TABLE IF EXISTS "promo";
