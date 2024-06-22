-- upgrade --
ALTER TABLE "bot" ADD "enable_olgram_text" BOOL NOT NULL  DEFAULT True;
-- downgrade --
ALTER TABLE "bot" DROP COLUMN "enable_olgram_text";
