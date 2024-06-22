-- upgrade --
ALTER TABLE "group_chat" ALTER COLUMN "chat_id" TYPE BIGINT USING "chat_id"::BIGINT;
ALTER TABLE "user" ALTER COLUMN "telegram_id" TYPE BIGINT USING "telegram_id"::BIGINT;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "telegram_id" TYPE INT USING "telegram_id"::INT;
ALTER TABLE "group_chat" ALTER COLUMN "chat_id" TYPE INT USING "chat_id"::INT;
