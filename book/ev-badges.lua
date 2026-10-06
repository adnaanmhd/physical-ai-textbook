-- Evidence badges: [company claim]{.ev}, [demo]{.ev}, [inference]{.ev}.
-- HTML and EPUB style them with styles.css. Other formats (PDF) get an italic "(company claim)".
function Span(el)
  if el.classes:includes("ev") and not FORMAT:match("html") and not FORMAT:match("epub") then
    local out = pandoc.List({pandoc.Str("(")})
    out:extend(el.content)
    out:insert(pandoc.Str(")"))
    return pandoc.Emph(out)
  end
end
