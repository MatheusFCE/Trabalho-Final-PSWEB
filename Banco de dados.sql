DROP DATABASE IF EXISTS ProfEduDB;
CREATE DATABASE ProfEduDB;
USE ProfEduDB;
CREATE TABLE Professores(
	id_professor INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	nome VARCHAR(200) NOT NULL,
	email VARCHAR(100) NOT NULL UNIQUE,
  	telefone VARCHAR(50) NOT NULL UNIQUE
); 
CREATE TABLE Habilitacoes(
	id_habilitacao INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
	descricao VARCHAR(100) NOT NULL
);
CREATE TABLE Professores_X_Habilitacoes(
	id_professor INT NOT NULL,
  	id_habilitacao INT NOT NULL,
	PRIMARY KEY (id_professor, id_habilitacao)
);
CREATE TABLE Disciplinas(
	id_disciplina INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  	codigo VARCHAR(20) NOT NULL,
    	nome VARCHAR(50) NOT NULL,
    	CH CHAR(3) NOT NULL,
    	habilitacao_necessaria INT NOT NULL
);
CREATE TABLE Turmas(
	id_turma INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	id_professor INT NOT NULL,
    	id_disciplina INT NOT NULL,
    	ano YEAR NOT NULL, /*2024; 2025*/
    	periodo ENUM('1' , '2') NOT NULL,
    	horario ENUM('Manhã', 'Tarde', 'Noite') NOT NULL
);
ALTER TABLE Turmas
ADD CONSTRAINT fk_ProfessoresxTurmas
FOREIGN KEY (id_professor) REFERENCES Professores(id_professor);

ALTER TABLE Turmas
ADD CONSTRAINT fk_DisciplinasXTurmas
FOREIGN KEY (id_disciplina) REFERENCES Disciplinas(id_disciplina);

ALTER TABLE Professores_X_Habilitacoes
ADD CONSTRAINT fk_Professores_X_Habilitacoes_Professores
FOREIGN KEY (id_professor) references Professores(id_professor)
ON DELETE CASCADE;

ALTER TABLE Professores_X_Habilitacoes
ADD CONSTRAINT fk_Professores_X_Habilitacao_Habilitacoes
FOREIGN KEY (id_habilitacao) REFERENCES Habilitacoes(id_habilitacao)
ON DELETE CASCADE;

ALTER TABLE Disciplinas
ADD CONSTRAINT fk_HabilitacoesXDisciplinas
FOREIGN KEY (habilitacao_necessaria) REFERENCES Habilitacoes(id_habilitacao);

DELIMITER //

CREATE TRIGGER validar_habilitacao
BEFORE INSERT ON Turmas
FOR EACH ROW
BEGIN
    DECLARE habilitacao_professor INT;
    
    SELECT COUNT(*)
    INTO habilitacao_professor
    FROM Professores_X_Habilitacoes
    WHERE id_professor = NEW.id_professor
    AND id_habilitacao = (SELECT habilitacao_necessaria FROM Disciplinas WHERE id_disciplina = NEW.id_disciplina);

    IF habilitacao_professor = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'O professor não possui a habilitação necessária para lecionar esta disciplina';
    END IF;
END;

//

DELIMITER ;

INSERT INTO Habilitacoes(descricao)
VALUES  ('Matemática e Cálculo'),
	('Eletricidade e Eletrônica'),
        ('Computação e Programação'),
        ('Redes e Telecomunicações'),
        ('Comunicação de Dados e Sistemas'),
	('Ciências Humanas e Linguagem')
        
