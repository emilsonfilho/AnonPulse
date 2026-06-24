import asyncio
from datetime import datetime, timezone, timedelta
from fastapi_pagination import Params

from app.core.database import init_db, close_db
from app.core.enums import MessageType

# Importação de todas as Entidades
from app.models import (
    Subject,
    Professor,
    Classroom,
    Student,
    Enrollment,
    Monitor,
    MonitorAssignment,
    Feedback,
    DocumentMetadata,
)

# Importação de todos os Repositórios
from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.monitor_repository import MonitorRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.document_repository import DocumentRepository


async def run_massive_tests():
    print("🚀 INICIANDO TESTE MASSIVO DO ECOSSISTEMA ANONPULSE 🚀\n")

    print("🔌 1. Inicializando MongoDB (Beanie)...")
    await init_db(
        [
            Subject,
            Professor,
            Classroom,
            Student,
            Enrollment,
            Monitor,
            MonitorAssignment,
            Feedback,
            DocumentMetadata,
        ]
    )

    print("🧹 2. Limpando a base de dados (Clean Slate)...")
    for model in [
        Subject,
        Professor,
        Classroom,
        Student,
        Enrollment,
        Monitor,
        MonitorAssignment,
        Feedback,
        DocumentMetadata,
    ]:
        await model.find_all().delete()

    # ==========================================
    # FASE 1: POPULAR O BANCO DE DADOS (SEED)
    # ==========================================
    print("\n🌱 3. FASE DE CRIAÇÃO (Gerando Massa de Dados)...")

    # --- Professores e Disciplinas ---
    prof1 = await Professor(name="Arthur Araruna", email="araruna@ufc.br").insert()
    prof2 = await Professor(name="João Silva", email="joao@ufc.br").insert()

    subj1 = await Subject(cod="QXD001", name="Estrutura de Dados").insert()
    subj2 = await Subject(cod="QXD002", name="Banco de Dados").insert()

    # --- Turmas ---
    class1 = await Classroom(cod="ED-T01", subject=subj1, professor=prof1).insert()
    class2 = await Classroom(cod="BD-T01", subject=subj2, professor=prof2).insert()

    # --- Estudantes e Matrículas ---
    student1 = await Student(registration="111111").insert()
    student2 = await Student(registration="222222").insert()
    student3 = await Student(registration="333333").insert()

    await Enrollment(student=student1, classroom=class1).insert()
    await Enrollment(student=student2, classroom=class1).insert()
    await Enrollment(student=student3, classroom=class2).insert()

    # --- Monitores e Alocações ---
    monitor1 = await Monitor(
        registration="494912", name="Francisco Emilson", email="emilson@ufc.br"
    ).insert()
    monitor2 = await Monitor(
        registration="999999", name="Ana Laura", email="ana@ufc.br"
    ).insert()

    assign1 = await MonitorAssignment(
        weekly_hours=12, monitor=monitor1, classroom=class1
    ).insert()
    assign2 = await MonitorAssignment(
        weekly_hours=8, monitor=monitor2, classroom=class2
    ).insert()

    # --- Documentos ---
    await DocumentMetadata(
        original_filename="arvores_avl.pdf",
        content_type="application/pdf",
        extension=".pdf",
        size_bytes=2048,
        assignment=assign1,
    ).insert()
    await DocumentMetadata(
        original_filename="lichao_tree.pdf",
        content_type="application/pdf",
        extension=".pdf",
        size_bytes=1024,
        assignment=assign1,
    ).insert()
    await DocumentMetadata(
        original_filename="sql_basico.pdf",
        content_type="application/pdf",
        extension=".pdf",
        size_bytes=512,
        assignment=assign2,
    ).insert()

    # --- Feedbacks ---
    hoje = datetime.now(timezone.utc)
    ontem = hoje - timedelta(days=1)

    await Feedback(
        registration="hash_111",
        text="A apostila de AVL é excelente!",
        rating=5,
        type=MessageType.ELOGIO,
        assignment=assign1,
        created_at=hoje,
    ).insert()
    await Feedback(
        registration="hash_222",
        text="Tenho dúvida sobre Li-Chao, pode ajudar?",
        rating=3,
        type=MessageType.DUVIDA,
        assignment=assign1,
        created_at=ontem,
    ).insert()
    await Feedback(
        registration="hash_333",
        text="O material de SQL está incompleto.",
        rating=2,
        type=MessageType.CRITICA,
        assignment=assign2,
        created_at=hoje,
    ).insert()

    print("✅ Massa de dados gerada com sucesso!")

    # ==========================================
    # FASE 2: BATERIA DE TESTES NOS REPOSITÓRIOS
    # ==========================================
    print("\n🔬 4. FASE DE TESTES DOS REPOSITÓRIOS...")
    params = Params(page=1, size=50)

    # --- Teste de Contagem (BaseRepository) ---
    print("\n📊 Testando BaseRepository (Contagem total):")
    print(f"   -> Estudantes: {await StudentRepository().count()}")
    print(f"   -> Matrículas: {await EnrollmentRepository().count()}")
    print(f"   -> Monitores: {await MonitorRepository().count()}")

    # --- Testes de ClassroomRepository ---
    print("\n🏫 Testando ClassroomRepository:")
    turmas_araruna = await ClassroomRepository().list_by_professor(prof1.id, params)
    print(f"   -> Turmas do Prof. Araruna: {[t.cod for t in turmas_araruna.items]}")

    turmas_ed = await ClassroomRepository().list_by_subject("QXD001", params)
    print(f"   -> Turmas da disciplina ED (QXD001): {[t.cod for t in turmas_ed.items]}")

    # --- Testes de DocumentRepository ---
    print("\n📄 Testando DocumentRepository:")
    docs_emilson = await DocumentRepository().list_by_assignment(assign1.id, params)
    print(
        f"   -> Documentos da Alocação 1: {[d.original_filename for d in docs_emilson.items]}"
    )

    # --- Testes de FeedbackRepository (O Boss Final) ---
    print("\n💬 Testando FeedbackRepository (Consultas Complexas):")
    repo_fb = FeedbackRepository()

    # 1. Busca por Texto (Regex)
    fb_text = await repo_fb.search_by_text("excelente", params)
    print(
        f"   -> Busca textual ('excelente'): Encontrou {len(fb_text.items)} feedback(s)."
    )

    # 2. Busca por Monitor (JOIN)
    fb_monitor = await repo_fb.list_by_monitor(monitor1.registration, params)
    print(
        f"   -> Feedbacks para o Monitor {monitor1.registration}: {len(fb_monitor.items)} encontrados."
    )

    # 3. Hash do Aluno
    fb_hash = await repo_fb.list_by_student_hash("hash_111", params)
    print(
        f"   -> Feedbacks do aluno anónimo (hash_111): {[f.text for f in fb_hash.items]}"
    )

    # 4. Agrupamento por Monitor (Pipeline)
    count_mon = await repo_fb.count_by_monitor(params)
    print("   -> Contagem de Feedbacks por Monitor (Agregação):")
    for item in count_mon.items:
        print(
            f"      - Monitor: {item.get('monitor_registration')}, Total: {item.get('count')}"
        )

    # 5. Agrupamento por Disciplina (Super Pipeline Múltiplo)
    count_sub = await repo_fb.count_by_subject(params)
    print("   -> Contagem de Feedbacks por Disciplina (Agregação 4 Níveis):")
    for item in count_sub.items:
        print(
            f"      - Disciplina: {item.get('subject_name')}, Total: {item.get('feedback_count')}"
        )

    # 6. Filtro por Data
    fb_datas = await repo_fb.list_by_date_range(
        params, start_date=hoje - timedelta(hours=1)
    )
    print(f"   -> Feedbacks recebidos hoje: {len(fb_datas.items)} encontrados.")

    print("\n🔌 5. Fechando conexões...")
    await close_db()
    print("🏆 TESTE MASSIVO CONCLUÍDO COM SUCESSO! 🏆")


if __name__ == "__main__":
    asyncio.run(run_massive_tests())
