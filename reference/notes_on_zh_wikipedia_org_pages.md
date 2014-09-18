## Notes on Zh.Wikipedia.Org pages

 1. Reference:
   2. API here: https://www.mediawiki.org/wiki/API:Main_page.
   2. Some mash-ups listed here: http://www.programmableweb.com/api/wikipedia.
 

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

 1. Output of the summary of changes listed under `<div class="noteTA-local">`:

        本文使用标题手工转换
        
            转换标题为：简体：黑客帝国；香港：廿二世紀殺人網絡；台灣：駭客任務；
            实际标题为：黑客帝国；当前显示为：黑客帝国
        
        [编辑]
        
        本文使用公共转换组“电影译名”。
        
        [编辑]
        
        本文使用公共转换组“藝人譯名”。
        
        [编辑]
        
        本文使用全文手工转换
        
            简体：尼奥；繁體：尼歐；当前显示为：尼奥
            简体：矩阵；繁體：母體；当前显示为：矩阵
            大陆：史密斯特工；台灣：史密斯探員；香港：史特工；当前显示为：史密斯特工
            大陆：托马斯·安德森；台灣：湯瑪斯·安德森；香港：安湯武；当前显示为：托马斯·安德森
            大陆：艾波克；台灣：艾巴；香港：天啟；当前显示为：艾波克
            大陆：开关；台灣：蘇薇琪；香港：變體；当前显示为：开关
            大陆：塞弗；台灣：塞佛；香港：暗碼；当前显示为：塞弗
            大陆：坦克；台灣：坦克；香港：戰車；当前显示为：坦克
            大陆：多泽；台灣：道瑟；香港：推土機；当前显示为：多泽
            大陆：耗子；台灣：茂史；香港：滑鼠；当前显示为：耗子
            大陆：先知；台灣：先知；香港：祭司；当前显示为：先知
            大陆：重装上阵；台灣：重裝上陣；香港：決戰未來；当前显示为：重装上阵
            大陆：矩阵革命；台灣：最後戰役；香港：驚變世紀；当前显示为：矩阵革命
            简体：程序；繁體：程式；当前显示为：程序

 1. There is a module `NoteTA` to choose the correct form. (See [https://zh.wikipedia.org/zh/模块:NoteTA](https://zh.wikipedia.org/zh/%E6%A8%A1%E5%9D%97:NoteTA) and https://zh.wikipedia.org/wiki/MediaWiki:Gadget-noteTA.js; accessed 20140916.)

 1. Justification (https://zh.wikibooks.org/zh-tw/Template:NoteTA):

   > 本模板用來在一個頁面裡，轉換不同地區的翻譯用語或指定特定的標題。
   >
   > 本模板套用字詞轉換基礎模板實現（請參看Template:CH/doc），使用上相對簡單，但也存在一些限制性，全文轉換項目不能超過30個，如果要突破這些局限，請直接使用字詞轉換基礎模板組合。

   See also https://zh.wikipedia.org/wiki/Template:NoteTA/lua.

 1. The API does not currently list `noteta` as an option.
 
 1. In API, `action=query` is most likely to be what I need to use.
 
 1. "Token" required for editing, but perhaps not otherwise. (See https://www.mediawiki.org/wiki/Manual:Edit_token, accessed 20140916.)
 
 1. Interesting cases for study:
 
   1. [黑客帝国](https://zh.wikipedia.org/wiki/%E9%BB%91%E5%AE%A2%E5%B8%9D%E5%9B%BD)

[end]
