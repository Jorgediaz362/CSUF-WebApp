USE titanconnect;

CREATE TABLE `users` (
  	`username` varchar(255) NOT NULL,
  	`email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    UNIQUE INDEX user_name_unique (email),
    PRIMARY KEY (`email`)
);

/* Category for related posts */
CREATE TABLE `categories` (
	`cat_id` INT(8) NOT NULL AUTO_INCREMENT,
    `cat_name` VARCHAR(255) NOT NULL,
    `cat_description` VARCHAR(255) NOT NULL,
    UNIQUE INDEX cat_title_unique (cat_name),
    PRIMARY KEY (`cat_id`)
);

CREATE TABLE `topics` (
	`topic_id` INT(8) NOT NULL AUTO_INCREMENT,
    `topic_subject` VARCHAR(255) NOT NULL,
    `topic_date` DATETIME NOT NULL,
    `topic_cat` INT(8) NOT NULL,
    `topic_by` INT(8) NOT NULL,
    PRIMARY KEY (`topic_id`)
);

CREATE TABLE `posts` (
  	`post_id` INT(8) NOT NULL AUTO_INCREMENT,
    `post_content` TEXT NOT NULL,
    `post_date` DATETIME NOT NULL,
    `post_topic` INT(8) NOT NULL,
  	`post_by` INT(8) NOT NULL,
    PRIMARY KEY (`post_id`)
);

/*Link topics to categories, topics to users, posts to topics, posts to user*/
ALTER TABLE topics ADD FOREIGN KEY(topic_cat) REFERENCES categories(cat_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE topics ADD FOREIGN KEY(topic_by) REFERENCES users(email) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE posts ADD FOREIGN KEY(post_topic) REFERENCES topics(topic_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE posts ADD FOREIGN KEY(post_by) REFERENCES users(email) ON DELETE RESTRICT ON UPDATE CASCADE;
