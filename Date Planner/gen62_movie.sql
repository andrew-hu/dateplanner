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
-- Table structure for table `gen62_movie`
--

CREATE TABLE IF NOT EXISTS `gen62_movie` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `movie` varchar(50) NOT NULL,
  `url` varchar(100) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `gen62_movie`
--

INSERT INTO `gen62_movie` (`ID`, `movie`, `url`, `type`) VALUES
(1, 'The Avengers', 'http://t0.gstatic.com/images?q=tbn:ANd9GcRlGeugacRkKznDOtRhUCVt0AkrOTPbaaKwF9xgGZgNViyC_Xko', 'Superhero'),
(2, 'Mad Max', 'http://t0.gstatic.com/images?q=tbn:ANd9GcQuK41mExh1Qv3kbXoxohWYGlcstOQ6zEnnNdSI2BGIKywQwgRI', 'Sci-Fi'),
(3, 'Tomorrowland', 'http://t3.gstatic.com/images?q=tbn:ANd9GcSQ_0W7gaPpHYi7l5Y1pPKD2rpnSuo_z89Cz7f4pWMBatdMKqy7', 'Fantasy'),
(4, 'Furious 7', 'http://t1.gstatic.com/images?q=tbn:ANd9GcReedjA2vJSO4_6GDpsI3PShvbRqfAAEv03qaJ9qOxtiLZX0Jx7', 'Thriller'),
(5, 'Ex Machina', 'http://t3.gstatic.com/images?q=tbn:ANd9GcQe8L-1PTMlUf-si2Oy6BTd9ZtbWH7BSRSF5k5JGNATxOHzyIdg', 'Sci-Fi'),
(6, 'Kingsman: Secret Service', 'http://t3.gstatic.com/images?q=tbn:ANd9GcTn2E6bqcLehK92h215qFnUpCYFqt02Iuwg-N4gVBmixzAXvGfZ', 'Action');
