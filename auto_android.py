import subprocess
import os

# CONFIGURACIÓN
APK_OFICIAL = "GooglePay.apk"  # Ruta local a tu APK
FIRMA_VALIDA = "AB:CD:EF:..."  # Pega aquí la firma SHA-256 real que obtuviste
PAQUETE = "com.google.android.apps.nbu.paisa.user"
APK_SIGNER = "/ruta/completa/a/apksigner"  # Ajusta esta ruta

def obtener_ruta_apk(package):
    result = subprocess.run(["adb", "shell", "pm", "path", package], capture_output=True, text=True)
    if "package:" in result.stdout:
        return result.stdout.strip().split(":")[1]
    return None

def extraer_apk_dispositivo(ruta_remota, ruta_local):
    subprocess.run(["adb", "pull", ruta_remota, ruta_local], check=True)
    return ruta_local

def obtener_firma(apk_path):
    cmd = [APK_SIGNER, "verify", "--verbose", apk_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    for linea in result.stdout.splitlines():
        if "SHA-256 digest" in linea:
            return linea.split(":")[-1].strip()
    return None

def reemplazar_app():
    print("❌ Firma inválida. Reinstalando APK...")
    subprocess.run(["adb", "uninstall", PAQUETE], check=True)
    subprocess.run(["adb", "install", APK_OFICIAL], check=True)
    print("✅ Reemplazo completado con la versión legítima.")

def main():
    ruta_remota = obtener_ruta_apk(PAQUETE)
    if not ruta_remota:
        print("📦 La app no está instalada.")
        return

    print(f"📤 Extrayendo APK de: {ruta_remota}")
    extraido = extraer_apk_dispositivo(ruta_remota, "extraido.apk")
    firma_actual = obtener_firma("extraido.apk")

    print(f"🔍 Firma obtenida: {firma_actual}")
    print(f"🔒 Firma esperada: {FIRMA_VALIDA}")

    if firma_actual != FIRMA_VALIDA:
        reemplazar_app()
    else:
        print("✅ La app ya es legítima.")

if __name__ == "__main__":
    main()
