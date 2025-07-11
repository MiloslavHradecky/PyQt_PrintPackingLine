# 🖨️ PyQt_PrintPackingLine

Qt-based desktop app for smart label printing and data parsing using custom triggers and file mappings.

---

## 🇬🇧 Description (EN)

**PrintPackingLine** is a PyQt6-powered desktop application for managing label generation, parsing serial numbers, and triggering custom printing flows using BarTender.  
Supports structured file formats (`.lbl`, `.nor`), dynamic config mapping (`.ini`) and token extraction for secure labels (My2N).

### ✨ Features

- Serial number input and format validation
- Label extraction (B/D/E rows) and extended trigger logic (I/J/K rows for C4-SMART products)
- Config-driven mapping of product triggers
- Automatic file generation for BarTender integration
- Separate file outputs for main product and C4 product variants
- Token scanning with My2N security output
- UI optimized with custom styles and dynamic scaling

---

## 🇨🇿 Popis (CZ)

**PrintPackingLine** je desktopová aplikace založená na PyQt6, určená pro správu tisku etiket, zpracování sériových čísel a řízené spuštění tiskových procesů pomocí BarTender.  
Podporuje strukturované formáty souborů (`.lbl`, `.nor`), konfiguraci přes `.ini` soubor a extrakci bezpečnostních tokenů pro štítky typu My2N.

### ✨ Funkce

- Zadání a validace sériového čísla (formát `00-0000-0000`)
- Načítání etiket z řádků B/D/E, rozšířená logika pro I/J/K řádky (produkty C4-SMART)
- Mapování produktových spouštěčů pomocí konfigurace
- Automatické generování souborů pro BarTender Commander
- Oddělený výstup souborů pro hlavní produkt i variantu C4
- Detekce tokenu s výstupem bezpečnostního kódu My2N
- Stylované uživatelské rozhraní s dynamickým měřítkem

---

## 🚀 Technologies

- **Python 3.10+**
- **PyQt6**
- **BarTender Commander Integration**
- **ConfigParser**
- **Regex / File I/O**

---

## 📂 Structure

```
📦 PrintPackingLine/
├── .idea/
├── build/
├── controllers/
├── core/
├── dist/
├── effects/
├── info/
├── log/
├── resources/
│   └── ico/
├── setup/
├── utils/
├── views/
├── .gitignore
├── LICENSE
├── LineB
├── main
├── README
└── version
```

---

## 🧑‍💻 Author

Developed with 💙 and precision by [Miloslav Hradecky]  
© 2025 — Built to print, parse & simplify 🎉

