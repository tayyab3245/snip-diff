"""
Single, high-contrast black & white Qt style-sheet.
Tweak as you like.
"""
STYLE = """
* {
    background: #000;
    color:       #FFF;
    selection-background-color:#FFF;
    selection-color:#000;
    outline:0;
}
QTreeView::item::indicator {
    width:18px; height:18px;
}
QHeaderView::section {
    background:#000;
    color:#FFF;
    padding:4px;
    border:0;
}
"""
