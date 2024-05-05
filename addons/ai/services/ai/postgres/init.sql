CREATE TABLE assistant_conversation (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE assistant_conversation_item (
    id SERIAL PRIMARY KEY,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author VARCHAR(255),
    context_window TEXT,
    message TEXT,
    model VARCHAR(255),
    lang VARCHAR(255),
    conversation_id INT REFERENCES assistant_conversation(id),
    personality VARCHAR(255),
    subject VARCHAR(255),
    subject_data JSON,
    command VARCHAR(255)
);