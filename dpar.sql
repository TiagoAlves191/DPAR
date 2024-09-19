-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 05-Maio-2024 às 20:29
-- Versão do servidor: 10.4.27-MariaDB
-- versão do PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `dpar`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `gestores`
--

CREATE TABLE `gestores` (
  `Nome` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL,
  `Nr_Gestor` int(11) NOT NULL,
  `Estado` tinyint(1) NOT NULL,
  `Contacto` varchar(14) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `gestores`
--

INSERT INTO `gestores` (`Nome`, `Nr_Gestor`, `Estado`, `Contacto`) VALUES
('Tiago Alves', 1, 1, '+351 937993286'),
('Pedro', 2, 0, '0'),
('Alexandre', 3, 1, '+351 936058385'),
('Henrique', 4, 1, '+351 925940101');

-- --------------------------------------------------------

--
-- Estrutura da tabela `login`
--

CREATE TABLE `login` (
  `Nr_Gestor` int(11) NOT NULL,
  `username` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `password` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `login`
--

INSERT INTO `login` (`Nr_Gestor`, `username`, `password`) VALUES
(3, 'alex', 'alex'),
(4, 'henrique', 'henrique'),
(2, 'pedro', 'pedro'),
(1, 'Tiago', 'tiago');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `gestores`
--
ALTER TABLE `gestores`
  ADD PRIMARY KEY (`Nr_Gestor`);

--
-- Índices para tabela `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`username`),
  ADD KEY `Nr_Gestor` (`Nr_Gestor`);

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `login`
--
ALTER TABLE `login`
  ADD CONSTRAINT `login_ibfk_1` FOREIGN KEY (`Nr_Gestor`) REFERENCES `gestores` (`Nr_Gestor`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
