import asyncio
from app.core.database import init_db

from app.core.enums import MessageType
from app.services.hash_service import HashService, HashAlgorithm
from app.models.professor import Professor
from app.models.subject import Subject
from app.models.classroom import Classroom
from app.models.student import Student
from app.models.enrollment import Enrollment
from app.models.monitor import Monitor
from app.models.monitor_assignment import MonitorAssignment
from app.models.feedback import Feedback


async def seed_data():
    try:
        print("A iniciar a ligação ao MongoDB...")

        await init_db()

        print("A limpar a base de dados antiga...")

        await Classroom.find_all().delete()
        await Subject.find_all().delete()
        await Professor.find_all().delete()
        await Student.find_all().delete()
        await Enrollment.find_all().delete()
        await Monitor.find_all().delete()
        await MonitorAssignment.find_all().delete()
        await Feedback.find_all().delete()

        print("A inserir Professores (Nível 1)...")
        professores = [
            Professor(name="ARTHUR RODRIGUES ARARUNA", email="ararunaufc@gmail.com"),
            Professor(name="ARTHUR RODRIGUES ARARUNA", email="qxd@araruna.prof"),
            Professor(name="ATILIO GOMES LUIZ", email="gomes.atilio@gmail.com"),
            Professor(
                name="CARLOS ROBERTO RODRIGUES FILHO",
                email="filho.rodrigues@ufc.br",
            ),
            Professor(name="CLARO HENRIQUE SILVA SALES", email="clarosales@ufc.br"),
            Professor(name="DAVID SENA OLIVEIRA", email="sena.ufc@gmail.com"),
            Professor(name="FABIO CARLOS SOUSA DIAS", email="fabiodias@ufc.br"),
            Professor(
                name="MARCELO MARTINS DA SILVA", email="martins2016eng@gmail.com"
            ),
            Professor(
                name="MARCIO ESPINDOLA FREIRE MAIA", email="marcioefmaia@gmail.com"
            ),
            Professor(
                name="MARCOS ANTONIO DE OLIVEIRA", email="marcos.oliveira@ufc.br"
            ),
            Professor(
                name="PAULO HENRIQUE MACEDO DE ARAUJO",
                email="phmacedoaraujo@ufc.br",
            ),
            Professor(
                name="RICARDO REIS PEREIRA", email="ricardoreispereira@gmail.com"
            ),
            Professor(name="RUBENS FERNANDES NUNES", email="rubensfn@gmail.com"),
            Professor(
                name="SIDARTHA AZEVEDO LOBO DE CARVALHO", email="sidartha@ufc.br"
            ),
            Professor(
                name="VICTOR AGUIAR EVANGELISTA DE FARIAS",
                email="victor.aefarias@gmail.com",
            ),
            Professor(name="BRUNO MATHEUS GÓIS", email="brunomateus@gmail.com"),
            Professor(
                name="ENYO JOSE TAVARES GONCALVES", email="enyo.goncalves@ufc.br"
            ),
            Professor(name="ALEXANDRE MATOS ARRUDA", email="alexandre.matos@ufc.br"),
            Professor(name="WAGNER GUIMARAES AL ALAM", email="wagner.alalam@ufc.br"),
        ]
        await Professor.insert_many(professores)

        professores_salvos = await Professor.find_all().to_list()
        professor_por_email = {p.email: p for p in professores_salvos}

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

        print("A inserir Disciplinas (Nível 1)...")
        disciplinas = [
            Subject(cod="QXD0001", name="Fundamentos de Programação"),
            Subject(cod="QXD0007", name="Programação Orientada a Objetos"),
            Subject(cod="QXD0010", name="Estrutura de Dados"),
            Subject(cod="QXD0115", name="Estrutura de Dados Avançada"),
        ]
        await Subject.insert_many(disciplinas)

        disciplinas_salvas = await Subject.find_all().to_list()
        disciplina_por_cod = {d.cod: d for d in disciplinas_salvas}

        print("A inserir Turmas (Nível 2)...")
        turmas = [
            Classroom(
                cod="FUP-RC-08A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_enyo,
            ),
            Classroom(
                cod="FUP-RC-09A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_claro,
            ),
            Classroom(
                cod="FUP-SI-04A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_alexandre,
            ),
            Classroom(
                cod="FUP-SI-05A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_arthur,
            ),
            Classroom(
                cod="FUP-CC-01A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_david,
            ),
            Classroom(
                cod="FUP-CC-02A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_alexandre,
            ),
            Classroom(
                cod="FUP-IA-03A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_alexandre,
            ),
            Classroom(
                cod="FUP-IA-10A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_sidartha,
            ),
            Classroom(
                cod="FUP-EC-11A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_rubens,
            ),
            Classroom(
                cod="FUP-EC-12A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_claro,
            ),
            Classroom(
                cod="FUP-ES-06A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_rubens,
            ),
            Classroom(
                cod="FUP-ES-07A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_claro,
            ),
            Classroom(
                cod="FUP-DD-01A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_david,
            ),
            Classroom(
                cod="FUP-DD-02A",
                subject=disciplina_por_cod["QXD0001"],
                professor=professor_bruno,
            ),
            Classroom(
                cod="POO-01A",
                subject=disciplina_por_cod["QXD0007"],
                professor=professor_wagner,
            ),
            Classroom(
                cod="POO-02A",
                subject=disciplina_por_cod["QXD0007"],
                professor=professor_wagner,
            ),
            Classroom(
                cod="ED-SI-01A",
                subject=disciplina_por_cod["QXD0010"],
                professor=professor_david,
            ),
            Classroom(
                cod="ED-SI-04A",
                subject=disciplina_por_cod["QXD0010"],
                professor=professor_arthur,
            ),
            Classroom(
                cod="ED-ES-02A",
                subject=disciplina_por_cod["QXD0010"],
                professor=professor_david,
            ),
            Classroom(
                cod="ED-ES-05A",
                subject=disciplina_por_cod["QXD0010"],
                professor=professor_arthur,
            ),
            Classroom(
                cod="ED-RC-03A",
                subject=disciplina_por_cod["QXD0010"],
                professor=professor_wagner,
            ),
            Classroom(
                cod="EDA-CC-01A",
                subject=disciplina_por_cod["QXD0010"],
                professor=professor_atilio,
            ),
        ]
        await Classroom.insert_many(turmas)

        turmas_salvas = await Classroom.find_all().to_list()
        turma_por_cod = {t.cod: t for t in turmas_salvas}

        print("A inserir Alunos (Nível 3)...")
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
            Student(registration=HashService.generate_hash(m, HashAlgorithm.SHA256))
            for m in matriculas_alunos
        ]

        hash_para_indice = {
            HashService.generate_hash(m, HashAlgorithm.SHA256): i
            for i, m in enumerate(matriculas_alunos)
        }

        await Student.insert_many(alunos)
        alunos_salvos = await Student.find_all().to_list()

        alunos_ordenados = [None] * len(matriculas_alunos)
        for a in alunos_salvos:
            idx = hash_para_indice[a.registration]
            alunos_ordenados[idx] = a

        print("A inserir Matrículas (Nível 4)...")
        enrollments = [
            Enrollment(
                student=alunos_ordenados[0], classroom=turma_por_cod["FUP-RC-08A"]
            ),
            Enrollment(
                student=alunos_ordenados[1], classroom=turma_por_cod["FUP-RC-08A"]
            ),
            Enrollment(
                student=alunos_ordenados[2], classroom=turma_por_cod["FUP-RC-08A"]
            ),
            Enrollment(
                student=alunos_ordenados[3], classroom=turma_por_cod["FUP-RC-08A"]
            ),
            Enrollment(
                student=alunos_ordenados[4], classroom=turma_por_cod["FUP-RC-08A"]
            ),
            Enrollment(
                student=alunos_ordenados[5], classroom=turma_por_cod["FUP-RC-09A"]
            ),
            Enrollment(
                student=alunos_ordenados[6], classroom=turma_por_cod["FUP-RC-09A"]
            ),
            Enrollment(
                student=alunos_ordenados[7], classroom=turma_por_cod["FUP-RC-09A"]
            ),
            Enrollment(
                student=alunos_ordenados[8], classroom=turma_por_cod["FUP-RC-09A"]
            ),
            Enrollment(
                student=alunos_ordenados[9], classroom=turma_por_cod["FUP-RC-09A"]
            ),
            Enrollment(
                student=alunos_ordenados[10], classroom=turma_por_cod["FUP-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[11], classroom=turma_por_cod["FUP-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[12], classroom=turma_por_cod["FUP-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[13], classroom=turma_por_cod["FUP-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[14], classroom=turma_por_cod["FUP-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[15], classroom=turma_por_cod["FUP-SI-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[16], classroom=turma_por_cod["FUP-SI-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[17], classroom=turma_por_cod["FUP-SI-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[18], classroom=turma_por_cod["FUP-SI-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[19], classroom=turma_por_cod["FUP-SI-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[20], classroom=turma_por_cod["FUP-CC-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[21], classroom=turma_por_cod["FUP-CC-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[22], classroom=turma_por_cod["FUP-CC-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[23], classroom=turma_por_cod["FUP-CC-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[24], classroom=turma_por_cod["FUP-CC-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[25], classroom=turma_por_cod["FUP-CC-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[26], classroom=turma_por_cod["FUP-CC-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[27], classroom=turma_por_cod["FUP-CC-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[28], classroom=turma_por_cod["FUP-CC-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[29], classroom=turma_por_cod["FUP-CC-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[30], classroom=turma_por_cod["FUP-IA-03A"]
            ),
            Enrollment(
                student=alunos_ordenados[31], classroom=turma_por_cod["FUP-IA-03A"]
            ),
            Enrollment(
                student=alunos_ordenados[32], classroom=turma_por_cod["FUP-IA-03A"]
            ),
            Enrollment(
                student=alunos_ordenados[33], classroom=turma_por_cod["FUP-IA-03A"]
            ),
            Enrollment(
                student=alunos_ordenados[34], classroom=turma_por_cod["FUP-IA-03A"]
            ),
            Enrollment(
                student=alunos_ordenados[35], classroom=turma_por_cod["FUP-IA-10A"]
            ),
            Enrollment(
                student=alunos_ordenados[36], classroom=turma_por_cod["FUP-IA-10A"]
            ),
            Enrollment(
                student=alunos_ordenados[37], classroom=turma_por_cod["FUP-IA-10A"]
            ),
            Enrollment(
                student=alunos_ordenados[38], classroom=turma_por_cod["FUP-IA-10A"]
            ),
            Enrollment(
                student=alunos_ordenados[39], classroom=turma_por_cod["FUP-IA-10A"]
            ),
            Enrollment(
                student=alunos_ordenados[40], classroom=turma_por_cod["FUP-EC-11A"]
            ),
            Enrollment(
                student=alunos_ordenados[41], classroom=turma_por_cod["FUP-EC-11A"]
            ),
            Enrollment(
                student=alunos_ordenados[42], classroom=turma_por_cod["FUP-EC-11A"]
            ),
            Enrollment(
                student=alunos_ordenados[43], classroom=turma_por_cod["FUP-EC-11A"]
            ),
            Enrollment(
                student=alunos_ordenados[44], classroom=turma_por_cod["FUP-EC-11A"]
            ),
            Enrollment(
                student=alunos_ordenados[45], classroom=turma_por_cod["FUP-EC-12A"]
            ),
            Enrollment(
                student=alunos_ordenados[46], classroom=turma_por_cod["FUP-EC-12A"]
            ),
            Enrollment(
                student=alunos_ordenados[47], classroom=turma_por_cod["FUP-EC-12A"]
            ),
            Enrollment(
                student=alunos_ordenados[48], classroom=turma_por_cod["FUP-EC-12A"]
            ),
            Enrollment(
                student=alunos_ordenados[49], classroom=turma_por_cod["FUP-EC-12A"]
            ),
            Enrollment(
                student=alunos_ordenados[50], classroom=turma_por_cod["FUP-ES-06A"]
            ),
            Enrollment(
                student=alunos_ordenados[51], classroom=turma_por_cod["FUP-ES-06A"]
            ),
            Enrollment(
                student=alunos_ordenados[52], classroom=turma_por_cod["FUP-ES-06A"]
            ),
            Enrollment(
                student=alunos_ordenados[53], classroom=turma_por_cod["FUP-ES-06A"]
            ),
            Enrollment(
                student=alunos_ordenados[54], classroom=turma_por_cod["FUP-ES-06A"]
            ),
            Enrollment(
                student=alunos_ordenados[55], classroom=turma_por_cod["FUP-ES-07A"]
            ),
            Enrollment(
                student=alunos_ordenados[56], classroom=turma_por_cod["FUP-ES-07A"]
            ),
            Enrollment(
                student=alunos_ordenados[57], classroom=turma_por_cod["FUP-ES-07A"]
            ),
            Enrollment(
                student=alunos_ordenados[58], classroom=turma_por_cod["FUP-ES-07A"]
            ),
            Enrollment(
                student=alunos_ordenados[59], classroom=turma_por_cod["FUP-ES-07A"]
            ),
            Enrollment(
                student=alunos_ordenados[60], classroom=turma_por_cod["FUP-DD-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[61], classroom=turma_por_cod["FUP-DD-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[62], classroom=turma_por_cod["FUP-DD-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[63], classroom=turma_por_cod["FUP-DD-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[64], classroom=turma_por_cod["FUP-DD-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[65], classroom=turma_por_cod["FUP-DD-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[66], classroom=turma_por_cod["FUP-DD-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[67], classroom=turma_por_cod["FUP-DD-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[68], classroom=turma_por_cod["FUP-DD-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[69], classroom=turma_por_cod["FUP-DD-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[70], classroom=turma_por_cod["POO-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[71], classroom=turma_por_cod["POO-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[72], classroom=turma_por_cod["POO-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[73], classroom=turma_por_cod["POO-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[74], classroom=turma_por_cod["POO-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[75], classroom=turma_por_cod["POO-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[76], classroom=turma_por_cod["POO-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[77], classroom=turma_por_cod["POO-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[78], classroom=turma_por_cod["POO-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[79], classroom=turma_por_cod["POO-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[80], classroom=turma_por_cod["ED-SI-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[81], classroom=turma_por_cod["ED-SI-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[82], classroom=turma_por_cod["ED-SI-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[83], classroom=turma_por_cod["ED-SI-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[84], classroom=turma_por_cod["ED-SI-01A"]
            ),
            Enrollment(
                student=alunos_ordenados[85], classroom=turma_por_cod["ED-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[86], classroom=turma_por_cod["ED-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[87], classroom=turma_por_cod["ED-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[88], classroom=turma_por_cod["ED-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[89], classroom=turma_por_cod["ED-SI-04A"]
            ),
            Enrollment(
                student=alunos_ordenados[90], classroom=turma_por_cod["ED-ES-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[91], classroom=turma_por_cod["ED-ES-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[92], classroom=turma_por_cod["ED-ES-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[93], classroom=turma_por_cod["ED-ES-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[94], classroom=turma_por_cod["ED-ES-02A"]
            ),
            Enrollment(
                student=alunos_ordenados[95], classroom=turma_por_cod["ED-ES-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[96], classroom=turma_por_cod["ED-ES-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[97], classroom=turma_por_cod["ED-ES-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[98], classroom=turma_por_cod["ED-ES-05A"]
            ),
            Enrollment(
                student=alunos_ordenados[99], classroom=turma_por_cod["ED-ES-05A"]
            ),
        ]
        await Enrollment.insert_many(enrollments)

        enrollments_salvos = await Enrollment.find_all().to_list()

        for matricula in enrollments_salvos:
            student_id = matricula.student.id if hasattr(matricula.student, "id") else matricula.student.ref.id
            
            for aluno in alunos_ordenados:
                if aluno and aluno.id == student_id:
                    if getattr(aluno, "enrollments", None) is None:
                        aluno.enrollments = []
                    aluno.enrollments.append(matricula)
                    break

        for aluno in alunos_ordenados:
            if aluno and getattr(aluno, "enrollments", None):
                await aluno.save()

        print("A inserir Monitores (Nível 5)...")
        monitores = [
            Monitor(
                registration="564925",
                name="Ana Amélia de Sousa Santos",
                email="anaameliatdj@gmail.com",
            ),
            Monitor(
                registration="565321",
                name="Iago de Oliveira Lô",
                email="iagooliveiralo070@gmail.com",
            ),
            Monitor(
                registration="567157",
                name="Denilso Bernardo Nunes da Silva",
                email="nilsonde@alu.ufc.br",
            ),
            Monitor(
                registration="568334",
                name="Weryck Lemos Silva",
                email="weryck.lemos@alu.ufc.br",
            ),
            Monitor(
                registration="581924",
                name="João David B. de Araújo",
                email="davidbramsiga@gmail.com",
            ),
            Monitor(
                registration="579703",
                name="Hanna Lavine Lima Chaves",
                email="hannalavine@alu.ufc.br",
            ),
            Monitor(
                registration="564976",
                name="Alana Maria Sousa Augusto",
                email="alana.augusto@alu.ufc.br",
            ),
            Monitor(
                registration="586077",
                name="Maria Vitória de Almeida Ferreira",
                email="mariavito@alu.ufc.br",
            ),
            Monitor(
                registration="581908",
                name="Matheus de Sousa Mendes",
                email="matheussousamendes81@gmail.com",
            ),
            Monitor(
                registration="579705",
                name="Cesário Porto Magalhães Filho",
                email="cesario.0324@alu.ufc.br",
            ),
            Monitor(
                registration="581895",
                name="Matheus Eugênio Granja",
                email="matheuseugenioo@alu.ufc.br",
            ),
            Monitor(
                registration="565805",
                name="Francisco Emilson Santos Souza Filho",
                email="emilsonfilhocontato@gmail.com",
            ),
            Monitor(
                registration="566245",
                name="Heitor Pimenta Gotz",
                email="heitor.gotz@alu.ufc.br",
            ),
            Monitor(
                registration="567579",
                name="Pedro Edson Maciel de Araújo",
                email="pedroedsonmaciel@alu.ufc.br",
            ),
            Monitor(
                registration="571600",
                name="Carla Cristina Sousa Araújo",
                email="carlacristinasousasaraujo@alu.ufc.br",
            ),
            Monitor(
                registration="582749",
                name="Luiz Guilherme Cavalcante Martins",
                email="luiz.gcm@alu.ufc.br",
            ),
            Monitor(
                registration="579925",
                name="Vicente de Paulo da Silva Neto",
                email="vicentesilva@alu.ufc.br",
            ),
            Monitor(
                registration="582392",
                name="Jordan Pinheiro Mesquita",
                email="jordanpinheiro@alu.ufc.br",
            ),
            Monitor(
                registration="581559",
                name="Carlos Rodrigues Nobre",
                email="carlosrodrigues23@alu.ufc.br",
            ),
            Monitor(
                registration="581946",
                name="José Luis Souza Arruda Rodrigues",
                email="joseluis12@alu.ufc.br",
            ),
            Monitor(
                registration="580650",
                name="João Eudes Campos Colares Neto",
                email="jeudescolares@alu.ufc.br",
            ),
            Monitor(
                registration="583190",
                name="Daniel Andrade Siqueira",
                email="danielandrade070@alu.ufc.br",
            ),
            Monitor(
                registration="582243",
                name="João Filipe Fonseca de Oliveira",
                email="joaofilipefonseca@alu.ufc.br",
            ),
            Monitor(
                registration="580840",
                name="Antônio Pompeu de Araújo Neto",
                email="pompeuaraujo512@gmail.com",
            ),
            Monitor(
                registration="542056",
                name="Mário Martins Aragão",
                email="marioaragao@alu.ufc.br",
            ),
            Monitor(
                registration="579284",
                name="João Eduardo Rabelo de Medeiros",
                email="joaoeduardo@alu.ufc.br",
            ),
            Monitor(
                registration="590065",
                name="Daniel Fernandes Ferreira",
                email="danielfernandesmb11@gmail.com",
            ),
        ]
        await Monitor.insert_many(monitores)
        monitores_salvos = await Monitor.find_all().to_list()
        monitor_por_reg = {m.registration: m for m in monitores_salvos}

        print("A inserir Atribuições de Monitor (Nível 6)...")
        alocacoes_monitores = [
            # Carlos Rodrigues Nobre - FUP RC 08A - Bloco 3 - Lab 7 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["581559"],
                classroom=turma_por_cod["FUP-RC-08A"],
            ),
            # Ana Amélia de Sousa Santos - FUP RC 08A - Bloco 3 - Lab 7 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["564925"],
                classroom=turma_por_cod["FUP-RC-08A"],
            ),
            # José Luis Souza Arruda Rodrigues - FUP RC 09A - Bloco 1 - Lab 3 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["581946"],
                classroom=turma_por_cod["FUP-RC-09A"],
            ),
            # Matheus de Sousa Mendes - FUP RC 09A - Bloco 1 - Lab 3 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["581908"],
                classroom=turma_por_cod["FUP-RC-09A"],
            ),
            # Weryck Lemos Silva - FUP SI 04A - Bloco 4 - Lab 2 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["568334"],
                classroom=turma_por_cod["FUP-SI-04A"],
            ),
            # Vicente de Paulo da Silva Neto - FUP SI 05A - Bloco 1 - Lab 4 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["579925"],
                classroom=turma_por_cod["FUP-SI-05A"],
            ),
            # Daniel Andrade Siqueira - FUP CC 01A - Bloco 3 - Lab 6 - go
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["583190"],
                classroom=turma_por_cod["FUP-CC-01A"],
            ),
            # Jordan Pinheiro Mesquita - FUP CC 01A - Bloco 3 - Lab 6 - go
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["582392"],
                classroom=turma_por_cod["FUP-CC-01A"],
            ),
            # Maria Vitória de Almeida Ferreira - FUP CC 02A - Bloco 3 - Lab 7 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["586077"],
                classroom=turma_por_cod["FUP-CC-02A"],
            ),
            # Antônio Pompeu de Araújo Neto - FUP CC 02A - Bloco 3 - Lab 7 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["580840"],
                classroom=turma_por_cod["FUP-CC-02A"],
            ),
            # Iago de Oliveira Lô - FUP IA 03A - Bloco 3 - Lab 6 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["565321"],
                classroom=turma_por_cod["FUP-IA-03A"],
            ),
            # Denilso Bernardo Nunes da Silva - FUP IA 10A - Bloco 4 - Lab 5 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["567157"],
                classroom=turma_por_cod["FUP-IA-10A"],
            ),
            # Pedro Edson Maciel de Araújo - FUP EC 11A - Bloco 1 - Lab 4 - C/C++
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["567579"],
                classroom=turma_por_cod["FUP-EC-11A"],
            ),
            # Matheus Eugênio Granja - FUP EC 12A - Bloco 1 - Lab 3 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["581895"],
                classroom=turma_por_cod["FUP-EC-12A"],
            ),
            # Hanna Lavine Lima Chaves - FUP ES 06A - Bloco 1 - Lab 4 - c++
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["579703"],
                classroom=turma_por_cod["FUP-ES-06A"],
            ),
            # Luiz Guilherme Cavalcante Martins - FUP ES 06A - Bloco 1 - Lab 4 - c++
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["582749"],
                classroom=turma_por_cod["FUP-ES-06A"],
            ),
            # João David B. de Araújo / Brandão - FUP ES 07A - Bloco 1 - Lab 3 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["581924"],
                classroom=turma_por_cod["FUP-ES-07A"],
            ),
            # João Eudes Campos Colares Neto - FUP ES 07A - Bloco 1 - Lab 3 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["580650"],
                classroom=turma_por_cod["FUP-ES-07A"],
            ),
            # Hanna Lavine Lima Chaves - FUP DD 01A - Bloco 3 - Lab 7 - go
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["579703"],
                classroom=turma_por_cod["FUP-DD-01A"],
            ),
            # Daniel Fernandes Ferreira - FUP DD 01A - Bloco 3 - Lab 7 - go
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["590065"],
                classroom=turma_por_cod["FUP-DD-01A"],
            ),
            # Cesário Porto Magalhães Filho - FUP DD 02A - Bloco 3 - Lab 6 - go
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["579705"],
                classroom=turma_por_cod["FUP-DD-02A"],
            ),
            # Alana Maria Sousa Augusto - POO 01A - Bloco 4 - Lab 5 - java
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["564976"],
                classroom=turma_por_cod["POO-01A"],
            ),
            # Carla Cristina Sousa Araújo - POO 02A - Bloco 3 - Lab 7 - java
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["571600"],
                classroom=turma_por_cod["POO-02A"],
            ),
            # Weryck Lemos Silva - ED SI 01A - Bloco 4 - Lab 5 - go
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["568334"],
                classroom=turma_por_cod["ED-SI-01A"],
            ),
            # João Filipe Fonseca de Oliveira - ED SI 04A - Seg B1Lab 2 / Ter B1S1 - java
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["582243"],
                classroom=turma_por_cod["ED-SI-04A"],
            ),
            # João Eduardo Rabelo de Medeiros - ED ES 02A - Bloco 1 - Lab 4 - go
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["579284"],
                classroom=turma_por_cod["ED-ES-02A"],
            ),
            # Francisco Emilson Santos Souza Filho - ED ES 05A - Bloco 1 - Lab 3 - java
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["565805"],
                classroom=turma_por_cod["ED-ES-05A"],
            ),
            # Mário Martins Aragão - ED RC 03A - Bloco 3 - Lab 6 - c
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["542056"],
                classroom=turma_por_cod["ED-RC-03A"],
            ),
            # Heitor Pimenta Gotz - EDA CC 01A - Bloco 4 - Sala 1 - c++
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["566245"],
                classroom=turma_por_cod["EDA-CC-01A"],
            ),
            # Francisco Emilson Santos Souza Filho - EDA CC 01A - Bloco 4 - Sala 1 - c++
            MonitorAssignment(
                weekly_hours=6,
                monitor=monitor_por_reg["565805"],
                classroom=turma_por_cod["EDA-CC-01A"],
            ),
        ]
        await MonitorAssignment.insert_many(alocacoes_monitores)
        alocacoes_salvas = await MonitorAssignment.find_all().to_list()

        chave_para_indice = {}
        for i, a in enumerate(alocacoes_monitores):
            chave = (str(a.monitor.id), str(a.classroom.id))
            chave_para_indice[chave] = i

        alocacoes_ordenadas = [None] * len(alocacoes_monitores)
        for a in alocacoes_salvas:
            chave = (str(a.monitor.ref.id), str(a.classroom.ref.id))
            if chave in chave_para_indice:
                alocacoes_ordenadas[chave_para_indice[chave]] = a

        print("A inserir Feedbacks (Nível 7)...")
        feedbacks = [
            Feedback(
                assignment=alocacoes_ordenadas[0],
                registration=alunos_ordenados[0].registration,
                type=MessageType.ELOGIO,
                text="O monitor explicou o conteúdo com muita clareza e ajudou bastante na resolução dos exercícios.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[1],
                registration=alunos_ordenados[1].registration,
                type=MessageType.ELOGIO,
                text="A monitoria foi bem organizada, com exemplos práticos e explicações fáceis de acompanhar.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[2],
                registration=alunos_ordenados[2].registration,
                type=MessageType.SUGESTAO,
                text="Seria interessante disponibilizar uma lista extra de exercícios depois da monitoria.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[3],
                registration=alunos_ordenados[3].registration,
                type=MessageType.CRITICA,
                text="A explicação foi boa, mas alguns pontos ficaram rápidos demais para acompanhar.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[4],
                registration=alunos_ordenados[4].registration,
                type=MessageType.ELOGIO,
                text="O monitor demonstrou domínio do conteúdo e tirou as dúvidas com paciência.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[5],
                registration=alunos_ordenados[5].registration,
                type=MessageType.SUGESTAO,
                text="Poderia haver mais exemplos resolvidos passo a passo durante o atendimento.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[6],
                registration=alunos_ordenados[6].registration,
                type=MessageType.ELOGIO,
                text="A monitoria ajudou a entender melhor os conceitos vistos em sala de aula.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[7],
                registration=alunos_ordenados[7].registration,
                type=MessageType.CRITICA,
                text="O atendimento foi útil, mas o tempo para dúvidas individuais poderia ser maior.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[8],
                registration=alunos_ordenados[8].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi atencioso e conseguiu explicar o problema de forma simples.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[9],
                registration=alunos_ordenados[9].registration,
                type=MessageType.SUGESTAO,
                text="Seria bom separar um tempo final apenas para revisar os principais erros dos exercícios.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[10],
                registration=alunos_ordenados[10].registration,
                type=MessageType.ELOGIO,
                text="A explicação sobre os exercícios foi objetiva e contribuiu bastante para o aprendizado.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[11],
                registration=alunos_ordenados[11].registration,
                type=MessageType.CRITICA,
                text="A monitoria começou um pouco confusa e demorou para entrar no assunto principal.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[12],
                registration=alunos_ordenados[12].registration,
                type=MessageType.ELOGIO,
                text="O monitor respondeu bem às perguntas e manteve uma boa condução da atividade.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[13],
                registration=alunos_ordenados[13].registration,
                type=MessageType.SUGESTAO,
                text="Poderia ser criada uma rotina semanal de revisão dos tópicos mais cobrados.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[14],
                registration=alunos_ordenados[14].registration,
                type=MessageType.ELOGIO,
                text="A monitoria teve bons exemplos e ajudou na preparação para a prova.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[15],
                registration=alunos_ordenados[15].registration,
                type=MessageType.CRITICA,
                text="O conteúdo foi explicado corretamente, mas faltou mais interação com a turma.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[16],
                registration=alunos_ordenados[16].registration,
                type=MessageType.ELOGIO,
                text="O monitor mostrou disponibilidade e acompanhou bem as dificuldades dos alunos_ordenados.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[17],
                registration=alunos_ordenados[17].registration,
                type=MessageType.SUGESTAO,
                text="Seria útil compartilhar os códigos usados na monitoria após o encontro.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[18],
                registration=alunos_ordenados[18].registration,
                type=MessageType.ELOGIO,
                text="A atividade foi produtiva e os exemplos ajudaram a fixar o conteúdo.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[19],
                registration=alunos_ordenados[19].registration,
                type=MessageType.CRITICA,
                text="Algumas dúvidas ficaram sem resposta por falta de tempo no final da monitoria.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[20],
                registration=alunos_ordenados[20].registration,
                type=MessageType.ELOGIO,
                text="O monitor explicou com calma e usou exemplos próximos dos exercícios da disciplina.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[21],
                registration=alunos_ordenados[21].registration,
                type=MessageType.SUGESTAO,
                text="Poderia haver uma breve revisão teórica antes da resolução das questões.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[22],
                registration=alunos_ordenados[22].registration,
                type=MessageType.ELOGIO,
                text="A monitoria foi excelente e melhorou bastante minha compreensão do assunto.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[23],
                registration=alunos_ordenados[23].registration,
                type=MessageType.CRITICA,
                text="A explicação ficou acelerada em alguns momentos e dificultou acompanhar a resolução.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[24],
                registration=alunos_ordenados[24].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi prestativo e ajudou a identificar onde eu estava errando.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[25],
                registration=alunos_ordenados[25].registration,
                type=MessageType.SUGESTAO,
                text="Seria bom organizar os atendimentos por nível de dificuldade dos alunos_ordenados.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[26],
                registration=alunos_ordenados[26].registration,
                type=MessageType.ELOGIO,
                text="A condução da monitoria foi clara, objetiva e bem alinhada com a disciplina.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[27],
                registration=alunos_ordenados[27].registration,
                type=MessageType.CRITICA,
                text="A monitoria foi boa, mas poderia ter mais exercícios práticos durante o encontro.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[28],
                registration=alunos_ordenados[28].registration,
                type=MessageType.ELOGIO,
                text="O monitor teve paciência para explicar várias vezes até a turma entender.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[29],
                registration=alunos_ordenados[29].registration,
                type=MessageType.SUGESTAO,
                text="Poderiam ser enviados materiais complementares para estudo antes da monitoria.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[0],
                registration=alunos_ordenados[30].registration,
                type=MessageType.ELOGIO,
                text="A explicação foi muito boa e os exemplos facilitaram bastante o entendimento.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[1],
                registration=alunos_ordenados[31].registration,
                type=MessageType.CRITICA,
                text="A monitoria ajudou, mas alguns conceitos ficaram pouco aprofundados.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[2],
                registration=alunos_ordenados[32].registration,
                type=MessageType.ELOGIO,
                text="O monitor conseguiu esclarecer as dúvidas principais da atividade.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[3],
                registration=alunos_ordenados[33].registration,
                type=MessageType.SUGESTAO,
                text="Seria interessante reservar uma parte da monitoria para dúvidas de trabalhos.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[4],
                registration=alunos_ordenados[34].registration,
                type=MessageType.ELOGIO,
                text="O atendimento foi ótimo e o monitor demonstrou bastante segurança no conteúdo.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[5],
                registration=alunos_ordenados[35].registration,
                type=MessageType.CRITICA,
                text="A organização do encontro poderia melhorar, principalmente na divisão do tempo.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[6],
                registration=alunos_ordenados[36].registration,
                type=MessageType.ELOGIO,
                text="A monitoria contribuiu para resolver dificuldades que eu tinha nos exercícios.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[7],
                registration=alunos_ordenados[37].registration,
                type=MessageType.SUGESTAO,
                text="Sugiro montar um roteiro com os tópicos abordados em cada encontro.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[8],
                registration=alunos_ordenados[38].registration,
                type=MessageType.ELOGIO,
                text="O monitor explicou os detalhes das questões e ajudou a entender a lógica da solução.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[9],
                registration=alunos_ordenados[39].registration,
                type=MessageType.CRITICA,
                text="A explicação foi útil, mas faltaram exemplos mais simples antes dos mais difíceis.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[10],
                registration=alunos_ordenados[40].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi muito atencioso e respondeu todas as dúvidas com clareza.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[11],
                registration=alunos_ordenados[41].registration,
                type=MessageType.SUGESTAO,
                text="Poderia haver uma lista de problemas recomendados para praticar em casa.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[12],
                registration=alunos_ordenados[42].registration,
                type=MessageType.ELOGIO,
                text="O encontro foi produtivo e bem focado nos conteúdos da disciplina.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[13],
                registration=alunos_ordenados[43].registration,
                type=MessageType.CRITICA,
                text="A monitoria foi boa, mas poderia ter mais tempo para acompanhar cada alunos.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[14],
                registration=alunos_ordenados[44].registration,
                type=MessageType.ELOGIO,
                text="As explicações foram bem estruturadas e ajudaram a fixar o conteúdo.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[15],
                registration=alunos_ordenados[45].registration,
                type=MessageType.SUGESTAO,
                text="Seria bom disponibilizar um resumo dos principais comandos e conceitos usados.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[16],
                registration=alunos_ordenados[46].registration,
                type=MessageType.ELOGIO,
                text="O monitor conseguiu explicar o raciocínio sem apenas mostrar a resposta final.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[17],
                registration=alunos_ordenados[47].registration,
                type=MessageType.CRITICA,
                text="A monitoria poderia ser mais organizada em relação à sequência dos assuntos.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[18],
                registration=alunos_ordenados[48].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi paciente e ajudou bastante na correção dos exercícios.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[19],
                registration=alunos_ordenados[49].registration,
                type=MessageType.SUGESTAO,
                text="Sugiro que as próximas monitorias tenham mais exercícios de revisão para prova.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[20],
                registration=alunos_ordenados[50].registration,
                type=MessageType.ELOGIO,
                text="A monitoria foi clara e ajudou a melhorar minha confiança na disciplina.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[21],
                registration=alunos_ordenados[51].registration,
                type=MessageType.CRITICA,
                text="O atendimento foi bom, mas algumas explicações ficaram muito resumidas.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[22],
                registration=alunos_ordenados[52].registration,
                type=MessageType.ELOGIO,
                text="O monitor usou exemplos práticos que facilitaram bastante o entendimento.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[23],
                registration=alunos_ordenados[53].registration,
                type=MessageType.SUGESTAO,
                text="Poderia haver um documento compartilhado com dúvidas frequentes da turma.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[24],
                registration=alunos_ordenados[54].registration,
                type=MessageType.ELOGIO,
                text="A explicação foi objetiva e ajudou a entender os pontos principais.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[25],
                registration=alunos_ordenados[55].registration,
                type=MessageType.CRITICA,
                text="A monitoria foi útil, mas seria melhor com uma organização prévia dos exercícios.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[26],
                registration=alunos_ordenados[56].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi muito solícito e explicou bem os erros mais comuns.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[27],
                registration=alunos_ordenados[57].registration,
                type=MessageType.SUGESTAO,
                text="Seria interessante fazer uma revisão rápida no começo de cada atendimento.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[28],
                registration=alunos_ordenados[58].registration,
                type=MessageType.ELOGIO,
                text="A monitoria ajudou muito na compreensão dos assuntos que eu tinha dificuldade.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[29],
                registration=alunos_ordenados[59].registration,
                type=MessageType.CRITICA,
                text="O ritmo da explicação poderia ser mais lento para acompanhar melhor.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[0],
                registration=alunos_ordenados[60].registration,
                type=MessageType.ELOGIO,
                text="O monitor respondeu às dúvidas de forma educada e clara.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[1],
                registration=alunos_ordenados[61].registration,
                type=MessageType.SUGESTAO,
                text="Poderiam ser propostos pequenos desafios para praticar depois da explicação.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[2],
                registration=alunos_ordenados[62].registration,
                type=MessageType.ELOGIO,
                text="A atividade foi bem conduzida e teve exemplos relevantes para a disciplina.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[3],
                registration=alunos_ordenados[63].registration,
                type=MessageType.CRITICA,
                text="A monitoria foi boa, mas faltou revisar alguns conceitos básicos antes dos exercícios.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[4],
                registration=alunos_ordenados[64].registration,
                type=MessageType.ELOGIO,
                text="O monitor explicou bem e ajudou a turma a entender os passos da solução.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[5],
                registration=alunos_ordenados[65].registration,
                type=MessageType.SUGESTAO,
                text="Seria bom deixar os horários de atendimento mais visíveis para os alunos_ordenados.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[6],
                registration=alunos_ordenados[66].registration,
                type=MessageType.ELOGIO,
                text="A monitoria foi proveitosa e contribuiu para o desenvolvimento das atividades.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[7],
                registration=alunos_ordenados[67].registration,
                type=MessageType.CRITICA,
                text="O atendimento foi útil, mas poderia ter mais espaço para dúvidas individuais.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[8],
                registration=alunos_ordenados[68].registration,
                type=MessageType.ELOGIO,
                text="O monitor mostrou domínio e explicou os conceitos de maneira acessível.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[9],
                registration=alunos_ordenados[69].registration,
                type=MessageType.SUGESTAO,
                text="Poderia haver uma pequena lista de exercícios ao final de cada monitoria.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[10],
                registration=alunos_ordenados[70].registration,
                type=MessageType.ELOGIO,
                text="A explicação foi clara e os exemplos foram bem escolhidos.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[11],
                registration=alunos_ordenados[71].registration,
                type=MessageType.CRITICA,
                text="A monitoria poderia começar com objetivos mais claros para o encontro.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[12],
                registration=alunos_ordenados[72].registration,
                type=MessageType.ELOGIO,
                text="O monitor ajudou a compreender melhor a resolução das questões.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[13],
                registration=alunos_ordenados[73].registration,
                type=MessageType.SUGESTAO,
                text="Seria interessante gravar ou registrar os principais pontos das monitorias.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[14],
                registration=alunos_ordenados[74].registration,
                type=MessageType.ELOGIO,
                text="A monitoria foi bastante útil e ajudou no acompanhamento da disciplina.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[15],
                registration=alunos_ordenados[75].registration,
                type=MessageType.CRITICA,
                text="A explicação foi boa, mas alguns exemplos ficaram sem conclusão detalhada.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[16],
                registration=alunos_ordenados[76].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi paciente e conseguiu adaptar a explicação às dúvidas da turma.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[17],
                registration=alunos_ordenados[77].registration,
                type=MessageType.SUGESTAO,
                text="Sugiro trazer exemplos parecidos com os trabalhos avaliativos.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[18],
                registration=alunos_ordenados[78].registration,
                type=MessageType.ELOGIO,
                text="O atendimento foi organizado e ajudou a tirar dúvidas importantes.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[19],
                registration=alunos_ordenados[79].registration,
                type=MessageType.CRITICA,
                text="A monitoria contribuiu, mas poderia ter uma dinâmica mais participativa.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[20],
                registration=alunos_ordenados[80].registration,
                type=MessageType.ELOGIO,
                text="O monitor explicou muito bem e ajudou a entender os conceitos difíceis.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[21],
                registration=alunos_ordenados[81].registration,
                type=MessageType.SUGESTAO,
                text="Poderia ser feita uma revisão dos erros comuns antes das avaliações.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[22],
                registration=alunos_ordenados[82].registration,
                type=MessageType.ELOGIO,
                text="A monitoria foi clara, bem planejada e muito útil para os exercícios.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[23],
                registration=alunos_ordenados[83].registration,
                type=MessageType.CRITICA,
                text="O tempo foi curto para a quantidade de dúvidas apresentadas pela turma.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[24],
                registration=alunos_ordenados[84].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi atencioso e explicou bem os pontos que causavam confusão.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[25],
                registration=alunos_ordenados[85].registration,
                type=MessageType.SUGESTAO,
                text="Seria bom ter um cronograma com os temas de cada semana.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[26],
                registration=alunos_ordenados[86].registration,
                type=MessageType.ELOGIO,
                text="O atendimento foi excelente e as dúvidas foram respondidas com paciência.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[27],
                registration=alunos_ordenados[87].registration,
                type=MessageType.CRITICA,
                text="A monitoria foi produtiva, mas faltou aprofundar algumas questões mais difíceis.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[28],
                registration=alunos_ordenados[88].registration,
                type=MessageType.ELOGIO,
                text="A explicação ajudou a corrigir erros e melhorar a solução dos exercícios.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[29],
                registration=alunos_ordenados[89].registration,
                type=MessageType.SUGESTAO,
                text="Poderiam ser disponibilizados exercícios extras com gabarito comentado.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[0],
                registration=alunos_ordenados[90].registration,
                type=MessageType.ELOGIO,
                text="O monitor conduziu bem o encontro e explicou com bastante clareza.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[1],
                registration=alunos_ordenados[91].registration,
                type=MessageType.CRITICA,
                text="O encontro foi útil, mas poderia ter mais exemplos aplicados.",
                rating=3,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[2],
                registration=alunos_ordenados[92].registration,
                type=MessageType.ELOGIO,
                text="A monitoria ajudou bastante na preparação para as atividades da disciplina.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[3],
                registration=alunos_ordenados[93].registration,
                type=MessageType.SUGESTAO,
                text="Seria interessante abrir um espaço fixo para dúvidas sobre listas e trabalhos.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[4],
                registration=alunos_ordenados[94].registration,
                type=MessageType.ELOGIO,
                text="O monitor foi claro nas explicações e manteve boa comunicação com a turma.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[5],
                registration=alunos_ordenados[95].registration,
                type=MessageType.CRITICA,
                text="Algumas explicações ficaram corridas e dificultaram acompanhar a lógica.",
                rating=2,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[6],
                registration=alunos_ordenados[96].registration,
                type=MessageType.ELOGIO,
                text="A monitoria foi muito boa e ajudou a entender melhor a matéria.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[7],
                registration=alunos_ordenados[97].registration,
                type=MessageType.SUGESTAO,
                text="Poderia haver um material de apoio com os principais tópicos revisados.",
                rating=4,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[8],
                registration=alunos_ordenados[98].registration,
                type=MessageType.ELOGIO,
                text="O monitor demonstrou paciência e conseguiu explicar de formas diferentes.",
                rating=5,
            ),
            Feedback(
                assignment=alocacoes_ordenadas[9],
                registration=alunos_ordenados[99].registration,
                type=MessageType.CRITICA,
                text="A monitoria foi positiva, mas poderia ter melhor controle do tempo.",
                rating=3,
            ),
        ]
        await Feedback.insert_many(feedbacks)

        print("Carga de dados no MongoDB concluída com sucesso!")

    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Erro ao carregar dados: {e}")


if __name__ == "__main__":
    asyncio.run(seed_data())
