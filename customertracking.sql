ET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_customer_tracking`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_custmers`
--

CREATE TABLE `tbl_custmers` (
  `customer_id` int(11) NOT NULL,
  `customer_name` varchar(255) NOT NULL,
  `customer_phoneNo` varchar(20) NOT NULL,
  `customer_address` varchar(50) NOT NULL,
  `customer_temperature` varchar(10) NOT NULL,
  `date` varchar(20) NOT NULL,
  `time` varchar(20) NOT NULL,
  `customer_image` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
