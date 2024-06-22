-- upgrade --
CREATE TABLE IF NOT EXISTS "group_chat" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chat_id" INT NOT NULL UNIQUE,
    "name" VARCHAR(50) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_group_chat_chat_id_5da32d" ON "group_chat" ("chat_id");
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_id" INT NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS "idx_user_telegra_66ffbd" ON "user" ("telegram_id");
CREATE TABLE IF NOT EXISTS "bot" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(50) NOT NULL UNIQUE,
    "name" VARCHAR(33) NOT NULL,
    "code" UUID NOT NULL,
    "start_text" TEXT NOT NULL,
    "group_chat_id" INT REFERENCES "group_chat" ("id") ON DELETE CASCADE,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_bot_code_a43015" ON "bot" ("code");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "bot_group_chat" (
    "bot_id" INT NOT NULL REFERENCES "bot" ("id") ON DELETE CASCADE,
    "groupchat_id" INT NOT NULL REFERENCES "group_chat" ("id") ON DELETE CASCADE
);
