-- phpMyAdmin SQL Dump
-- version 3.3.7deb7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 21, 2015 at 02:43 PM
-- Server version: 5.1.73
-- PHP Version: 5.3.3-7+squeeze19

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `perl_test`
--

-- --------------------------------------------------------

--
-- Table structure for table `gen62_events`
--

CREATE TABLE IF NOT EXISTS `gen62_events` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(50) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `desc` varchar(500) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `gen62_events`
--

INSERT INTO `gen62_events` (`ID`, `event`, `url`, `desc`) VALUES
(1, 'take a stroll in the park', 'https://makeeatsimple.files.wordpress.com/2013/10/autumn-afternoon-in-park-paris.jpg', 'When the weather is warm, exploring the great outdoors can be a great way to spend time with your date. It''s free and simple; its perfect for a date! '),
(2, 'go hiking', 'http://www.lakearrowhead.com/img/hiking/hikers3.jpg', 'If you''re feeling very ambitious, you can hike up your nearest peak or mountain area to see the sunrise or sunset! Going hiking is the perfect opportunity to bring along picnic items you can enhance your outing with. How does a glass of wine or champagne under the clear evening sky sound? '),
(3, 'go fishing', 'http://katelynjamesblog.com/wp-content/uploads/2013/10/fishing-engagement-shoot_0104.jpg', 'It''s just you, your date, and the calm of the open water. You don''t have to catch anything for it to be a great date, bring along some snack items and have a relaxing evening with your significant other!'),
(4, 'visit the library', 'http://www.thedatereport.com/dating/wp-content/gallery/top-20-first-dates-youve-never-tried/7-cheap-date-ideas550423735-aug-31-2012-1-600x400.jpg', 'Not what you''d expect for a date idea, is it? Everyone loves a good story, and a trip to the library can help you and your partner share the ones you love with each other. Whether it''s fantasy, sci-fi, mystery, or romance: this place has got it all!'),
(5, 'go window shopping', 'http://www.bararch.com/system/uploads/project_image/image/945/santana-row-plaza.jpg', 'Sometimes window shopping can be just as exhilarating and fun as actual shopping. Have a blast going from store to store trying on clothes and playing with toys with your date. If your adventuring makes you hungry, stop by a nearby cafe to refresh!'),
(6, 'go to a theme park', 'http://upload.wikimedia.org/wikipedia/commons/b/be/Invertigo_At_Great_America.jpg', 'Theme parks are filled with fun rides, mini-games to win stuffed animals and toys, and delicious food. Nothing says romance like cotton candy, right?'),
(7, 'go to the beach', 'http://images.fineartamerica.com/images-medium-large/panther-beach--santa-cruz-county-brendan-reals.jpg', 'If you''re willing to make the drive, Santa Cruz and San Francisco have beautiful views on their many beaches. Take a walk down the shore with your date and maybe go for a dip in the ocean if the weather is permitting. Come on in, the water''s fine!'),
(8, 'visit the zoo', 'http://www.theherbstfoundation.org/wp/wp-content/uploads/2013/04/san-francisco-zoo-sign-21-540x335.jpg', 'Is your date an animal lover? If so, a trip to the San Francisco Zoo seems perfect. Explore natures many wonders from the curious monkeys to the lazy rhinos to the majestic lions. The zoo is a great place to relive one of the best childhood experiences... also, a plethora of animals means a bunch of room for conversation!');
