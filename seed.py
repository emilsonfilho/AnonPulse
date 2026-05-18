import asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.core.database import engine
from app.core.enums import MessageType

from app.models.professor import Professor
from app.models.monitor import Monitor
from app.models.subject import Subject
from app.models.classroom import Classroom
from app.models.student import Student
from app.models.monitor_assignment import MonitorAssignment
from app.models.feedback_type import FeedbackType
from app.models.enrollment import Enrollment
from app.models.feedback import Feedback
from app.models.document import Document

from app.services.hash_service import HashService, HashAlgorithm

async def seed_data():
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        try:
            print("A iniciar a carga de dados...")

            print("Limpando dados antigos para evitar conflitos de chave única...")
            await session.execute(delete(Feedback))
            await session.execute(delete(Document))
            await session.execute(delete(Enrollment))
            await session.execute(delete(MonitorAssignment))
            await session.execute(delete(Classroom))
            await session.execute(delete(Monitor))
            await session.execute(delete(Student))
            await session.execute(delete(Professor))
            await session.execute(delete(Subject))
            await session.execute(delete(FeedbackType))
            await session.commit()

            print("A inserir Tipos de Feedback...")
            tipos_feedback = [
                FeedbackType(type=MessageType.ELOGIO),
                FeedbackType(type=MessageType.CRITICA),
                FeedbackType(type=MessageType.SUGESTAO),
                FeedbackType(type=MessageType.DUVIDA),
            ]
            session.add_all(tipos_feedback)
            await session.flush()

            print("Inserindo professores...")
            professores = [
                Professor(
                    name="ARTHUR RODRIGUES ARARUNA",
                    email="ararunaufc@gmail.com"
                ),
                Professor(
                    name="ARTHUR RODRIGUES ARARUNA",
                    email="qxd@araruna.prof"
                ),
                Professor(
                    name="ATILIO GOMES LUIZ",
                    email="gomes.atilio@gmail.com"
                ),
                Professor(
                    name="CARLOS ROBERTO RODRIGUES FILHO",
                    email="filho.rodrigues@ufc.br"
                ),
                Professor(
                    name="CLARO HENRIQUE SILVA SALES",
                    email="clarosales@ufc.br"
                ),
                Professor(
                    name="DAVID SENA OLIVEIRA",
                    email="sena.ufc@gmail.com"
                ),
                Professor(
                    name="FABIO CARLOS SOUSA DIAS",
                    email="fabiodias@ufc.br"
                ),
                Professor(
                    name="MARCELO MARTINS DA SILVA",
                    email="martins2016eng@gmail.com"
                ),
                Professor(
                    name="MARCIO ESPINDOLA FREIRE MAIA",
                    email="marcioefmaia@gmail.com"
                ),
                Professor(
                    name="MARCOS ANTONIO DE OLIVEIRA",
                    email="marcos.oliveira@ufc.br"
                ),
                Professor(
                    name="PAULO HENRIQUE MACEDO DE ARAUJO",
                    email="phmacedoaraujo@ufc.br"
                ),
                Professor(
                    name="RICARDO REIS PEREIRA",
                    email="ricardoreispereira@gmail.com"
                ),
                Professor(
                    name="RUBENS FERNANDES NUNES",
                    email="rubensfn@gmail.com"
                ),
                Professor(
                    name="SIDARTHA AZEVEDO LOBO DE CARVALHO",
                    email="sidartha@ufc.br"
                ),
                Professor(
                    name="VICTOR AGUIAR EVANGELISTA DE FARIAS",
                    email="victor.aefarias@gmail.com"
                ),
                Professor(
                    name="BRUNO MATHEUS GÓIS",
                    email="brunomateus@gmail.com"
                ),
            ]
            session.add_all(professores)
            await session.flush()

            print("Inserindo Monitores...")
            monitores = [
                Monitor(
                    registration="564925",
                    name="Ana Amélia de Sousa Santos",
                    email="anaameliatdj@gmail.com"
                ),
                Monitor(
                    registration="565321",
                    name="Iago de Oliveira Lô",
                    email="iagooliveiralo070@gmail.com"
                ),
                Monitor(
                    registration="567157",
                    name="Denilso Bernardo Nunes da Silva",
                    email="nilsonde@alu.ufc.br"
                ),
                Monitor(
                    registration="568334",
                    name="Weryck Lemos Silva",
                    email="weryck.lemos@alu.ufc.br"
                ),
                Monitor(
                    registration="581924",
                    name="João David B. de Araújo",
                    email="davidbramsiga@gmail.com"
                ),
                Monitor(
                    registration="579703",
                    name="Hanna Lavine Lima Chaves",
                    email="hannalavine@alu.ufc.br"
                ),
                Monitor(
                    registration="564976",
                    name="Alana Maria Sousa Augusto",
                    email="alana.augusto@alu.ufc.br"
                ),
                Monitor(
                    registration="586077",
                    name="Maria Vitória de Almeida Ferreira",
                    email="mariavito@alu.ufc.br"
                ),
                Monitor(
                    registration="581908",
                    name="Matheus de Sousa Mendes",
                    email="matheussousamendes81@gmail.com"
                ),
                Monitor(
                    registration="579705",
                    name="Cesário Porto Magalhães Filho",
                    email="cesario.0324@alu.ufc.br"
                ),
                Monitor(
                    registration="581895",
                    name="Matheus Eugênio Granja",
                    email="matheuseugenioo@alu.ufc.br"
                ),
                Monitor(
                    registration="565805",
                    name="Francisco Emilson Santos Souza Filho",
                    email="emilsonfilhocontato@gmail.com"
                ),
                Monitor(
                    registration="566245",
                    name="Heitor Pimenta Gotz",
                    email="heitor.gotz@alu.ufc.br"
                ),
                Monitor(
                    registration="567579",
                    name="Pedro Edson Maciel de Araújo",
                    email="pedroedsonmaciel@alu.ufc.br"
                ),
                Monitor(
                    registration="571600",
                    name="Carla Cristina Sousa Araújo",
                    email="carlacristinasousasaraujo@alu.ufc.br"
                ),
                Monitor(
                    registration="582749",
                    name="Luiz Guilherme Cavalcante Martins",
                    email="luiz.gcm@alu.ufc.br"
                ),
                Monitor(
                    registration="579925",
                    name="Vicente de Paulo da Silva Neto",
                    email="vicentesilva@alu.ufc.br"
                ),
                Monitor(
                    registration="582392",
                    name="Jordan Pinheiro Mesquita",
                    email="jordanpinheiro@alu.ufc.br"
                ),
                Monitor(
                    registration="581559",
                    name="Carlos Rodrigues Nobre",
                    email="carlosrodrigues23@alu.ufc.br"
                ),
                Monitor(
                    registration="581946",
                    name="José Luis Souza Arruda Rodrigues",
                    email="joseluis12@alu.ufc.br"
                ),
                Monitor(
                    registration="580650",
                    name="João Eudes Campos Colares Neto",
                    email="jeudescolares@alu.ufc.br"
                ),
                Monitor(
                    registration="583190",
                    name="Daniel Andrade Siqueira",
                    email="danielandrade070@alu.ufc.br"
                ),
                Monitor(
                    registration="582243",
                    name="João Filipe Fonseca de Oliveira",
                    email="joaofilipefonseca@alu.ufc.br"
                ),
                Monitor(
                    registration="580840",
                    name="Antônio Pompeu de Araújo Neto",
                    email="pompeuaraujo512@gmail.com"
                ),
                Monitor(
                    registration="542056",
                    name="Mário Martins Aragão",
                    email="marioaragao@alu.ufc.br"
                ),
                Monitor(
                    registration="579284",
                    name="João Eduardo Rabelo de Medeiros",
                    email="joaoeduardo@alu.ufc.br"
                ),
                Monitor(
                    registration="590065",
                    name="Daniel Fernandes Ferreira",
                    email="danielfernandesmb11@gmail.com"
                ),
            ]
            session.add_all(monitores)
            await session.flush()

            print("Inserindo disciplinas...")
            disciplinas = [
                Subject(
                    cod="QXD0001",
                    name="Fundamentos de Programação"
                ),
                Subject(
                    cod="QXD0007",
                    name="Programação Orientada a Objetos"
                ),
                Subject(
                    cod="QXD0010",
                    name="Estrutura de Dados"
                ),
                Subject(
                    cod="QXD0115",
                    name="Estrutura de Dados Avançada"
                ),
            ]
            session.add_all(disciplinas)
            await session.flush()
            
            print("Inserindo professores faltantes das turmas...")
            professores_faltantes = [
                Professor(
                    name="ENYO JOSE TAVARES GONCALVES",
                    email="enyo.goncalves@ufc.br"
                ),
                Professor(
                    name="ALEXANDRE MATOS ARRUDA",
                    email="alexandre.matos@ufc.br"
                ),
                Professor(
                    name="WAGNER GUIMARAES AL ALAM",
                    email="wagner.alalam@ufc.br"
                ),
            ]
            session.add_all(professores_faltantes)
            professores.extend(professores_faltantes)

            await session.flush()

            professor_por_email = {
                professor.email: professor
                for professor in professores
            }

            professor_arthur = professor_por_email["ararunaufc@gmail.com"]
            professor_atilio = professor_por_email["gomes.atilio@gmail.com"]
            professor_claro = professor_por_email["clarosales@ufc.br"]
            professor_david = professor_por_email["sena.ufc@gmail.com"]
            professor_rubens = professor_por_email["rubensfn@gmail.com"]
            professor_sidartha = professor_por_email["sidartha@ufc.br"]
            professor_bruno = professor_por_email["brunomateus@gmail.com"]
            professor_enyo = professor_por_email["enyo.goncalves@ufc.br"]
            professor_alexandre = professor_por_email["alexandre.matos@ufc.br"]
            professor_wagner = professor_por_email["wagner.alalam@ufc.br"]

            print("Inserindo turmas...")
            turmas = [
                Classroom(
                    cod="FUP-RC-08A",
                    subject_cod="QXD0001",
                    professor_id=professor_enyo.id
                ),
                Classroom(
                    cod="FUP-RC-09A",
                    subject_cod="QXD0001",
                    professor_id=professor_claro.id
                ),
                Classroom(
                    cod="FUP-SI-04A",
                    subject_cod="QXD0001",
                    professor_id=professor_alexandre.id
                ),
                Classroom(
                    cod="FUP-SI-05A",
                    subject_cod="QXD0001",
                    professor_id=professor_arthur.id
                ),
                Classroom(
                    cod="FUP-CC-01A",
                    subject_cod="QXD0001",
                    professor_id=professor_david.id
                ),
                Classroom(
                    cod="FUP-CC-02A",
                    subject_cod="QXD0001",
                    professor_id=professor_alexandre.id
                ),
                Classroom(
                    cod="FUP-IA-03A",
                    subject_cod="QXD0001",
                    professor_id=professor_alexandre.id
                ),
                Classroom(
                    cod="FUP-IA-10A",
                    subject_cod="QXD0001",
                    professor_id=professor_sidartha.id
                ),
                Classroom(
                    cod="FUP-EC-11A",
                    subject_cod="QXD0001",
                    professor_id=professor_rubens.id
                ),
                Classroom(
                    cod="FUP-EC-12A",
                    subject_cod="QXD0001",
                    professor_id=professor_claro.id
                ),
                Classroom(
                    cod="FUP-ES-06A",
                    subject_cod="QXD0001",
                    professor_id=professor_rubens.id
                ),
                Classroom(
                    cod="FUP-ES-07A",
                    subject_cod="QXD0001",
                    professor_id=professor_claro.id
                ),
                Classroom(
                    cod="FUP-DD-01A",
                    subject_cod="QXD0001",
                    professor_id=professor_david.id
                ),
                Classroom(
                    cod="FUP-DD-02A",
                    subject_cod="QXD0001",
                    professor_id=professor_bruno.id
                ),
                Classroom(
                    cod="POO-01A",
                    subject_cod="QXD0007",
                    professor_id=professor_wagner.id
                ),
                Classroom(
                    cod="POO-02A",
                    subject_cod="QXD0007",
                    professor_id=professor_wagner.id
                ),
                Classroom(
                    cod="ED-SI-01A",
                    subject_cod="QXD0010",
                    professor_id=professor_david.id
                ),
                Classroom(
                    cod="ED-SI-04A",
                    subject_cod="QXD0010",
                    professor_id=professor_arthur.id
                ),
                Classroom(
                    cod="ED-ES-02A",
                    subject_cod="QXD0010",
                    professor_id=professor_david.id
                ),
                Classroom(
                    cod="ED-ES-05A",
                    subject_cod="QXD0010",
                    professor_id=professor_arthur.id
                ),
                Classroom(
                    cod="ED-RC-03A",
                    subject_cod="QXD0010",
                    professor_id=professor_wagner.id
                ),
                Classroom(
                    cod="EDA-CC-01A",
                    subject_cod="QXD0115",
                    professor_id=professor_atilio.id
                ),
            ]
            session.add_all(turmas)
            await session.flush()

            print("Inserindo alocações dos monitores...")
            alocacoes_monitores = [
                # Carlos Rodrigues Nobre - FUP RC 08A - Bloco 3 - Lab 7 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="581559",
                    classroom_cod="FUP-RC-08A"
                ),
                # Ana Amélia de Sousa Santos - FUP RC 08A - Bloco 3 - Lab 7 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="564925",
                    classroom_cod="FUP-RC-08A"
                ),

                # José Luis Souza Arruda Rodrigues - FUP RC 09A - Bloco 1 - Lab 3 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="581946",
                    classroom_cod="FUP-RC-09A"
                ),
                # Matheus de Sousa Mendes - FUP RC 09A - Bloco 1 - Lab 3 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="581908",
                    classroom_cod="FUP-RC-09A"
                ),

                # Weryck Lemos Silva - FUP SI 04A - Bloco 4 - Lab 2 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="568334",
                    classroom_cod="FUP-SI-04A"
                ),

                # Vicente de Paulo da Silva Neto - FUP SI 05A - Bloco 1 - Lab 4 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="579925",
                    classroom_cod="FUP-SI-05A"
                ),

                # Daniel Andrade Siqueira - FUP CC 01A - Bloco 3 - Lab 6 - go
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="583190",
                    classroom_cod="FUP-CC-01A"
                ),
                # Jordan Pinheiro Mesquita - FUP CC 01A - Bloco 3 - Lab 6 - go
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="582392",
                    classroom_cod="FUP-CC-01A"
                ),

                # Maria Vitória de Almeida Ferreira - FUP CC 02A - Bloco 3 - Lab 7 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="586077",
                    classroom_cod="FUP-CC-02A"
                ),
                # Antônio Pompeu de Araújo Neto - FUP CC 02A - Bloco 3 - Lab 7 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="580840",
                    classroom_cod="FUP-CC-02A"
                ),

                # Iago de Oliveira Lô - FUP IA 03A - Bloco 3 - Lab 6 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="565321",
                    classroom_cod="FUP-IA-03A"
                ),

                # Denilso Bernardo Nunes da Silva - FUP IA 10A - Bloco 4 - Lab 5 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="567157",
                    classroom_cod="FUP-IA-10A"
                ),

                # Pedro Edson Maciel de Araújo - FUP EC 11A - Bloco 1 - Lab 4 - C/C++
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="567579",
                    classroom_cod="FUP-EC-11A"
                ),

                # Matheus Eugênio Granja - FUP EC 12A - Bloco 1 - Lab 3 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="581895",
                    classroom_cod="FUP-EC-12A"
                ),

                # Hanna Lavine Lima Chaves - FUP ES 06A - Bloco 1 - Lab 4 - c++
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="579703",
                    classroom_cod="FUP-ES-06A"
                ),
                # Luiz Guilherme Cavalcante Martins - FUP ES 06A - Bloco 1 - Lab 4 - c++
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="582749",
                    classroom_cod="FUP-ES-06A"
                ),

                # João David B. de Araújo / Brandão - FUP ES 07A - Bloco 1 - Lab 3 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="581924",
                    classroom_cod="FUP-ES-07A"
                ),
                # João Eudes Campos Colares Neto - FUP ES 07A - Bloco 1 - Lab 3 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="580650",
                    classroom_cod="FUP-ES-07A"
                ),

                # Hanna Lavine Lima Chaves - FUP DD 01A - Bloco 3 - Lab 7 - go
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="579703",
                    classroom_cod="FUP-DD-01A"
                ),
                # Daniel Fernandes Ferreira - FUP DD 01A - Bloco 3 - Lab 7 - go
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="590065",
                    classroom_cod="FUP-DD-01A"
                ),

                # Cesário Porto Magalhães Filho - FUP DD 02A - Bloco 3 - Lab 6 - go
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="579705",
                    classroom_cod="FUP-DD-02A"
                ),

                # Alana Maria Sousa Augusto - POO 01A - Bloco 4 - Lab 5 - java
                # Alocação aleatória, pois a linha estava sem monitor na imagem.
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="564976",
                    classroom_cod="POO-01A"
                ),

                # Carla Cristina Sousa Araújo - POO 02A - Bloco 3 - Lab 7 - java
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="571600",
                    classroom_cod="POO-02A"
                ),

                # Weryck Lemos Silva - ED SI 01A - Bloco 4 - Lab 5 - go
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="568334",
                    classroom_cod="ED-SI-01A"
                ),

                # João Filipe Fonseca de Oliveira - ED SI 04A - Seg B1Lab 2 / Ter B1S1 - java
                # Alocação aleatória, pois a linha estava sem monitor na imagem.
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="582243",
                    classroom_cod="ED-SI-04A"
                ),

                # João Eduardo Rabelo de Medeiros - ED ES 02A - Bloco 1 - Lab 4 - go
                # Alocação aleatória, pois a linha estava sem monitor na imagem.
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="579284",
                    classroom_cod="ED-ES-02A"
                ),

                # Francisco Emilson Santos Souza Filho - ED ES 05A - Bloco 1 - Lab 3 - java
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="565805",
                    classroom_cod="ED-ES-05A"
                ),

                # Mário Martins Aragão - ED RC 03A - Bloco 3 - Lab 6 - c
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="542056",
                    classroom_cod="ED-RC-03A"
                ),

                # Heitor Pimenta Gotz - EDA CC 01A - Bloco 4 - Sala 1 - c++
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="566245",
                    classroom_cod="EDA-CC-01A"
                ),
                # Francisco Emilson Santos Souza Filho - EDA CC 01A - Bloco 4 - Sala 1 - c++
                MonitorAssignment(
                    weekly_hours=6,
                    monitor_registration="565805",
                    classroom_cod="EDA-CC-01A"
                ),
            ]
            session.add_all(alocacoes_monitores)
            await session.flush()

            print("Inserindo alunos...")

            matriculas_alunos = [
                "600001",
                "600002",
                "600003",
                "600004",
                "600005",
                "600006",
                "600007",
                "600008",
                "600009",
                "600010",
                "600011",
                "600012",
                "600013",
                "600014",
                "600015",
                "600016",
                "600017",
                "600018",
                "600019",
                "600020",
                "600021",
                "600022",
                "600023",
                "600024",
                "600025",
                "600026",
                "600027",
                "600028",
                "600029",
                "600030",
                "600031",
                "600032",
                "600033",
                "600034",
                "600035",
                "600036",
                "600037",
                "600038",
                "600039",
                "600040",
                "600041",
                "600042",
                "600043",
                "600044",
                "600045",
                "600046",
                "600047",
                "600048",
                "600049",
                "600050",
                "600051",
                "600052",
                "600053",
                "600054",
                "600055",
                "600056",
                "600057",
                "600058",
                "600059",
                "600060",
                "600061",
                "600062",
                "600063",
                "600064",
                "600065",
                "600066",
                "600067",
                "600068",
                "600069",
                "600070",
                "600071",
                "600072",
                "600073",
                "600074",
                "600075",
                "600076",
                "600077",
                "600078",
                "600079",
                "600080",
                "600081",
                "600082",
                "600083",
                "600084",
                "600085",
                "600086",
                "600087",
                "600088",
                "600089",
                "600090",
                "600091",
                "600092",
                "600093",
                "600094",
                "600095",
                "600096",
                "600097",
                "600098",
                "600099",
                "600100",
            ]

            alunos = [
                Student(
                    registration=HashService.generate_hash(
                        matricula,
                        HashAlgorithm.SHA256
                    )
                )
                for matricula in matriculas_alunos
            ]

            session.add_all(alunos)
            await session.flush() 

            print("Inserindo matrículas dos alunos nas turmas...") 
            enrollments = [ 
                
                Enrollment( student_id=alunos[0].id, classroom_cod="FUP-RC-08A" ), 
                Enrollment( student_id=alunos[1].id, classroom_cod="FUP-RC-08A" ), 
                Enrollment( student_id=alunos[2].id, classroom_cod="FUP-RC-08A" ), 
                Enrollment( student_id=alunos[3].id, classroom_cod="FUP-RC-08A" ), 
                Enrollment( student_id=alunos[4].id, classroom_cod="FUP-RC-08A" ), 
                Enrollment( student_id=alunos[5].id, classroom_cod="FUP-RC-09A" ), 
                Enrollment( student_id=alunos[6].id, classroom_cod="FUP-RC-09A" ), 
                Enrollment( student_id=alunos[7].id, classroom_cod="FUP-RC-09A" ), 
                Enrollment( student_id=alunos[8].id, classroom_cod="FUP-RC-09A" ), 
                Enrollment( student_id=alunos[9].id, classroom_cod="FUP-RC-09A" ), 
                Enrollment( student_id=alunos[10].id, classroom_cod="FUP-SI-04A" ), 
                Enrollment( student_id=alunos[11].id, classroom_cod="FUP-SI-04A" ), 
                Enrollment( student_id=alunos[12].id, classroom_cod="FUP-SI-04A" ), 
                Enrollment( student_id=alunos[13].id, classroom_cod="FUP-SI-04A" ), 
                Enrollment( student_id=alunos[14].id, classroom_cod="FUP-SI-04A" ), 
                Enrollment( student_id=alunos[15].id, classroom_cod="FUP-SI-05A" ), 
                Enrollment( student_id=alunos[16].id, classroom_cod="FUP-SI-05A" ), 
                Enrollment( student_id=alunos[17].id, classroom_cod="FUP-SI-05A" ), 
                Enrollment( student_id=alunos[18].id, classroom_cod="FUP-SI-05A" ), 
                Enrollment( student_id=alunos[19].id, classroom_cod="FUP-SI-05A" ), 
                Enrollment( student_id=alunos[20].id, classroom_cod="FUP-CC-01A" ), 
                Enrollment( student_id=alunos[21].id, classroom_cod="FUP-CC-01A" ), 
                Enrollment( student_id=alunos[22].id, classroom_cod="FUP-CC-01A" ), 
                Enrollment( student_id=alunos[23].id, classroom_cod="FUP-CC-01A" ), 
                Enrollment( student_id=alunos[24].id, classroom_cod="FUP-CC-01A" ), 
                Enrollment( student_id=alunos[25].id, classroom_cod="FUP-CC-02A" ), 
                Enrollment( student_id=alunos[26].id, classroom_cod="FUP-CC-02A" ), 
                Enrollment( student_id=alunos[27].id, classroom_cod="FUP-CC-02A" ), 
                Enrollment( student_id=alunos[28].id, classroom_cod="FUP-CC-02A" ), 
                Enrollment( student_id=alunos[29].id, classroom_cod="FUP-CC-02A" ), 
                Enrollment( student_id=alunos[30].id, classroom_cod="FUP-IA-03A" ), 
                Enrollment( student_id=alunos[31].id, classroom_cod="FUP-IA-03A" ), 
                Enrollment( student_id=alunos[32].id, classroom_cod="FUP-IA-03A" ), 
                Enrollment( student_id=alunos[33].id, classroom_cod="FUP-IA-03A" ), 
                Enrollment( student_id=alunos[34].id, classroom_cod="FUP-IA-03A" ), 
                Enrollment( student_id=alunos[35].id, classroom_cod="FUP-IA-10A" ), 
                Enrollment( student_id=alunos[36].id, classroom_cod="FUP-IA-10A" ), 
                Enrollment( student_id=alunos[37].id, classroom_cod="FUP-IA-10A" ), 
                Enrollment( student_id=alunos[38].id, classroom_cod="FUP-IA-10A" ), 
                Enrollment( student_id=alunos[39].id, classroom_cod="FUP-IA-10A" ), 
                Enrollment( student_id=alunos[40].id, classroom_cod="FUP-EC-11A" ), 
                Enrollment( student_id=alunos[41].id, classroom_cod="FUP-EC-11A" ), 
                Enrollment( student_id=alunos[42].id, classroom_cod="FUP-EC-11A" ), 
                Enrollment( student_id=alunos[43].id, classroom_cod="FUP-EC-11A" ), 
                Enrollment( student_id=alunos[44].id, classroom_cod="FUP-EC-11A" ), 
                Enrollment( student_id=alunos[45].id, classroom_cod="FUP-EC-12A" ), 
                Enrollment( student_id=alunos[46].id, classroom_cod="FUP-EC-12A" ), 
                Enrollment( student_id=alunos[47].id, classroom_cod="FUP-EC-12A" ), 
                Enrollment( student_id=alunos[48].id, classroom_cod="FUP-EC-12A" ), 
                Enrollment( student_id=alunos[49].id, classroom_cod="FUP-EC-12A" ), 
                Enrollment( student_id=alunos[50].id, classroom_cod="FUP-ES-06A" ), 
                Enrollment( student_id=alunos[51].id, classroom_cod="FUP-ES-06A" ), 
                Enrollment( student_id=alunos[52].id, classroom_cod="FUP-ES-06A" ), 
                Enrollment( student_id=alunos[53].id, classroom_cod="FUP-ES-06A" ), 
                Enrollment( student_id=alunos[54].id, classroom_cod="FUP-ES-06A" ), 
                Enrollment( student_id=alunos[55].id, classroom_cod="FUP-ES-07A" ), 
                Enrollment( student_id=alunos[56].id, classroom_cod="FUP-ES-07A" ), 
                Enrollment( student_id=alunos[57].id, classroom_cod="FUP-ES-07A" ), 
                Enrollment( student_id=alunos[58].id, classroom_cod="FUP-ES-07A" ), 
                Enrollment( student_id=alunos[59].id, classroom_cod="FUP-ES-07A" ), 
                Enrollment( student_id=alunos[60].id, classroom_cod="FUP-DD-01A" ), 
                Enrollment( student_id=alunos[61].id, classroom_cod="FUP-DD-01A" ), 
                Enrollment( student_id=alunos[62].id, classroom_cod="FUP-DD-01A" ), 
                Enrollment( student_id=alunos[63].id, classroom_cod="FUP-DD-01A" ), 
                Enrollment( student_id=alunos[64].id, classroom_cod="FUP-DD-01A" ), 
                Enrollment( student_id=alunos[65].id, classroom_cod="FUP-DD-02A" ), 
                Enrollment( student_id=alunos[66].id, classroom_cod="FUP-DD-02A" ), 
                Enrollment( student_id=alunos[67].id, classroom_cod="FUP-DD-02A" ), 
                Enrollment( student_id=alunos[68].id, classroom_cod="FUP-DD-02A" ), 
                Enrollment( student_id=alunos[69].id, classroom_cod="FUP-DD-02A" ), 
                Enrollment( student_id=alunos[70].id, classroom_cod="POO-01A" ), 
                Enrollment( student_id=alunos[71].id, classroom_cod="POO-01A" ), 
                Enrollment( student_id=alunos[72].id, classroom_cod="POO-01A" ), 
                Enrollment( student_id=alunos[73].id, classroom_cod="POO-01A" ), 
                Enrollment( student_id=alunos[74].id, classroom_cod="POO-01A" ), 
                Enrollment( student_id=alunos[75].id, classroom_cod="POO-02A" ), 
                Enrollment( student_id=alunos[76].id, classroom_cod="POO-02A" ), 
                Enrollment( student_id=alunos[77].id, classroom_cod="POO-02A" ), 
                Enrollment( student_id=alunos[78].id, classroom_cod="POO-02A" ), 
                Enrollment( student_id=alunos[79].id, classroom_cod="POO-02A" ), 
                Enrollment( student_id=alunos[80].id, classroom_cod="ED-SI-01A" ), 
                Enrollment( student_id=alunos[81].id, classroom_cod="ED-SI-01A" ), 
                Enrollment( student_id=alunos[82].id, classroom_cod="ED-SI-01A" ), 
                Enrollment( student_id=alunos[83].id, classroom_cod="ED-SI-01A" ), 
                Enrollment( student_id=alunos[84].id, classroom_cod="ED-SI-01A" ), 
                Enrollment( student_id=alunos[85].id, classroom_cod="ED-SI-04A" ), 
                Enrollment( student_id=alunos[86].id, classroom_cod="ED-SI-04A" ), 
                Enrollment( student_id=alunos[87].id, classroom_cod="ED-SI-04A" ), 
                Enrollment( student_id=alunos[88].id, classroom_cod="ED-SI-04A" ), 
                Enrollment( student_id=alunos[89].id, classroom_cod="ED-SI-04A" ), 
                Enrollment( student_id=alunos[90].id, classroom_cod="ED-ES-02A" ), 
                Enrollment( student_id=alunos[91].id, classroom_cod="ED-ES-02A" ), 
                Enrollment( student_id=alunos[92].id, classroom_cod="ED-ES-02A" ), 
                Enrollment( student_id=alunos[93].id, classroom_cod="ED-ES-02A" ), 
                Enrollment( student_id=alunos[94].id, classroom_cod="ED-ES-02A" ), 
                Enrollment( student_id=alunos[95].id, classroom_cod="ED-ES-05A" ), 
                Enrollment( student_id=alunos[96].id, classroom_cod="ED-ES-05A" ), 
                Enrollment( student_id=alunos[97].id, classroom_cod="ED-ES-05A" ), 
                Enrollment( student_id=alunos[98].id, classroom_cod="ED-ES-05A" ), 
                Enrollment( student_id=alunos[99].id, classroom_cod="ED-ES-05A" ), 
            ] 
            session.add_all(enrollments)
            await session.flush()

            print("Inserindo feedbacks dos alunos...")
            feedbacks = [
                Feedback(
                    assignment_id=alocacoes_monitores[0].id,
                    registration=alunos[0].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor explicou o conteúdo com muita clareza e ajudou bastante na resolução dos exercícios.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[1].id,
                    registration=alunos[1].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria foi bem organizada, com exemplos práticos e explicações fáceis de acompanhar.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[2].id,
                    registration=alunos[2].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria interessante disponibilizar uma lista extra de exercícios depois da monitoria.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[3].id,
                    registration=alunos[3].registration,
                    type_id=tipos_feedback[1].id,
                    text="A explicação foi boa, mas alguns pontos ficaram rápidos demais para acompanhar.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[4].id,
                    registration=alunos[4].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor demonstrou domínio do conteúdo e tirou as dúvidas com paciência.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[5].id,
                    registration=alunos[5].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia haver mais exemplos resolvidos passo a passo durante o atendimento.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[6].id,
                    registration=alunos[6].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria ajudou a entender melhor os conceitos vistos em sala de aula.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[7].id,
                    registration=alunos[7].registration,
                    type_id=tipos_feedback[1].id,
                    text="O atendimento foi útil, mas o tempo para dúvidas individuais poderia ser maior.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[8].id,
                    registration=alunos[8].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi atencioso e conseguiu explicar o problema de forma simples.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[9].id,
                    registration=alunos[9].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria bom separar um tempo final apenas para revisar os principais erros dos exercícios.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[10].id,
                    registration=alunos[10].registration,
                    type_id=tipos_feedback[0].id,
                    text="A explicação sobre os exercícios foi objetiva e contribuiu bastante para o aprendizado.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[11].id,
                    registration=alunos[11].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria começou um pouco confusa e demorou para entrar no assunto principal.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[12].id,
                    registration=alunos[12].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor respondeu bem às perguntas e manteve uma boa condução da atividade.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[13].id,
                    registration=alunos[13].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia ser criada uma rotina semanal de revisão dos tópicos mais cobrados.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[14].id,
                    registration=alunos[14].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria teve bons exemplos e ajudou na preparação para a prova.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[15].id,
                    registration=alunos[15].registration,
                    type_id=tipos_feedback[1].id,
                    text="O conteúdo foi explicado corretamente, mas faltou mais interação com a turma.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[16].id,
                    registration=alunos[16].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor mostrou disponibilidade e acompanhou bem as dificuldades dos alunos.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[17].id,
                    registration=alunos[17].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria útil compartilhar os códigos usados na monitoria após o encontro.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[18].id,
                    registration=alunos[18].registration,
                    type_id=tipos_feedback[0].id,
                    text="A atividade foi produtiva e os exemplos ajudaram a fixar o conteúdo.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[19].id,
                    registration=alunos[19].registration,
                    type_id=tipos_feedback[1].id,
                    text="Algumas dúvidas ficaram sem resposta por falta de tempo no final da monitoria.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[20].id,
                    registration=alunos[20].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor explicou com calma e usou exemplos próximos dos exercícios da disciplina.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[21].id,
                    registration=alunos[21].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia haver uma breve revisão teórica antes da resolução das questões.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[22].id,
                    registration=alunos[22].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria foi excelente e melhorou bastante minha compreensão do assunto.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[23].id,
                    registration=alunos[23].registration,
                    type_id=tipos_feedback[1].id,
                    text="A explicação ficou acelerada em alguns momentos e dificultou acompanhar a resolução.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[24].id,
                    registration=alunos[24].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi prestativo e ajudou a identificar onde eu estava errando.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[25].id,
                    registration=alunos[25].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria bom organizar os atendimentos por nível de dificuldade dos alunos.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[26].id,
                    registration=alunos[26].registration,
                    type_id=tipos_feedback[0].id,
                    text="A condução da monitoria foi clara, objetiva e bem alinhada com a disciplina.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[27].id,
                    registration=alunos[27].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria foi boa, mas poderia ter mais exercícios práticos durante o encontro.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[28].id,
                    registration=alunos[28].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor teve paciência para explicar várias vezes até a turma entender.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[29].id,
                    registration=alunos[29].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderiam ser enviados materiais complementares para estudo antes da monitoria.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[0].id,
                    registration=alunos[30].registration,
                    type_id=tipos_feedback[0].id,
                    text="A explicação foi muito boa e os exemplos facilitaram bastante o entendimento.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[1].id,
                    registration=alunos[31].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria ajudou, mas alguns conceitos ficaram pouco aprofundados.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[2].id,
                    registration=alunos[32].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor conseguiu esclarecer as dúvidas principais da atividade.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[3].id,
                    registration=alunos[33].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria interessante reservar uma parte da monitoria para dúvidas de trabalhos.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[4].id,
                    registration=alunos[34].registration,
                    type_id=tipos_feedback[0].id,
                    text="O atendimento foi ótimo e o monitor demonstrou bastante segurança no conteúdo.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[5].id,
                    registration=alunos[35].registration,
                    type_id=tipos_feedback[1].id,
                    text="A organização do encontro poderia melhorar, principalmente na divisão do tempo.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[6].id,
                    registration=alunos[36].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria contribuiu para resolver dificuldades que eu tinha nos exercícios.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[7].id,
                    registration=alunos[37].registration,
                    type_id=tipos_feedback[2].id,
                    text="Sugiro montar um roteiro com os tópicos abordados em cada encontro.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[8].id,
                    registration=alunos[38].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor explicou os detalhes das questões e ajudou a entender a lógica da solução.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[9].id,
                    registration=alunos[39].registration,
                    type_id=tipos_feedback[1].id,
                    text="A explicação foi útil, mas faltaram exemplos mais simples antes dos mais difíceis.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[10].id,
                    registration=alunos[40].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi muito atencioso e respondeu todas as dúvidas com clareza.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[11].id,
                    registration=alunos[41].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia haver uma lista de problemas recomendados para praticar em casa.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[12].id,
                    registration=alunos[42].registration,
                    type_id=tipos_feedback[0].id,
                    text="O encontro foi produtivo e bem focado nos conteúdos da disciplina.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[13].id,
                    registration=alunos[43].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria foi boa, mas poderia ter mais tempo para acompanhar cada aluno.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[14].id,
                    registration=alunos[44].registration,
                    type_id=tipos_feedback[0].id,
                    text="As explicações foram bem estruturadas e ajudaram a fixar o conteúdo.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[15].id,
                    registration=alunos[45].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria bom disponibilizar um resumo dos principais comandos e conceitos usados.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[16].id,
                    registration=alunos[46].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor conseguiu explicar o raciocínio sem apenas mostrar a resposta final.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[17].id,
                    registration=alunos[47].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria poderia ser mais organizada em relação à sequência dos assuntos.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[18].id,
                    registration=alunos[48].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi paciente e ajudou bastante na correção dos exercícios.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[19].id,
                    registration=alunos[49].registration,
                    type_id=tipos_feedback[2].id,
                    text="Sugiro que as próximas monitorias tenham mais exercícios de revisão para prova.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[20].id,
                    registration=alunos[50].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria foi clara e ajudou a melhorar minha confiança na disciplina.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[21].id,
                    registration=alunos[51].registration,
                    type_id=tipos_feedback[1].id,
                    text="O atendimento foi bom, mas algumas explicações ficaram muito resumidas.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[22].id,
                    registration=alunos[52].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor usou exemplos práticos que facilitaram bastante o entendimento.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[23].id,
                    registration=alunos[53].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia haver um documento compartilhado com dúvidas frequentes da turma.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[24].id,
                    registration=alunos[54].registration,
                    type_id=tipos_feedback[0].id,
                    text="A explicação foi objetiva e ajudou a entender os pontos principais.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[25].id,
                    registration=alunos[55].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria foi útil, mas seria melhor com uma organização prévia dos exercícios.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[26].id,
                    registration=alunos[56].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi muito solícito e explicou bem os erros mais comuns.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[27].id,
                    registration=alunos[57].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria interessante fazer uma revisão rápida no começo de cada atendimento.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[28].id,
                    registration=alunos[58].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria ajudou muito na compreensão dos assuntos que eu tinha dificuldade.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[29].id,
                    registration=alunos[59].registration,
                    type_id=tipos_feedback[1].id,
                    text="O ritmo da explicação poderia ser mais lento para acompanhar melhor.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[0].id,
                    registration=alunos[60].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor respondeu às dúvidas de forma educada e clara.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[1].id,
                    registration=alunos[61].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderiam ser propostos pequenos desafios para praticar depois da explicação.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[2].id,
                    registration=alunos[62].registration,
                    type_id=tipos_feedback[0].id,
                    text="A atividade foi bem conduzida e teve exemplos relevantes para a disciplina.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[3].id,
                    registration=alunos[63].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria foi boa, mas faltou revisar alguns conceitos básicos antes dos exercícios.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[4].id,
                    registration=alunos[64].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor explicou bem e ajudou a turma a entender os passos da solução.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[5].id,
                    registration=alunos[65].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria bom deixar os horários de atendimento mais visíveis para os alunos.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[6].id,
                    registration=alunos[66].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria foi proveitosa e contribuiu para o desenvolvimento das atividades.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[7].id,
                    registration=alunos[67].registration,
                    type_id=tipos_feedback[1].id,
                    text="O atendimento foi útil, mas poderia ter mais espaço para dúvidas individuais.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[8].id,
                    registration=alunos[68].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor mostrou domínio e explicou os conceitos de maneira acessível.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[9].id,
                    registration=alunos[69].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia haver uma pequena lista de exercícios ao final de cada monitoria.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[10].id,
                    registration=alunos[70].registration,
                    type_id=tipos_feedback[0].id,
                    text="A explicação foi clara e os exemplos foram bem escolhidos.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[11].id,
                    registration=alunos[71].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria poderia começar com objetivos mais claros para o encontro.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[12].id,
                    registration=alunos[72].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor ajudou a compreender melhor a resolução das questões.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[13].id,
                    registration=alunos[73].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria interessante gravar ou registrar os principais pontos das monitorias.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[14].id,
                    registration=alunos[74].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria foi bastante útil e ajudou no acompanhamento da disciplina.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[15].id,
                    registration=alunos[75].registration,
                    type_id=tipos_feedback[1].id,
                    text="A explicação foi boa, mas alguns exemplos ficaram sem conclusão detalhada.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[16].id,
                    registration=alunos[76].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi paciente e conseguiu adaptar a explicação às dúvidas da turma.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[17].id,
                    registration=alunos[77].registration,
                    type_id=tipos_feedback[2].id,
                    text="Sugiro trazer exemplos parecidos com os trabalhos avaliativos.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[18].id,
                    registration=alunos[78].registration,
                    type_id=tipos_feedback[0].id,
                    text="O atendimento foi organizado e ajudou a tirar dúvidas importantes.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[19].id,
                    registration=alunos[79].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria contribuiu, mas poderia ter uma dinâmica mais participativa.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[20].id,
                    registration=alunos[80].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor explicou muito bem e ajudou a entender os conceitos difíceis.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[21].id,
                    registration=alunos[81].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia ser feita uma revisão dos erros comuns antes das avaliações.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[22].id,
                    registration=alunos[82].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria foi clara, bem planejada e muito útil para os exercícios.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[23].id,
                    registration=alunos[83].registration,
                    type_id=tipos_feedback[1].id,
                    text="O tempo foi curto para a quantidade de dúvidas apresentadas pela turma.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[24].id,
                    registration=alunos[84].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi atencioso e explicou bem os pontos que causavam confusão.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[25].id,
                    registration=alunos[85].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria bom ter um cronograma com os temas de cada semana.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[26].id,
                    registration=alunos[86].registration,
                    type_id=tipos_feedback[0].id,
                    text="O atendimento foi excelente e as dúvidas foram respondidas com paciência.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[27].id,
                    registration=alunos[87].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria foi produtiva, mas faltou aprofundar algumas questões mais difíceis.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[28].id,
                    registration=alunos[88].registration,
                    type_id=tipos_feedback[0].id,
                    text="A explicação ajudou a corrigir erros e melhorar a solução dos exercícios.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[29].id,
                    registration=alunos[89].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderiam ser disponibilizados exercícios extras com gabarito comentado.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[0].id,
                    registration=alunos[90].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor conduziu bem o encontro e explicou com bastante clareza.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[1].id,
                    registration=alunos[91].registration,
                    type_id=tipos_feedback[1].id,
                    text="O encontro foi útil, mas poderia ter mais exemplos aplicados.",
                    rating=3
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[2].id,
                    registration=alunos[92].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria ajudou bastante na preparação para as atividades da disciplina.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[3].id,
                    registration=alunos[93].registration,
                    type_id=tipos_feedback[2].id,
                    text="Seria interessante abrir um espaço fixo para dúvidas sobre listas e trabalhos.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[4].id,
                    registration=alunos[94].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor foi claro nas explicações e manteve boa comunicação com a turma.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[5].id,
                    registration=alunos[95].registration,
                    type_id=tipos_feedback[1].id,
                    text="Algumas explicações ficaram corridas e dificultaram acompanhar a lógica.",
                    rating=2
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[6].id,
                    registration=alunos[96].registration,
                    type_id=tipos_feedback[0].id,
                    text="A monitoria foi muito boa e ajudou a entender melhor a matéria.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[7].id,
                    registration=alunos[97].registration,
                    type_id=tipos_feedback[2].id,
                    text="Poderia haver um material de apoio com os principais tópicos revisados.",
                    rating=4
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[8].id,
                    registration=alunos[98].registration,
                    type_id=tipos_feedback[0].id,
                    text="O monitor demonstrou paciência e conseguiu explicar de formas diferentes.",
                    rating=5
                ),
                Feedback(
                    assignment_id=alocacoes_monitores[9].id,
                    registration=alunos[99].registration,
                    type_id=tipos_feedback[1].id,
                    text="A monitoria foi positiva, mas poderia ter melhor controle do tempo.",
                    rating=3
                )
            ]

            session.add_all(feedbacks)
            await session.flush()

            await session.commit()
            
            print("Carga de dados concluída com sucesso!")
        except Exception as e:
            await session.rollback()
            print(f"Erro ao carregar dados: {e}")

if __name__ == "__main__":
    asyncio.run(seed_data())