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
-- Table structure for table `gen62_dinner`
--

CREATE TABLE IF NOT EXISTS `gen62_dinner` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `dinner` varchar(50) NOT NULL,
  `url` varchar(200) NOT NULL,
  `link` varchar(100) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `gen62_dinner`
--

INSERT INTO `gen62_dinner` (`ID`, `dinner`, `url`, `link`, `type`) VALUES
(1, 'Ristorante Il Porcino', 'http://s3-media3.fl.yelpcdn.com/bphoto/hXWfj_K7G4YCd33fMLWiTg/o.jpg', 'http://www.yelp.com/biz/ristorante-il-porcino-fremont-2', 'Italian'),
(2, 'Three Guys Pies', 'http://s3-media4.fl.yelpcdn.com/bphoto/OlcnlPnTntzLcmPEi5XnPQ/o.jpg', 'http://www.yelp.com/biz/three-guys-pies-fremont-2', 'Italian'),
(3, 'Massimo’s', 'http://s3-media4.fl.yelpcdn.com/bphoto/jEVK-WV1lZhqQruegzGaQw/o.jpg', 'http://www.yelp.com/biz/massimos-fremont', 'Italian'),
(4, 'Aniki’s Sushi', 'http://s3-media2.fl.yelpcdn.com/bphoto/iylTtNNp6xp7-jWBm5YMzA/o.jpg', 'http://www.yelp.com/biz/anikis-sushi-fremont', 'Japanese'),
(5, 'Satomi Sushi', 'http://s3-media4.fl.yelpcdn.com/bphoto/2_zbvjdYkhY9U6z1DZvA-Q/o.jpg', 'http://www.yelp.com/biz/satomi-sushi-fremont', 'Japanese'),
(6, 'Mioki Sushi', 'http://s3-media4.fl.yelpcdn.com/bphoto/KLReCnTscxl6t7wRvUUw1A/o.jpg', 'http://www.yelp.com/biz/mioki-sushi-fremont', 'Japanese'),
(7, 'The Kebab Shop', 'http://s3-media4.fl.yelpcdn.com/bphoto/cTqlUwgu9FBi8iM5-D8CXw/o.jpg', 'http://www.yelp.com/biz/the-kebab-shop-fremont-2', 'Greek'),
(8, 'Gyro Express', 'http://s3-media1.fl.yelpcdn.com/bphoto/h4FIR8zXxUkURUbmVu-0BQ/o.jpg', 'http://www.yelp.com/biz/gyro-express-fremont', 'Greek'),
(9, 'Zorba’s Deli Cafe and Catering', 'http://s3-media1.fl.yelpcdn.com/bphoto/X6-Qni9s1q2JOuJvWHL7IQ/o.jpg', 'http://www.yelp.com/biz/zorbas-deli-cafe-and-catering-fremont', 'Greek');
