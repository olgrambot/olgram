-- upgrade --
ALTER TABLE "bot" ADD "outgoing_messages_count" BIGINT NOT NULL  DEFAULT 0;
ALTER TABLE "bot" ADD "incoming_messages_count" BIGINT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "bot" DROP COLUMN "outgoing_messages_count";
ALTER TABLE "bot" DROP COLUMN "incoming_messages_count";
