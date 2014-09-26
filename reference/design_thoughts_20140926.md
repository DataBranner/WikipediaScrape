## WKPD Project design thoughts

 1. Store data in flat files; move to database as part of a later process.
 1. Since we don't want to bombard server, time the roundtrip: compose request, send request, receive data, process and store data. The Wikipedia article on [Bot best practices](https://en.wikipedia.org/wiki/Wikipedia:Creating_a_bot#Bot_best_practices) (accessed 20140926) suggests "limit the total requests (read and write requests together) to no more than 10/minute." Timings:
   2. 5.63 s for 20 items, no synonyms. `titles = ['使徒行者', '南方贫困法律中心', '李姓', '查尔斯·范恩', '柯喬治', '柳丁擱來亂角色列表', '满城之战', '無間音樂', '瑞银集团', '瘋神無雙', '第25屆金曲獎', '終極系列', '血清学', '邓稼先', '鄭俊弘', '雁门之战', '非首脑会谈', '高島鞆之助', '魂斗罗', '黃尊秋']`
   2. 23 s for 65 items, some synonyms. `titles = ['普渡大學', '曼城2014年至2015年球季', '曾沛慈', '李姓', '李婉鈺', '李敏 (毛娇娇)', '李研山', '松本孝弘', '板野友美', '林鄭月娥', '查尔斯·范恩', '柳丁擱來亂角色列表', '梅嫦芬', '模块:VariantTest', '歲月留聲', '永續環境教育中心', '泉州市', '泉港区', '火烧圆明园', '無間音樂', '王征', '珠海有轨电车1号线', '理性與感性 (電影)', '真的漢子', '石溪大学', '禧福道', '第15屆金鐘獎', '第九城市', '終極三國登場角色列表', '罗斯柴尔德家族', '羅瑤', '美团网', '聖公會莫壽增會督中學', '聯福道', '臺北市立成功高級中學', '臺灣總督府民政部', '芭芭拉·戈德史密斯自由寫作獎', '英雄傳說 軌跡系列角色列表', '萬壽臺議事堂', '蘇四十三', '蘭開夏道', '西安咸阳国际机场', '诛仙', '超人力霸王系列', '超文本傳輸安全協議', '鄭俊弘', '金正閣', '陆令萱', '陰摩羅鬼之瑕', '陳建平 (電台主持)', '陳曉東 (藝人)', '電動方程式賽車車手列表', '非首脑会谈', '韓瑜', '颶風洛厄爾 (2014年)', '香港外籍家庭傭工', '香港威海衛警察', '香港電視網絡', '馬千齡', '驍龍', '高清翡翠台電視劇集列表 (2014年)', '黃昭順', '黃積權', '黑Girl', '龍飛鳳舞 (電視劇)']`
 1. Use raw kanji for file names, not %-delimited hex names — greater readability, but slight processing delay.
 1. Files:
   2. scraped dictionary of synonyms: one dict to file, named by source file;
   2. links to request: single file, one unique link per line;
   2. links already requested: single file, one unique link per line and date requested;
   2. links to pages listing new pages: one unique link per line; to be used if "to request" list gets sparse.
 1. Errors to fix:
   2. In `get_words()`, one error found here was `pair = "zh-cn:地址栏zh-tw:網址列"`. Can we divide on the known keys if error?
   2. But also cases of single words, which we can't handle: `"月台", "恒生", "琼", "平台", "入伙"`, etc.
   2. And some cases where the keys are in Chinese: `"中国大陆：昂山素季；台灣：翁山蘇姬；香港：昂山素姬"`, etc.
 1. Many malformed HTML errors from `lxml`, too!

[end]

