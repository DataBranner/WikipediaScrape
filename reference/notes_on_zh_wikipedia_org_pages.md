## Notes on Zh.Wikipedia.Org pages

 1. Variant names are marked with class `noteTA-title` and content `data-noteta-code`:

        <div class="noteTA-title" 
             data-noteta-code="zh-hans:文档对象模型; zh-hant:文件物件模型;"></div>

   There is also code to control the appearance (etc.) of the menu for choosing regional variants:

        <div class="metadata topicon noprint nopopups noteTA-topicon" 
             title="本页使用了标题或全文手工转换" 
             id="noteTA-topicon-203078" 
             style="display: none;padding:0px 2px;">
          <img alt="本页使用了标题或全文手工转换"
              src="//upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Zh_conversion_icon_m.svg/35px-Zh_conversion_icon_m.svg.png" 
             width="35" 
             height="22"
             srcset="//upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Zh_conversion_icon_m.svg/53px-Zh_conversion_icon_m.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Zh_conversion_icon_m.svg/70px-Zh_conversion_icon_m.svg.png 2x" 
             data-file-width="32" 
             data-file-height="20" />
        </div>


 1. There is a module `NoteTA` to choose the correct form. (See https://zh.wikipedia.org/zh/%E6%A8%A1%E5%9D%97:NoteTA and https://zh.wikipedia.org/wiki/MediaWiki:Gadget-noteTA.js; accessed 20140916.)

 1. Justification (https://zh.wikibooks.org/zh-tw/Template:NoteTA):

> 本模板用來在一個頁面裡，轉換不同地區的翻譯用語或指定特定的標題。
>
> 本模板套用字詞轉換基礎模板實現（請參看Template:CH/doc），使用上相對簡單，但也存在一些限制性，全文轉換項目不能超過30個，如果要突破這些局限，請直接使用字詞轉換基礎模板組合。

   See also https://zh.wikipedia.org/wiki/Template:NoteTA/lua.

 1. The API does not currently list `noteta` as an option.
 
 1. In API, `action=query` is most likely to be what I need to use.
 
 1. "Token" required for editing, but perhaps not otherwise. (See https://www.mediawiki.org/wiki/Manual:Edit_token, accessed 20140916.)
 
 

[end]