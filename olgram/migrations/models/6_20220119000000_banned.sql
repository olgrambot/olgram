-- upgrade --
CREATE TABLE IF NOT EXISTS "bot_banned_user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "telegram_id" BIGINT NOT NULL,
    "username" VARCHAR(100),
    "bot_id" INT NOT NULL REFERENCES "bot" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_bot_banned__telegra_915aca" ON "bot_banned_user" ("telegram_id");
-- downgrade --
DROP TABLE IF EXISTS "bot_banned_user";
DROP INDEX IF EXISTS "idx_bot_banned__telegra_915aca";
