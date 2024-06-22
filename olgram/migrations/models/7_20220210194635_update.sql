-- upgrade --
CREATE TABLE IF NOT EXISTS "defaultanswer" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "bot_id" INT NOT NULL REFERENCES "bot" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "defaultanswer";
