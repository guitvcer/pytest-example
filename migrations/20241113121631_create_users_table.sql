-- migrate:up
CREATE TABLE if not exists users (
    id serial primary key not null,
    username varchar(32) not null,
    created_at timestamp with time zone not null
);

CREATE UNIQUE INDEX users_username_idx ON users (username);


-- migrate:down
DROP TABLE IF EXISTS users;
