CREATE DATABASE ProfEduDB;
USE ProfEduDB;
CREATE TABLE Professores(
	id_professor INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	matricula INT NOT NULL,
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
    CH INT(3) NOT NULL,
    competencia_necessaria INT NOT NULL
);
CREATE TABLE Turmas(
	id INT PRIMARY KEY AUTO_INCREMENT,
	id_professor INT NOT NULL,
    id_disciplina INT NOT NULL,
    ano INT(4) NOT NULL, /*2024; 2025*/
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

INSERT INTO Professores(matricula, nome, email, telefone)
VALUES  ( 1050808, 'ANTONIO DE BARROS SERRA', 'anserra@ifce.edu.br', '(85) 9234-5678'),
		( 508080, 'ANTONIO WENDELL DE OLIVEIRA RODRIGUES', 'wendell@ifce.edu.br', '(85) 9791-2345'),
        ( 907727, 'FABIO ALENCAR MENDONÇA', 'fabio@ifce.edu.br', '(85) 2800-4177');
        
INSERT INTO Competencias(descricao) 
VALUES  ('PROJETO DE SISTEMAS WEB'),
		('SISTEMAS DE RÁDIO ENLACE');       
        
INSERT INTO Professores_X_Competencias(id_professor, id_competencia)
VALUES  (1,1),
		(3,2);
        
INSERT INTO Disciplinas(codigo, nome, CH, competencia_necessaria)
VALUES ('SRE', 'SISTEMAS DE RÁDIO ENLACE', '80', 2);

INSERT INTO Turmas(id_professor, id_disciplina, ano, periodo, horario)
VALUES (3, 1, '2025', 2, 'Manhã');