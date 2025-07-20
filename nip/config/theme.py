"""
Nintendo 3-DS x mac-glass theme (no Qt warnings - removed unsupported transition/transform)
"""
STYLE = r"""
/* =====  GLOBAL  ===================================================== */
* {
    font-family:-apple-system,"Segoe UI","Fira Sans",sans-serif;
    font-size:11.2pt;
}
QMainWindow,QToolTip,QMessageBox { background:transparent; color:#E9ECEF; }

/* =====  GLASS EFFECT  ============================================== */
QWidget#glass {             /* applied by GlassWindow mix-in            */
    background:rgba(24,24,28,170);          /* translucent charcoal */
}

/* =====  TOOLBAR  ==================================================== */
#toolbar {
    background:rgba(28,40,56,.92);          /* 3-DS shell teal */
    border:none;
}
#toolbar QToolButton {
    padding:6px 16px;  margin:0 5px;  border-radius:7px;
    background:#324B68;  color:#E9ECEF;
}
#toolbar QToolButton:hover   { background:#3E5E7E; }
#toolbar QToolButton:pressed { background:#1D70F8; }

/* =====  PANES  ====================================================== */
QTreeView,QPlainTextEdit {
    background:#1B212A;
    border:1px solid #2A394B;
    border-radius:9px;
}

/* =====  CHECK-MARKS  =============================================== */
QTreeView::indicator           { width:15px;height:15px;border-radius:3px; }
QTreeView::indicator:unchecked { border:1px solid #5F738D; background:transparent; }
QTreeView::indicator:checked   { border:none; background:#30D5FF; }          /* neon-cyan */
QTreeView::indicator:indeterminate {
    border:1px solid #FFC400;
    background:repeating-linear-gradient(45deg,#FFC400 0 4px,transparent 4px 8px);
}

/* =====  SELECTION & FOCUS  ========================================= */
*::item:selected { background:#1D70F8; color:#F2F5F7; }
*::item:focus,
QToolButton:focus { outline:2px solid #30D5FF; outline-offset:0; }

/* =====  SCROLLBARS  ================================================= */
QScrollBar {
    background:transparent; width:9px; height:9px;
}
QScrollBar::handle {
    background:rgba(255,255,255,.26); border-radius:4px;
}
QScrollBar::handle:hover { background:rgba(255,255,255,.42); }
"""
