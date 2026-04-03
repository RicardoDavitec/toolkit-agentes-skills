from datetime import datetime

CHECKLIST = [
    "Objetivo e escopo confirmados",
    "Guardrails hexagonal verificados",
    "Contratos de portas/adaptadores checados",
    "Caso de uso revisado",
    "Implementacao validada com testes",
    "Gate de release avaliado",
    "Documentacao de sessao atualizada",
    "Encerramento de sessao executado",
]


def main() -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Checklist de fluxo orquestrado - {ts}")
    for idx, item in enumerate(CHECKLIST, start=1):
        print(f"[{idx}] {item}")


if __name__ == "__main__":
    main()
