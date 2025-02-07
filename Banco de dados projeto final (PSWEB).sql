DROP DATABASE IF EXISTS ProfEduDB;
CREATE DATABASE ProfEduDB;
USE ProfEduDB;
CREATE TABLE Professores(
	id_professor INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	nome VARCHAR(200) NOT NULL,
	email VARCHAR(100) NOT NULL,
  	telefone VARCHAR(50) NOT NULL
); 
CREATE TABLE Competencias(
	id_competencia int primary key auto_increment, 
	descricao VARCHAR(100) NOT NULL
);
CREATE TABLE Professores_X_Competencias(
	id_professor INT NOT NULL,
  	id_competencia INT NOT NULL
);
CREATE TABLE Disciplinas(
	id_disciplina INT auto_increment PRIMARY KEY,
  	codigo VARCHAR(20) NOT NULL,
    	nome VARCHAR(50) NOT NULL,
    	CH CHAR(3) NOT NULL,
    	competencia_necessaria INT NOT NULL
);
CREATE TABLE Turmas(
	id INT PRIMARY KEY AUTO_INCREMENT,
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

ALTER TABLE Professores_X_Competencias
ADD CONSTRAINT fk_Professores_X_Competencias_Professores
FOREIGN KEY (id_professor) references Professores(id_professor);

ALTER TABLE Professores_X_Competencias
ADD CONSTRAINT fk_Professores_X_Competencia_Competencias
FOREIGN KEY (id_competencia) REFERENCES Competencias(id_competencia);

ALTER TABLE Disciplinas
ADD CONSTRAINT fk_CompetenciasXDisciplinas
FOREIGN KEY (competencia_necessaria) REFERENCES Competencias(id_competencia);

DELIMITER //

CREATE TRIGGER validar_competencia
BEFORE INSERT ON Turmas
FOR EACH ROW
BEGIN
    DECLARE competencia_professor INT;
    
    SELECT COUNT(*)
    INTO competencia_professor
    FROM Professores_X_Competencias
    WHERE id_professor = NEW.id_professor
    AND id_competencia = (SELECT competencia_necessaria FROM Disciplinas WHERE id_disciplina = NEW.id_disciplina);

    IF competencia_professor = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'O professor não possui a competência necessária para lecionar esta disciplina';
    END IF;
END;

//

DELIMITER ;
