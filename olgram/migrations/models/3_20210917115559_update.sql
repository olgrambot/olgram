-- upgrade --
ALTER TABLE "group_chat" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
-- downgrade --
ALTER TABLE "group_chat" ALTER COLUMN "name" TYPE VARCHAR(50) USING "name"::VARCHAR(50);
