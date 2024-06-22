-- upgrade --
ALTER TABLE "bot" ADD "second_text" TEXT;
-- downgrade --
ALTER TABLE "bot" DROP COLUMN "second_text";
