import os
import sys
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_IDS = [c.strip() for c in os.environ.get("CHAT_IDS", "").split(",") if c.strip()]

SITIO = "https://www.maquillajetrendyshop.com/"
API = SITIO + "api/catalog_system/pub/products/search?ft="

# Palabras que se buscan en los productos de la tienda
BUSQUEDAS = ["adviento"]

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
    for termino in BUSQUEDAS:
        r = requests.get(API + termino, headers=HEADERS, timeout=30)
        r.raise_for_status()
        productos = r.json()
        print(f"Búsqueda '{termino}': {len(productos)} productos")
        if len(productos) > 0:
            return True
    return False


def main():
    faltan = []
    if not BOT_TOKEN:
        faltan.append("BOT_TOKEN")
    if not CHAT_IDS:
        faltan.append("CHAT_IDS")
    if faltan:
        print("Faltan:", ", ".join(faltan))
        sys.exit(1)

    if "--test" in sys.argv:
        enviar_telegram("Prueba del bot de Trendy desde GitHub ✅")
        return

    if ya_salio():
        enviar_telegram(
            "💄✨ ¡Ya salió el calendario de adviento de Trendy! "
            "Corre a verlo antes de que se agote:\n"
            + SITIO + "adviento?_q=adviento&map=ft"
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
