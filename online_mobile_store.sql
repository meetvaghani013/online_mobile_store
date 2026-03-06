-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 06, 2026 at 06:05 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `online_mobile_store`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `product_name`, `price`, `qty`) VALUES
(26, 2, 6, 't4x', 41000, 1),
(27, 2, 3, 's25 ultra', 150000, 1),
(29, 2, 8, '17 pro', 172000, 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `tracking_id` varchar(100) DEFAULT NULL,
  `delivered_date` datetime DEFAULT NULL,
  `estimated_delivery` datetime DEFAULT NULL,
  `cancel_reason` text DEFAULT NULL,
  `cancel_date` datetime DEFAULT NULL,
  `return_reason` text DEFAULT NULL,
  `return_status` varchar(50) DEFAULT NULL,
  `return_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `customer_name`, `address`, `phone`, `payment_method`, `total`, `status`, `tracking_id`, `delivered_date`, `estimated_delivery`, `cancel_reason`, `cancel_date`, `return_reason`, `return_status`, `return_date`) VALUES
(25, 'user', 'adress', '0000000000', 'COD', 120000, 'Cancelled', 'TRK-3264B7A9', NULL, '2026-03-06 15:07:20', 'Changed mind', '2026-03-03 15:07:55', NULL, NULL, NULL),
(26, 'user', 'adress', '0000000000', 'COD', 172000, 'Return', 'TRK-24BF8BB1', '2026-03-03 15:13:16', '2026-03-06 15:07:43', NULL, NULL, 'Damaged product - return', 'Return Requested', '2026-03-03 15:19:51'),
(27, 'user', 'adress', '0000000000', 'COD', 56000, 'Delivered', 'TRK-B66DAA15', '2026-03-03 15:30:07', '2026-03-06 15:08:14', NULL, NULL, NULL, NULL, NULL),
(28, 'user', 'adress', '0000000000', 'COD', 150000, 'Cancelled', 'TRK-E0E6B734', NULL, '2026-03-06 15:08:30', 'Found cheaper elsewhere', '2026-03-03 15:30:13', NULL, NULL, NULL),
(29, 'user', 'adress', '0000000000', 'COD', 56000, 'Return', 'TRK-8F4F1FEB', '2026-03-03 15:29:49', '2026-03-06 15:29:05', NULL, NULL, 'Damaged product', 'Return Requested', '2026-03-05 12:30:53'),
(30, 'user', 'adress', '0000000000', 'COD', 40000, 'Delivered', 'TRK-D2F9DE1C', '2026-03-03 15:29:54', '2026-03-06 15:29:16', NULL, NULL, NULL, NULL, NULL),
(31, 'user', 'adress', '0000000000', 'COD', 150000, 'Cancelled', 'TRK-D9F63489', NULL, '2026-03-06 15:29:29', 'Changed mind', '2026-03-03 16:44:29', NULL, NULL, NULL),
(32, 'user', 'adress', '0000000000', 'COD', 150000, 'Ordered', 'TRK-C81AA0FA', NULL, '2026-03-06 15:29:31', NULL, NULL, NULL, NULL, NULL),
(33, 'user', 'adress', '0000000000', 'Card', 240000, 'Delivered', 'TRK-C27CBA05', '2026-03-06 09:54:22', '2026-03-08 10:10:51', NULL, NULL, NULL, NULL, NULL),
(34, 'user', 'adress', '0000000000', 'COD', 644000, 'Delivered', 'TRK-9CE506C9', '2026-03-06 10:02:59', '2026-03-09 10:02:14', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `product_brand` varchar(100) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_image` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_brand`, `product_name`, `price`, `qty`, `product_id`, `product_image`) VALUES
(1, 25, 'Google', 'pixel 10', 120000, 1, 5, 'images/9b45396d-1ff7-4676-9016-4ede91a01287_68eb28366c12b_google_pixel_10.jpg'),
(2, 26, 'i-phone', '17 pro', 172000, 1, 8, 'images/5b790fab-06df-4de0-81db-798bbdd49fdd_i_phone_17.jpg'),
(3, 27, 'Nothing', 'phone 1', 56000, 1, 7, 'images/814f4bdc-01a6-48bc-823c-74ae7ee532fc_68eb31c04402e_nothing_phone_1.webp'),
(4, 28, 'Samsung', 's25 ultra', 150000, 1, 3, 'images/dff5a175-94ab-4b26-8483-173eda1a52d4_68e9e127b1b7d_SamsungS25Ultra.jpg'),
(5, 29, 'Nothing', 'phone 1', 56000, 1, 7, 'images/814f4bdc-01a6-48bc-823c-74ae7ee532fc_68eb31c04402e_nothing_phone_1.webp'),
(6, 30, 'i-phone', '15', 40000, 1, 2, 'images/b46ab221-9d7e-42db-b71a-da84bd221f84_31vz6yNQ6L._SY300_SX300_QL70_FMwebp_.webp'),
(7, 31, 'Samsung', 's25 ultra', 150000, 1, 3, 'images/dff5a175-94ab-4b26-8483-173eda1a52d4_68e9e127b1b7d_SamsungS25Ultra.jpg'),
(8, 32, 'Samsung', 's25 ultra', 150000, 1, 3, 'images/dff5a175-94ab-4b26-8483-173eda1a52d4_68e9e127b1b7d_SamsungS25Ultra.jpg'),
(9, 33, 'Google', 'pixel 10', 120000, 2, 5, 'images/9b45396d-1ff7-4676-9016-4ede91a01287_68eb28366c12b_google_pixel_10.jpg'),
(10, 34, 'Google', 'pixel 10', 120000, 3, 5, 'images/9b45396d-1ff7-4676-9016-4ede91a01287_68eb28366c12b_google_pixel_10.jpg'),
(11, 34, 'i-phone', '17 pro', 172000, 1, 8, 'images/5b790fab-06df-4de0-81db-798bbdd49fdd_i_phone_17.jpg'),
(12, 34, 'Nothing', 'phone 1', 56000, 2, 7, 'images/814f4bdc-01a6-48bc-823c-74ae7ee532fc_68eb31c04402e_nothing_phone_1.webp');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `network` varchar(50) DEFAULT NULL,
  `sim_type` varchar(50) DEFAULT NULL,
  `display` varchar(50) DEFAULT NULL,
  `ram` varchar(50) DEFAULT NULL,
  `storage` varchar(50) DEFAULT NULL,
  `battery` varchar(50) DEFAULT NULL,
  `back_camera` varchar(100) DEFAULT NULL,
  `front_camera` varchar(100) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `about` text DEFAULT NULL,
  `image` varchar(300) DEFAULT NULL,
  `processor` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `brand`, `weight`, `color`, `network`, `sim_type`, `display`, `ram`, `storage`, `battery`, `back_camera`, `front_camera`, `price`, `quantity`, `about`, `image`, `processor`) VALUES
(2, '15', 'i-phone', 170, 'pink', '5G', 'Dual SIM', '6.8\"', '16GB', '512GB', '4500mAh', '8MP', '12MP', 40000, 5, 'primium pink color\r\n\r\n', 'images/b46ab221-9d7e-42db-b71a-da84bd221f84_31vz6yNQ6L._SY300_SX300_QL70_FMwebp_.webp', 'A17 Pro'),
(3, 's25 ultra', 'Samsung', 190, 'gray white', '5G', 'Dual SIM', '6.9\"', '16GB', '1TB', '5500mAh', '8MP', '16MP', 150000, 4, 'samsung lattest mbile in s series\r\n', 'images/dff5a175-94ab-4b26-8483-173eda1a52d4_68e9e127b1b7d_SamsungS25Ultra.jpg', 'Snapdragon 8+ Gen 1'),
(4, 'open', 'OnePlus', 290, 'dark red', '5G', 'Dual SIM', '6.9\"', '16GB', '1TB', '6000mAh', '8MP', '32MP', 170000, 4, 'one plus fold mobile', 'images/77b589bb-f1c3-4e87-9b6f-ce0f1d1c7151_68e8cbc21538d_OnePlusOpen1.jpg', 'Dimensity 8200'),
(5, 'pixel 10', 'Google', 200, 'sky blue', '5G', 'Dual SIM', '6.7\"', '16GB', '512GB', '5000mAh', '8MP', '32MP', 120000, 12, 'google pixel lattest mobile', 'images/9b45396d-1ff7-4676-9016-4ede91a01287_68eb28366c12b_google_pixel_10.jpg', 'Tensor G3'),
(6, 't4x', 'Vivo', 180, 'dark gray', '5G', 'Dual SIM', '6.7\"', '8GB', '256GB', '6000mAh', '8MP', '16MP', 41000, 5, 'vivo 5g mobile', 'images/3689a878-e79a-4dfa-8768-ba2228b9e429_68eb358ddcda5_vivo_t4x.webp', 'Dimensity 8200'),
(7, 'phone 1', 'Nothing', 190, 'orange', '5G', 'Dual SIM', '6.7\"', '8GB', '256GB', '5000mAh', '8MP', '16MP', 56000, 4, 'nothing phone 1\r\n', 'images/814f4bdc-01a6-48bc-823c-74ae7ee532fc_68eb31c04402e_nothing_phone_1.webp', 'Snapdragon 7 Gen 1'),
(8, '17 pro', 'i-phone', 256, 'orange', '5G', 'Dual SIM', '6.9\"', '16GB', '512GB', '4500mAh', '48MP', '16MP', 172000, 8, 'i phone latest piece', 'images/5b790fab-06df-4de0-81db-798bbdd49fdd_i_phone_17.jpg', 'A17 Pro');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `db_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `db_name`) VALUES
(1, 'meet', '1212', 'admin', 'meet_db'),
(68, 'user', '1212', 'user', 'user_db');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=194;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
