-- upgrade --
ALTER TABLE "bot" ALTER COLUMN "token" TYPE VARCHAR(200) USING "token"::VARCHAR(200);
CREATE TABLE IF NOT EXISTS "_custom_meta_info" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" INT NOT NULL  DEFAULT 0
);;
INSERT INTO _custom_meta_info (id, version) VALUES (0, 0) ON CONFLICT DO NOTHING;
-- downgrade --
ALTER TABLE "bot" ALTER COLUMN "token" TYPE VARCHAR(50) USING "token"::VARCHAR(50);
DROP TABLE IF EXISTS "_custom_meta_info";
