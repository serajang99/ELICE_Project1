-- 책 정보 테이블
CREATE TABLE `elice_library`.`book` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(100) NOT NULL,
    `publisher` VARCHAR(100) NOT NULL,
    `author` VARCHAR(100) NOT NULL,
    `publication_date` VARCHAR(20) NOT NULL,
    `pages` INT NOT NULL,
    `isbn` VARCHAR(20) NOT NULL,
    `description` TEXT NOT NULL,
    `link` TEXT NOT NULL,
    `img` VARCHAR(100) NOT NULL,
    `stock` INT NOT NULL DEFAULT 5,
    `star` INT NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);

-- 유저 정보 테이블 
CREATE TABLE `elice_library`.`user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `password` TEXT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `username_UNIQUE` (`username` ASC)
);

-- 책 대여기록 테이블
CREATE TABLE `elice_library`.`bookRental` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `rental_date` DATETIME NOT NULL,
    `user_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    PRIMARY KEY (`id`,`user_id`, `rental_date`),
    FOREIGN KEY (`user_id`) REFERENCES user (`id`),
    FOREIGN KEY (`book_id`) REFERENCES book (`id`)
);

-- 책 리뷰 테이블
CREATE TABLE `elice_library`.`bookReview` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `comment_date` DATETIME NOT NULL,
    `user_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    `comment` TEXT NOT NULL,
    `star` INT NOT NULL,
    PRIMARY KEY (`id`,`user_id`, `comment_date`),
    FOREIGN KEY (`user_id`) REFERENCES user (`id`),
    FOREIGN KEY (`book_id`) REFERENCES book (`id`)
);