-- upgrade --
ALTER TABLE "bot" ADD "enable_antiflood" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "bot" DROP COLUMN "enable_antiflood";
