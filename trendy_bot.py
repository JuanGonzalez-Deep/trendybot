import os
import sys
import requests

BOT_TOKEN = os.environ.get("8672935024:AAGjgpWr3Hzr0wdOaANMFreWFFVauAX4Sdw")
CHAT_IDS = [c.strip() for c in os.environ.get("6989441799","8800326037").split(",") if c.strip()]
URL = os.environ.get("https://www.maquillajetrendyshop.com/")

# Palabras que indican que ya salió (en minúsculas)
KEYWORDS = ["adviento", "advent"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def enviar_telegram(texto):
    for chat_id in CHAT_IDS:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": chat_id, "text": texto},
            timeout=20,
        )
        if not r.ok:
            print(f"Error enviando a {chat_id}: {r.status_code}")


def ya_salio():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    html = r.text.lower()
    return any(k in html for k in KEYWORDS)


def main():
    faltan = []
    if not BOT_TOKEN:
        faltan.append("BOT_TOKEN")
    if not CHAT_IDS:
        faltan.append("CHAT_IDS")
    if not URL:
        faltan.append("TRENDY_URL")
    if faltan:
        print("Faltan:", ", ".join(faltan))
        sys.exit(1)

    if "--test" in sys.argv:
        enviar_telegram("Prueba del bot de Trendy desde GitHub ✅")
        return

    if ya_salio():
        enviar_telegram(
            "💄✨ ¡Ya salió el calendario de adviento de Trendy! "
            "Corre a verlo antes de que se agote:\n" + URL
        )
        print("¡Detectado! Aviso enviado.")
        salida = os.environ.get("GITHUB_OUTPUT")
        if salida:
            with open(salida, "a") as f:
                f.write("found=true\n")
    else:
        print("Todavía no está el calendario.")


if __name__ == "__main__":
    main()
