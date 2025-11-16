"use strict";
/**
 * Shared types for SNIP-DIFF Electron app
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.LINE_TYPE_SYMBOLS = exports.DIFF_MODE_LABELS = exports.DEFAULT_RENDER_OPTIONS = exports.DiffMode = exports.ChangeType = exports.LineType = void 0;
// ===== Diff View Types =====
var LineType;
(function (LineType) {
    LineType["CONTEXT"] = "context";
    LineType["ADDED"] = "added";
    LineType["DELETED"] = "deleted";
    LineType["MODIFIED"] = "modified";
})(LineType || (exports.LineType = LineType = {}));
var ChangeType;
(function (ChangeType) {
    ChangeType["ADDED"] = "added";
    ChangeType["DELETED"] = "deleted";
    ChangeType["MODIFIED"] = "modified";
    ChangeType["RENAMED"] = "renamed";
    ChangeType["UNCHANGED"] = "unchanged";
})(ChangeType || (exports.ChangeType = ChangeType = {}));
var DiffMode;
(function (DiffMode) {
    DiffMode["UNIFIED_FULL"] = "unified_full";
    DiffMode["UNIFIED_CONTEXT"] = "unified_context";
    DiffMode["SIDE_BY_SIDE"] = "side_by_side";
    DiffMode["INLINE_FULL"] = "inline_full";
})(DiffMode || (exports.DiffMode = DiffMode = {}));
exports.DEFAULT_RENDER_OPTIONS = {
    context_radius: 3,
    show_line_numbers: true,
    collapse_unchanged: false,
    char_level: false
};
exports.DIFF_MODE_LABELS = {
    [DiffMode.UNIFIED_FULL]: "Unified (Full)",
    [DiffMode.UNIFIED_CONTEXT]: "Unified (Context)",
    [DiffMode.SIDE_BY_SIDE]: "Side by Side",
    [DiffMode.INLINE_FULL]: "Inline (Full)"
};
exports.LINE_TYPE_SYMBOLS = {
    [LineType.CONTEXT]: " ",
    [LineType.ADDED]: "+",
    [LineType.DELETED]: "-",
    [LineType.MODIFIED]: "~"
};
//# sourceMappingURL=types.js.map