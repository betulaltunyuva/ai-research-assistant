from langgraph.graph import StateGraph, START, END

from state import ResearchState
from config import MODEL_NAME

from agents.researcher import researcher_agent
from agents.analyst import analyst_agent
from agents.writer import writer_agent
from agents.verifier import verifier_agent

from utils.report_saver import save_report, save_history
from utils.system_check import check_ollama

from utils.conversation_memory import (
    init_memory,
    save_message,
    get_recent_messages,
    save_research,
    get_last_research
)

from settings import PROJECT_NAME, MAX_REVISIONS
import time



def route_after_verification(state: ResearchState):
    verification = state.get(
        "verification_report",
        ""
    )

    revision_count = state.get(
        "revision_count",
        0
    )

    if "DURUM: UYGUN" in verification.upper():
        return "end"

    if revision_count >= MAX_REVISIONS:
        return "end"

    return "revise"


workflow = StateGraph(ResearchState)

workflow.add_node(
    "researcher",
    researcher_agent
)

workflow.add_node(
    "analyst",
    analyst_agent
)

workflow.add_node(
    "writer",
    writer_agent
)

workflow.add_node(
    "verifier",
    verifier_agent
)


workflow.add_edge(
    START,
    "researcher"
)

workflow.add_edge(
    "researcher",
    "analyst"
)

workflow.add_edge(
    "analyst",
    "writer"
)

workflow.add_edge(
    "writer",
    "verifier"
)


workflow.add_conditional_edges(
    "verifier",
    route_after_verification,
    {
        "revise": "writer",
        "end": END
    }
)


app = workflow.compile()


if __name__ == "__main__":
    init_memory()
    
    print(f"=== {PROJECT_NAME} ===")

    ollama_ready, message = check_ollama(
        MODEL_NAME
    )

    if not ollama_ready:
        print("\n[Sistem Hatası]")
        print(message)

    else:
        query = ""
        result = {}
        start_time = None

        try:
            session_id = input(
                "\nOturum adı yazın "
                "(örnek: network-01, boş bırakırsanız default): "
            ).strip()

            if not session_id:
                session_id = "default"

            print(
                f"\nAktif oturum: {session_id}"
            )
            # 1. Önce araştırma konusunu sor
            query = input(
                "\nAraştırmak istediğiniz konuyu yazın: "
            ).strip()

            if not query:
                print(
                    "\nAraştırma konusu boş bırakılamaz."
                )

            else:
                recent_messages = get_recent_messages(
                    session_id=session_id,
                    limit=6
                )

                last_research = get_last_research(
                    session_id=session_id
                )

                conversation_history = ""

                for message in recent_messages:
                    conversation_history += (
                        f"{message['role']}: "
                        f"{message['content']}\n"
                    )

                previous_research = ""

                if last_research:
                    previous_research = (
                        f"Önceki araştırma konusu:\n"
                        f"{last_research['query']}\n\n"
                        f"Önceki cevap:\n"
                        f"{last_research['final_answer']}"
                    )

                document_path = input(
                    "\nBelge kullanmak istiyorsanız dosya yolunu yazın "
                    "(kullanmayacaksanız Enter): "
                ).strip()
                start_time = time.perf_counter()

                # 3. Multi-agent sistemi çalıştır
                result = app.invoke({
                    "query": query,
                    "session_id": session_id,
                    "document_path": document_path,
                    "conversation_history": conversation_history,
                    "previous_research": previous_research,
                    "revision_count": 0
                })

                duration_seconds = (
                    time.perf_counter() - start_time
                )

                print("\n" + "=" * 60)
                print("NİHAİ ARAŞTIRMA RAPORU")
                print("=" * 60)

                print(
                    result.get(
                        "final_answer",
                        ""
                    )
                )

                print("\n" + "=" * 60)
                print("DOĞRULAMA RAPORU")
                print("=" * 60)

                print(
                    result.get(
                        "verification_report",
                        ""
                    )
                )

                print(
                    "\nYapılan otomatik düzeltme sayısı:",
                    result.get(
                        "revision_count",
                        0
                    )
                )

                print(
                    "\nKullanılan web kaynak sayısı:",
                    len(
                        result.get(
                            "sources",
                            []
                        )
                    )
                )

                print(
                    f"Toplam araştırma süresi: "
                    f"{duration_seconds:.2f} saniye"
                )

                verification_text = result.get(
                    "verification_report",
                    ""
                ).upper()

                if "DURUM: UYGUN" in verification_text:
                    result["final_status"] = "DOĞRULANDI"
                else:
                    result["final_status"] = (
                        "İNSAN İNCELEMESİ GEREKLİ"
                    )

                report_path = save_report(
                    query,
                    result,
                    duration_seconds
                )

                print("\nRapor kaydedildi:")
                print(report_path)
                save_message(
                    "user",
                    query,
                    session_id=session_id
                )

                save_message(
                    "assistant",
                    result.get(
                        "final_answer",
                        ""
                    ),
                    session_id=session_id
                )

                save_research(
                    query=query,
                    final_answer=result.get(
                        "final_answer",
                        ""
                    ),
                    sources=result.get(
                        "sources",
                        []
                    ),
                    document_path=document_path,
                    session_id=session_id
                )


        except KeyboardInterrupt:
            print(
                "\n\nİşlem kullanıcı tarafından durduruldu."
            )

        except Exception as e:
            print("\n[Program Hatası]")
            print("Araştırma tamamlanamadı.")
            print(f"Hata ayrıntısı: {e}")

            if start_time is not None:
                duration_seconds = (
                    time.perf_counter() - start_time
                )
            else:
                duration_seconds = 0

            save_history(
                query=query,
                status="failed",
                duration_seconds=duration_seconds,
                error=str(e)
            )