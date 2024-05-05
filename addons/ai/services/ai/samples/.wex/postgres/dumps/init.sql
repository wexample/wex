DROP TABLE IF EXISTS "assistant_conversation_item";
DROP TABLE IF EXISTS "assistant_conversation";
DROP TABLE IF EXISTS "user";

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE "assistant_conversation" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES "user"(id)
);

CREATE TABLE "assistant_conversation_item" (
    id SERIAL PRIMARY KEY,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author VARCHAR(255),
    context_window TEXT,
    message TEXT,
    model VARCHAR(255),
    lang VARCHAR(255),
    conversation_id INT REFERENCES "assistant_conversation"(id),
    personality VARCHAR(255),
    subject VARCHAR(255),
    subject_data JSON,
    command VARCHAR(255)
);
