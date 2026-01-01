# Wave Import System - Testing Guide

## ✅ System Status

**Server:** http://localhost:5000  
**Parser:** ✅ Working (parsed 1326 books)  
**Core Modules:** ✅ Rebuilt  
**Templates:** ✅ Created  

---

## 🧪 Test Flow

### Step 1: Paste Wave List
1. Go to http://localhost:5000/wave-import
2. Copy a section from `Ranked_Library_Waves.md` (e.g., lines 5-50)
3. Paste into textarea
4. Click "PARSE WAVES"

**Expected:** See wave selection page with W1, W2, W3, W4 breakdown

### Step 2: Select Waves
1. Enter numbers for each wave (e.g., W1: 5, W2: 3)
2. Watch total count update
3. Click "START TAB ORCHESTRATION"

**Expected:** Redirects to tab orchestration page

### Step 3: Discovery & Tabs
1. Wait for discovery to complete (if books need searching)
2. Click "OPEN TABS" for each book
3. Review tabs - close non-fair-use sources
4. Click "I HAVE ONLY FAIR-USE TABS OPEN"

**Expected:** Fair-use confirmation page

### Step 4: Download Setup
1. Confirm fair-use
2. Enter download directory path
3. Click "START DOWNLOAD" (5 second countdown)
4. Manually download PDFs from your tabs
5. System watches folder and processes automatically

**Expected:** PDFs detected, renamed, added to library (PENDING_APPROVAL)

### Step 5: Approval
1. Go to /approvals
2. Preview PDFs
3. Approve or reject

**Expected:** Approved books become READY

---

## 📝 Quick Test

**Test with small sample:**
```
0001. (W1) The 48 Laws of Power — Robert Greene
0002. (W1) The Art of Seduction — Robert Greene
0003. (W1) The 33 Strategies of War — Robert Greene
```

Select W1: 3 books → Should discover → Open tabs → Download → Approve

---

**Ready to test!** Open http://localhost:5000/wave-import








