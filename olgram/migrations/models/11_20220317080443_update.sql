-- upgrade --
ALTER TABLE "bot" ADD "enable_additional_info" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "bot" DROP COLUMN "enable_additional_info";
