-- CREATE DATABASE codejam CHARACTER SET utf8 COLLATE utf8_bin;

DROP TABLES answers, problems, users;

CREATE TABLE users (
    id   int unsigned   NOT NULL AUTO_INCREMENT,
    name varchar(64)    NOT NULL,
    country varchar(64) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY  (name)
);


CREATE TABLE problems (
    id   bigint unsigned NOT NULL, -- use codejam id
    name varchar(256)    NOT NULL,
    type varchar(256), -- fill this later by researcher -- might be multiple attr
    PRIMARY KEY (id)
);


CREATE TABLE answers (
    id            int unsigned    NOT NULL AUTO_INCREMENT,
    user_id       int unsigned    NOT NULL,
    problem_id    bigint unsigned NOT NULL,
    hardness      int unsigned    NOT NULL,
    attempts      int unsigned    NOT NULL,
    lang          varchar(64),   -- make it later
    submit_time   int unsigned,  -- allow null, in case code not pass
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)    REFERENCES users (id),
    FOREIGN KEY (problem_id) REFERENCES problems (id)
);
