;(function()
{
	// CommonJS
	typeof(require) != 'undefined' ? SyntaxHighlighter = require('shCore').SyntaxHighlighter : null;

	function Brush()
	{
        var separators = "+ :";
        this.regexList = [
            {regex: /^(?:'')?[A-Z]{3}(?:\+)/gm, css: 'keyword'},
            {regex: /^'.*/gm, css:'comments'},
            {regex: /[:+']/gm, css:'color2'},
            {regex: /&amp;/gm, css:'color2'}
        ];
	};

	Brush.prototype	= new SyntaxHighlighter.Highlighter();
	Brush.aliases	= ['edi', 'edifcat'];

	SyntaxHighlighter.brushes.Diff = Brush;

	// CommonJS
	typeof(exports) != 'undefined' ? exports.Brush = Brush : null;
})();