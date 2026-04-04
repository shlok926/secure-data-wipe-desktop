"""
translations.py - Multi-Language Support for Secure Wipe
Supports: English, Hindi (हिंदी), Spanish, and more
"""

# ─── Language Definitions ─────────────────────────────────────────
LANGUAGES = {
    "🇬🇧 English":           "en",
    "🇮🇳 हिंदी (Hindi)":     "hi",
    "🇪🇸 Español (Spanish)": "es",
    "🇫🇷 Français (French)": "fr",
    "🇩🇪 Deutsch (German)":  "de",
}

# ─── Translation Strings ──────────────────────────────────────────
TRANSLATIONS = {
    # ── Sidebar / Navigation ──────────────────────────────────────
    "nav_dashboard":   {"en": "🏠 Dashboard",       "hi": "🏠 डैशबोर्ड",       "es": "🏠 Panel",         "fr": "🏠 Tableau de bord", "de": "🏠 Übersicht"},
    "nav_wipe":        {"en": "🗑️ Secure Wipe",     "hi": "🗑️ सुरक्षित डिलीट", "es": "🗑️ Borrado Seguro","fr": "🗑️ Effacement",      "de": "🗑️ Sicheres Löschen"},
    "nav_free_space":  {"en": "🚀 Free Space Wiper", "hi": "🚀 फ्री स्पेस वाइपर", "es": "🚀 Espacio Libre", "fr": "🚀 Espace Libre", "de": "🚀 Freier Speicher"},
    "nav_audit":       {"en": "📋 Audit Logs",       "hi": "📋 ऑडिट लॉग",        "es": "📋 Registros",     "fr": "📋 Journaux",         "de": "📋 Protokolle"},
    "nav_settings":    {"en": "⚙️ Settings",         "hi": "⚙️ सेटिंग्स",        "es": "⚙️ Ajustes",      "fr": "⚙️ Paramètres",      "de": "⚙️ Einstellungen"},
    "nav_about":       {"en": "ℹ️ About",             "hi": "ℹ️ जानकारी",          "es": "ℹ️ Acerca de",    "fr": "ℹ️ À propos",         "de": "ℹ️ Über"},
    "nav_admin":       {"en": "🔧 Admin Panel",       "hi": "🔧 एडमिन पैनल",      "es": "🔧 Panel Admin",  "fr": "🔧 Panneau Admin",    "de": "🔧 Adminbereich"},
    "nav_monitoring":  {"en": "📊 Monitoring",        "hi": "📊 मॉनिटरिंग",       "es": "📊 Monitoreo",    "fr": "📊 Surveillance",     "de": "📊 Überwachung"},
    "nav_tamper":      {"en": "🔒 Secure Audit",      "hi": "🔒 सुरक्षित ऑडिट",   "es": "🔒 Auditoría",    "fr": "🔒 Audit Sécurisé",   "de": "🔒 Sicheres Audit"},
    "nav_batch":       {"en": "⚡ Batch Wipe",        "hi": "⚡ बैच वाइप",         "es": "⚡ Lote",          "fr": "⚡ Lot",               "de": "⚡ Stapel"},
    "nav_network":     {"en": "🌐 Network Wipe",      "hi": "🌐 नेटवर्क वाइप",    "es": "🌐 Red",           "fr": "🌐 Réseau",            "de": "🌐 Netzwerk"},

    # ── Page Titles ───────────────────────────────────────────────
    "page_dashboard":  {"en": "Dashboard",        "hi": "डैशबोर्ड",         "es": "Panel",          "fr": "Tableau de bord", "de": "Übersicht"},
    "page_wipe":       {"en": "Secure File Wipe", "hi": "सुरक्षित फ़ाइल डिलीट", "es": "Borrado Seguro", "fr": "Effacement Sécurisé", "de": "Sicheres Löschen"},
    "page_audit":      {"en": "Audit Logs",       "hi": "ऑडिट लॉग",          "es": "Registros",      "fr": "Journaux d'Audit", "de": "Protokolle"},
    "page_settings":   {"en": "Settings",         "hi": "सेटिंग्स",           "es": "Ajustes",        "fr": "Paramètres", "de": "Einstellungen"},
    "page_about":      {"en": "About Secure Wipe","hi": "Secure Wipe के बारे में", "es": "Acerca de", "fr": "À propos", "de": "Über Secure Wipe"},

    # ── Wipe Page ─────────────────────────────────────────────────
    "select_file":     {"en": "Select File to Wipe:", "hi": "डिलीट करने के लिए फ़ाइल चुनें:", "es": "Seleccionar archivo:", "fr": "Sélectionner un fichier:", "de": "Datei auswählen:"},
    "no_file":         {"en": "No file selected...",   "hi": "कोई फ़ाइल नहीं चुनी...",          "es": "Sin archivo...",       "fr": "Aucun fichier...",        "de": "Keine Datei..."},
    "browse":          {"en": "📁 Browse",              "hi": "📁 ब्राउज़",                    "es": "📁 Navegar",            "fr": "📁 Parcourir",            "de": "📁 Durchsuchen"},
    "algorithm":       {"en": "Wiping Algorithm:",     "hi": "वाइपिंग एल्गोरिदम:",              "es": "Algoritmo:",            "fr": "Algorithme:",             "de": "Algorithmus:"},
    "start_wipe":      {"en": "🗑️ START SECURE WIPE",  "hi": "🗑️ सुरक्षित डिलीट शुरू करें",    "es": "🗑️ INICIAR BORRADO",    "fr": "🗑️ DÉMARRER L'EFFACEMENT","de": "🗑️ LÖSCHEN STARTEN"},
    "cancel":          {"en": "Cancel",                "hi": "रद्द करें",                      "es": "Cancelar",             "fr": "Annuler",                 "de": "Abbrechen"},
    "ready":           {"en": "Ready to wipe",        "hi": "वाइप करने के लिए तैयार",            "es": "Listo para borrar",    "fr": "Prêt à effacer",          "de": "Bereit zum Löschen"},
    "progress":        {"en": "Operation Progress:",  "hi": "ऑपरेशन प्रगति:",                  "es": "Progreso:",            "fr": "Progression:",            "de": "Fortschritt:"},

    # ── Dialogs ───────────────────────────────────────────────────
    "confirm_wipe":    {"en": "Confirm Wipe Operation",  "hi": "वाइप की पुष्टि करें",           "es": "Confirmar Borrado",    "fr": "Confirmer l'Effacement",  "de": "Löschung bestätigen"},
    "yes":             {"en": "Yes",                     "hi": "हाँ",                           "es": "Sí",                   "fr": "Oui",                     "de": "Ja"},
    "no":              {"en": "No",                      "hi": "नहीं",                          "es": "No",                   "fr": "Non",                     "de": "Nein"},
    "success":         {"en": "✅ Success",               "hi": "✅ सफलता",                      "es": "✅ Éxito",               "fr": "✅ Succès",                "de": "✅ Erfolg"},
    "error":           {"en": "❌ Error",                 "hi": "❌ त्रुटि",                      "es": "❌ Error",               "fr": "❌ Erreur",                "de": "❌ Fehler"},

    # ── Settings ──────────────────────────────────────────────────
    "settings_general": {"en": "General Settings",        "hi": "सामान्य सेटिंग्स",       "es": "Config. General",  "fr": "Paramètres Généraux", "de": "Allgemeine Einstellungen"},
    "settings_security":{"en": "Security & Confirmation", "hi": "सुरक्षा और पुष्टि",       "es": "Seguridad",        "fr": "Sécurité",            "de": "Sicherheit"},
    "settings_save":    {"en": "💾 Save Settings",         "hi": "💾 सेटिंग्स सहेजें",      "es": "💾 Guardar",        "fr": "💾 Enregistrer",      "de": "💾 Speichern"},
    "settings_reset":   {"en": "🔄 Reset to Defaults",    "hi": "🔄 डिफ़ॉल्ट पर रीसेट करें","es": "🔄 Restablecer",   "fr": "🔄 Réinitialiser",   "de": "🔄 Zurücksetzen"},

    # ── Audit ─────────────────────────────────────────────────────
    "export_logs":     {"en": "📄 Export Logs",  "hi": "📄 लॉग निर्यात करें", "es": "📄 Exportar",   "fr": "📄 Exporter",  "de": "📄 Exportieren"},
    "timestamp":       {"en": "Timestamp",       "hi": "समय",                "es": "Fecha/Hora",  "fr": "Horodatage",  "de": "Zeitstempel"},
    "file_path":       {"en": "File Path",       "hi": "फ़ाइल पथ",            "es": "Ruta",        "fr": "Chemin",       "de": "Dateipfad"},
    "status":          {"en": "Status",          "hi": "स्थिति",              "es": "Estado",      "fr": "Statut",       "de": "Status"},
    "duration":        {"en": "Duration",        "hi": "अवधि",               "es": "Duración",    "fr": "Durée",        "de": "Dauer"},
}


# ─── Translator Class ─────────────────────────────────────────────

class Translator:
    """Global translator singleton – call t('key') to get translated string."""

    _lang_code = "en"  # default

    @classmethod
    def set_language(cls, display_name: str):
        """Set language by the display name shown in the combo box."""
        cls._lang_code = LANGUAGES.get(display_name, "en")
        print(f"[i18n] Language set to: {cls._lang_code}")

    @classmethod
    def t(cls, key: str, fallback: str = "") -> str:
        """Translate a key to the currently active language."""
        entry = TRANSLATIONS.get(key, {})
        return entry.get(cls._lang_code) or entry.get("en") or fallback or key

    @classmethod
    def get_nav_items(cls) -> list:
        """Return sidebar navigation labels in the current language."""
        keys = [
            "nav_dashboard", "nav_wipe", "nav_free_space", "nav_audit", "nav_settings",
            "nav_about", "nav_admin", "nav_monitoring", "nav_tamper",
            "nav_batch", "nav_network",
        ]
        return [cls.t(k) for k in keys]


# Convenience shortcut
_T = Translator()


def t(key: str, fallback: str = "") -> str:
    """Module-level translate shortcut."""
    return Translator.t(key, fallback)
