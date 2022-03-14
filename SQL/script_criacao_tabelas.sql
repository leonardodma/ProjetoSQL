-- -----------------------------------------------------
-- Schema mercado
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS mercado DEFAULT CHARACTER SET utf8 ;
USE mercado ;

-- -----------------------------------------------------
-- Table mercado.usuario
-- -----------------------------------------------------
DROP TABLE IF EXISTS mercado.usuario ;

CREATE TABLE IF NOT EXISTS mercado.usuario (
  id_usuario INT NOT NULL,
  nome VARCHAR(45) NOT NULL,
  cpf VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_usuario));


-- -----------------------------------------------------
-- Table mercado.produto
-- -----------------------------------------------------
DROP TABLE IF EXISTS mercado.produto ;

CREATE TABLE IF NOT EXISTS mercado.produto (
  id_produto INT NOT NULL,
  nome VARCHAR(45) NOT NULL,
  marca VARCHAR(45) NOT NULL,
  preco FLOAT NOT NULL,
  PRIMARY KEY (id_produto));


-- -----------------------------------------------------
-- Table mercado.ingrediente
-- -----------------------------------------------------
DROP TABLE IF EXISTS mercado.ingrediente ;

CREATE TABLE IF NOT EXISTS mercado.ingrediente (
  fk_id_produto INT NOT NULL,
  nome_ingrediente VARCHAR(45) NOT NULL,
  PRIMARY KEY (fk_id_produto, nome_ingrediente),
  CONSTRAINT fk_id_produto_ingrediente
    FOREIGN KEY (fk_id_produto)
    REFERENCES mercado.produto (id_produto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table mercado.lista_compra
-- -----------------------------------------------------
DROP TABLE IF EXISTS mercado.lista_compra ;

CREATE TABLE IF NOT EXISTS mercado.lista_compra (
  fk_id_usuario INT NOT NULL,
  fk_id_produto INT NOT NULL,
  PRIMARY KEY (fk_id_usuario, fk_id_produto),
  INDEX fk_id_produto_lista_idx (fk_id_produto ASC) VISIBLE,
  CONSTRAINT fk_id_usuario_lista
    FOREIGN KEY (fk_id_usuario)
    REFERENCES mercado.usuario (id_usuario)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_id_produto_lista
    FOREIGN KEY (fk_id_produto)
    REFERENCES mercado.produto (id_produto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
