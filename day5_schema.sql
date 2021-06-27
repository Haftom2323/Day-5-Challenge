CREATE TABLE IF NOT EXISTS `tweetinformation` 
(
    `id` INT NOT NULL AUTO_INCREMENT,
    `original_text` TEXT DEFAULT NULL,
    `polarity` FLOAT DEFAULT NULL,
    PRIMARY KEY (`id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci; 
