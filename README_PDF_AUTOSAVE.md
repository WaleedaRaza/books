# PDF Tab Saver Macro

Simple keyboard macro that does exactly what you do manually:
**Ctrl+S → Enter → Ctrl+W** (repeat)

---

## 🚀 Quick Start

```bash
# Install pyautogui (one-time)
pip install pyautogui

# Run the macro
python save_pdf_macro.py
```

---

## 📋 How It Works

1. **Open all PDF tabs** in Chrome
2. **Click on the FIRST PDF tab**
3. **Run the script**
4. It simulates:
   - `Ctrl+S` (save)
   - `Enter` (confirm)
   - `Ctrl+W` (close tab)
   - Repeats for each tab

That's it. No fancy stuff.

---

## ⚠️ Important

- **Keep Chrome window active** while script runs
- **Don't move mouse/keyboard** during execution
- **Make sure save location is set** (default Downloads folder)
- **Test with 2-3 tabs first** before doing hundreds

---

## 💡 Tips

- If save dialog appears, make sure default location is set
- Script pauses 0.5 seconds between actions (adjustable)
- Press `Ctrl+C` to stop if needed
- PDFs save to your default Downloads folder

---

## 🔧 Customize

Edit `save_pdf_macro.py` to adjust:
- `delay_between_actions` - speed of macro (default 0.5s)
- Save location (set Chrome's default download folder)

---

**Simple. Effective. Done.** ✅

