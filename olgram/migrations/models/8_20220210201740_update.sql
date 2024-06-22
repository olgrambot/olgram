-- upgrade --
ALTER TABLE "defaultanswer" ADD "text" TEXT NOT NULL;
-- downgrade --
ALTER TABLE "defaultanswer" DROP COLUMN "text";
