-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 02, 2025 at 01:28 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `25vehicleparknumdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `amttb`
--

CREATE TABLE `amttb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `VehicleNo` varchar(250) NOT NULL,
  `Date` varchar(250) NOT NULL,
  `Amount` double(10,2) NOT NULL,
  `Status` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `amttb`
--


-- --------------------------------------------------------

--
-- Table structure for table `entrytb`
--

CREATE TABLE `entrytb` (
  `id` bigint(20) NOT NULL auto_increment,
  `VehicleNo` varchar(250) NOT NULL,
  `Date` varchar(250) NOT NULL,
  `InTime` time NOT NULL,
  `OutTime` time NOT NULL,
  `Status` varchar(250) NOT NULL,
  `ParkingNo` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `entrytb`
--

INSERT INTO `entrytb` (`id`, `VehicleNo`, `Date`, `InTime`, `OutTime`, `Status`, `ParkingNo`) VALUES
(1, '21BH2345AA', '02-Apr-2025', '18:56:02', '18:57:44', 'in', '1');

-- --------------------------------------------------------

--
-- Table structure for table `multitb`
--

CREATE TABLE `multitb` (
  `id` bigint(10) NOT NULL auto_increment,
  `VehicelNo` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `multitb`
--

INSERT INTO `multitb` (`id`, `VehicelNo`, `UserName`, `Mobile`, `Email`) VALUES
(1, '21BH2345AA', 'san', '9486365535', 'sangeeth5535@gmail.com'),
(2, '21BH2345AA', 'spacs', '9486365535', 'sangeeth5535@gmail.com'),
(3, '21BH2345AA', 'spacs', '9486365535', 'sangeeth5535@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `VehicleNo` varchar(50) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Amount` decimal(10,2) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Mobile`, `Email`, `VehicleNo`, `UserName`, `Password`, `Amount`) VALUES
(1, 'sangeeth Kumar', '9486365535', 'sangeeth5535@gmail.com', '21BH2345AA', 'san', 'san', '0.00');

-- --------------------------------------------------------

--
-- Table structure for table `temptb`
--

CREATE TABLE `temptb` (
  `id` int(10) NOT NULL auto_increment,
  `uname` varchar(250) NOT NULL,
  `VehicleNo` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `temptb`
--

INSERT INTO `temptb` (`id`, `uname`, `VehicleNo`, `Mobile`, `Email`) VALUES
(1, 'spacs', '21BH2345AA', '9486365535', 'sangeeth5535@gmail.com');
