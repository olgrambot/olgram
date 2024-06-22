-- upgrade --
ALTER TABLE "bot" ADD "enable_threads" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "bot" DROP COLUMN "enable_threads";
