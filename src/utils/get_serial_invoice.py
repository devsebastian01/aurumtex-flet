import os
from dotenv import load_dotenv

load_dotenv()

ENV_PATH = ".env"

def get_and_increment_invoice_serial():
    current = int(os.getenv("INVOICE_SERIAL", "1000"))
    new_value = current + 1

    # Actualizar archivo .env
    with open(ENV_PATH, "r") as f:
        lines = f.readlines()

    with open(ENV_PATH, "w") as f:
        found = False
        for line in lines:
            if line.startswith("INVOICE_SERIAL="):
                f.write(f"INVOICE_SERIAL={new_value}\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f"INVOICE_SERIAL={new_value}\n")

    # Actualizar variable global para siguientes lecturas
    os.environ["INVOICE_SERIAL"] = str(new_value)

    return current
