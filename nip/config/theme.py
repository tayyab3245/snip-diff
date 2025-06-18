"""
Mac-inspired, glassy Qt stylesheet
---------------------------------
• blurred window background (macOS & Win 10/11 Acrylic)
• subtle bevels & rounded corners
• neon-blue focus rings
"""
STYLE = r"""
/* ---------- window background ---------- */
QMainWindow, QToolTip, QMessageBox {          /* enable translucency */
    background: rgba(30, 30, 30, 160);        /* glassy charcoal */
    backdrop-filter: blur(40px);
    color: #EAEAEA;
    font-family: -apple-system, "Segoe UI", sans-serif;
    font-size: 12pt;
}

/* ---------- toolbar ---------- */
QToolBar {
    background: rgba(45, 45, 45, 200);
    border-bottom: 1px solid #1A1A1A;
}
QToolButton {
    padding: 6px 14px;
    margin: 0 2px;
    border-radius: 6px;
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #555, stop:1 #333
    );
    color:#FFF;
}
QToolButton:hover   { background:#636363; }
QToolButton:pressed { background:#7C7C7C; }

/* ---------- tree & preview backgrounds ---------- */
QTreeView, QPlainTextEdit {
    background: rgba(20, 20, 20, 220);
    border: 1px solid #2B2B2B;
    border-radius: 8px;
}

/* ---------- checkboxes ---------- */
QTreeView::indicator           { width:16px; height:16px; border-radius:4px; }
QTreeView::indicator:unchecked { border:1px solid #6F6F6F;  background:transparent; }
QTreeView::indicator:checked   { border:none; background:#00C853; }
QTreeView::indicator:indeterminate { border:none; background:#FFCA28; }

/* ---------- selection & focus ring ---------- */
*::item:selected  { background:#2962FF; color:#FFF; }
*::item:focus,
QToolButton:focus {
    outline:3px solid #448AFF;
    outline-offset:0;
}

/* ---------- scrollbar ---------- */
QScrollBar:vertical, QScrollBar:horizontal {
    background: transparent;
    margin: 0;
    width: 10px; height:10px;
}
QScrollBar::handle {
    background: rgba(255,255,255,0.3);
    border-radius:5px;
}
QScrollBar::handle:hover { background: rgba(255,255,255,0.5); }
"""
