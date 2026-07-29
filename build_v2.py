# -*- coding: utf-8 -*-
"""Build Steel Spirit v2 - with portraits, decisions, richer backgrounds."""
import json, os, base64, io
from PIL import Image

WORKDIR = r'C:\Users\Administrator\WorkBuddy\2026-07-28-18-14-29'
ASSETS = os.path.join(WORKDIR, 'assets')
REAL_PHOTOS = os.path.join(ASSETS, 'real_photos')
OUT = os.path.join(WORKDIR, 'index.html')

# === Image Processing ===
def img_to_b64(path, max_w=400, quality=65):
    """Resize image, convert to JPEG, return base64 data URL."""
    img = Image.open(path).convert('RGB')
    w, h = img.size
    if w > max_w:
        ratio = max_w / w
        img = img.resize((max_w, int(h * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=quality, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

# Map images to masters
# Real photos from the internet (胡赓祥 网上无公开照片，保留AI生成)
real_portrait_map = {
    1: 'weishoukun_1988.jpg',       # 魏寿昆 1988年在实验室
    2: 'kejun_portrait.jpg',         # 柯俊 百度百科肖像
    3: 'xiaojimei_portrait.png',     # 肖纪美 肖像
    4: 'zhangxingqian_portrait.jpg', # 张兴钤 百度百科肖像
    5: None,  # 胡赓祥 无公开照片
}
ai_portrait_keywords = {
    5: 'Chinese_professor_Hu_Gengxiang'
}
scene_files = {
    1: '1930s_China_university_campus',
    2: '1940s_Birmingham_University',
    3: '1950s_Chinese_steel_factory',
    4: '1960s_Qinghai_desert_research',
    5: 'Shanghai_Jiao_Tong_University'
}

print("Compressing images...")
portraits = {}
scenes = {}
for mid in range(1, 6):
    # Load portrait: real photo if available, otherwise AI-generated
    if real_portrait_map.get(mid):
        pf_path = os.path.join(REAL_PHOTOS, real_portrait_map[mid])
        portraits[mid] = img_to_b64(pf_path, max_w=350, quality=60)
        print(f"  Master {mid}: real photo {real_portrait_map[mid]}, {len(portraits[mid])//1024}KB")
    else:
        pf = [f for f in os.listdir(ASSETS) if ai_portrait_keywords[mid] in f and f.endswith('.png')][0]
        portraits[mid] = img_to_b64(os.path.join(ASSETS, pf), max_w=350, quality=60)
        print(f"  Master {mid}: AI portrait (no real photo online), {len(portraits[mid])//1024}KB")
    sf = [f for f in os.listdir(ASSETS) if scene_files[mid] in f and f.endswith('.png')][0]
    scenes[mid] = img_to_b64(os.path.join(ASSETS, sf), max_w=800, quality=55)
    print(f"  Master {mid}: scene {len(scenes[mid])//1024}KB")

# Forge bg
forge_files = [f for f in os.listdir(ASSETS) if 'Steel_forge' in f and f.endswith('.png')]
forge_bg = img_to_b64(os.path.join(ASSETS, forge_files[0]), max_w=800, quality=50) if forge_files else ''
print(f"  Forge bg: {len(forge_bg)//1024}KB")
print("Done compressing.\n")

# === MASTERS DATA (same as before, already clean) ===
MASTERS = [
    {"id":1,"name":"魏寿昆","title":"冶金物理化学奠基人","emoji":"🏛️","badge":"🧪","badgeName":"冶金热力学之章","color":"#f4813a","subtitle":"1907 - 2014 · 中国科学院院士","lifeStory":"魏寿昆，字镇雄，1907年生于天津一个没落商人家庭。年少时家道中落，生活拮据，但他天资聪颖、勤奋好学，以第一名成绩考入北洋大学（今天津大学前身）矿冶工程系。1929年以四年平均94.25分的惊人成绩毕业，创北洋大学有史以来最高分数纪录，被誉为「北洋才子」。<br><br>1930年考取公费留学德国，先后在柏林工业大学和德累斯顿工业大学深造。1935年以极优成绩获工学博士学位，自费赴亚琛工业大学钢铁冶金研究所进修一年。1936年归国，抗战期间辗转西北联合大学、西北工学院等多所高校，将先进冶金知识带入中国。<br><br>1952年院系调整中，率队参与筹建新中国第一所钢铁高等学府——北京钢铁学院（现北京科技大学）。从教80余年，在10所大学任教，讲授过28门课程，培养了四五代冶金科技人才。学生在他百年华诞时献词：「试问天下名冶师，几人不出先生门。」","achievements":"中国冶金物理化学的奠基人之一，中国金属学会创建人之一。著有经典著作《冶金过程热力学》和《活度在冶金物理化学中的应用》，其中《冶金过程热力学》被日本冶金学家后藤和弘誉为「迄今为止世界上最好的一部冶金热力学著作」。建立了高温熔体活度理论体系和炉渣脱硫离子理论，提出选择性氧化理论，率先开展固体电解质电池定氧技术研究（被誉为当时国际钢铁冶金三大发明之一）。","quote":"「中国地大物博，钢铁少，国外钢铁多，祖国需要钢铁。」——魏寿昆","timeline":[{"year":"1907","text":"出生于天津"},{"year":"1929","text":"北洋大学矿冶工程系毕业，成绩创纪录（94.25分）"},{"year":"1935","text":"获德国德累斯顿工业大学博士学位"},{"year":"1952","text":"参与筹建北京钢铁学院（现北京科技大学）"},{"year":"1964","text":"出版《活度在冶金物理化学中的应用》"},{"year":"1980","text":"当选中国科学院院士，出版《冶金过程热力学》"},{"year":"2014","text":"逝世，享年107岁"}],"questions":[{"q":"魏寿昆被誉为中国哪个学科的奠基人","options":["冶金物理化学","机械工程","高分子化学","地球物理学"],"answer":0,"hint":"魏寿昆是中国冶金物理化学学科的奠基人，他的《冶金过程热力学》被国际学者誉为该领域最好的著作。"},{"q":"魏寿昆在哪所德国大学获得博士学位？","options":["柏林工业大学","慕尼黑工业大学","德累斯顿工业大学","亚琛工业大学"],"answer":2,"hint":"魏寿昆1935年在德累斯顿工业大学获工学博士学位，后又自费赴亚琛工业大学进修钢铁冶金。"},{"q":"魏寿昆的经典著作——被国际学者誉为「最好冶金热力学著作」的是哪本？","options":["《金属物理学》","《冶金过程热力学》","《钢铁是怎样炼成的》","《材料科学导论》"],"answer":1,"hint":"《冶金过程热力学》是魏寿昆的代表作，日本冶金学家后藤和弘盛赞其为「迄今为止世界上最好的一部冶金热力学著作」。"},{"q":"魏寿昆参与筹建的新中国第一所钢铁高等学府是？","options":["东北大学","武汉钢铁学院","北京钢铁学院（现北京科技大学）","鞍山钢铁学院"],"answer":2,"hint":"1952年院系调整时，魏寿昆参与筹建北京钢铁学院并担任第一任教务长，这所学校后来发展为北京科技大学。"},{"q":"魏寿昆提出的什么概念成功指导了多金属矿的冶炼分离？","options":["选择性氧化理论","量子跃迁理论","超导转变理论","高分子聚合理论"],"answer":0,"hint":"魏寿昆提出的选择性氧化理论，成功指导了红土矿脱铬、金川矿提镍、包头矿提铌、攀枝花钒钛磁铁矿提钒等多金属矿的冶炼分离。"},{"q":"魏寿昆在北洋大学矿冶系的毕业平均分是多少？","options":["88.50分","94.25分","90.00分","98.50分"],"answer":1,"hint":"1929年魏寿昆以四年平均94.25分的惊人成绩从北洋大学毕业，创北洋大学有史以来最高分数纪录！"},{"q":"魏寿昆率先在国内开展的什么技术，被誉为国际钢铁冶金三大发明之一？","options":["真空冶金技术","固体电解质电池快速定氧技术","连续铸轧技术","电磁搅拌技术"],"answer":1,"hint":"魏寿昆率先在国内开拓固体电解质电池直接快速定氧技术，这项技术当时被誉为国际钢铁冶金三大发明之一。"},{"q":"魏寿昆一生共主讲过约多少门课程？","options":["10门","18门","28门","35门"],"answer":2,"hint":"魏寿昆从教80余年，共主讲过28门课程，培养了四五代冶金科技人才。学生献词：「试问天下名冶师，几人不出先生门。」"}]},
    {"id":2,"name":"柯俊","title":"贝茵体先生","emoji":"🔬","badge":"⚙️","badgeName":"贝茵体相变之章","color":"#5b9ed4","subtitle":"1917 - 2017 · 中国科学院院士","lifeStory":"柯俊，1917年生于吉林长春，祖籍浙江黄岩。1938年毕业于武汉大学化学系。1944年赴英国伯明翰大学深造，1948年获自然哲学博士学位。<br><br>1951年，柯俊首次提出钢中贝茵体转变的切变位移机制，证明其与珠光体、马氏体不同的独特相变。这一发现使国际上形成了关于贝茵体相变的「切变学派」，《钢铁金相学》以他的姓氏将无碳贝茵体命名为「柯氏贝茵体」，他本人被国际同行尊称为「Mr. Bain（贝茵体先生）」。<br><br>1954年回国后，在北京钢铁学院创立中国第一个金属物理专业，参与创办第一个冶金物理化学专业。70年代后又创办中国第一个科学技术史专业。三个学科先后被评为国家重点学科。90年代推动全国工程教育改革，建立「大材料」试点班，在全国产生广泛影响。","achievements":"贝茵体切变理论创始人。首次观察到钢中马氏体形成时基体形变和原子簇对马氏体长大的阻碍作用；系统研究铁镍钒碳钢中原子簇导致蝶状马氏体形成，发展了马氏体相变动力学。开拓中国冶金史研究，阐明中国生铁技术发明与发展对人类文明的重大作用。先后获国家自然科学奖、何梁何利奖。设立「柯俊科技教育基金」。","quote":"「钢铁科学与技术的集大成者」——后人评价。他用一生证明，钢铁不仅是工业脊梁，更是文明火炬。","timeline":[{"year":"1917","text":"出生于吉林长春"},{"year":"1938","text":"武汉大学化学系毕业"},{"year":"1948","text":"获英国伯明翰大学自然哲学博士学位"},{"year":"1951","text":"首次提出贝茵体切变机制，命名为「柯氏贝茵体」"},{"year":"1954","text":"回国任教，创立中国第一个金属物理专业"},{"year":"1980","text":"当选中国科学院院士"},{"year":"2017","text":"逝世，享年101岁"}],"questions":[{"q":"柯俊被国际同行尊称为什么？","options":["Mr. Steel","Mr. Bain（贝茵体先生）","Dr. Metal","Sir Physics"],"answer":1,"hint":"柯俊因首次发现钢中贝茵体切变机制，被国际同行尊称为「Mr. Bain（贝茵体先生）」。无碳贝茵体甚至以他的姓氏命名为「柯氏贝茵体」。"},{"q":"柯俊创立了中国第一个什么专业？","options":["冶金工程专业","材料科学专业","金属物理专业","核物理专业"],"answer":2,"hint":"1954年回国后，柯俊在北京钢铁学院创立了中国第一个金属物理专业，后来又创办了第一个科学技术史专业。"},{"q":"柯俊在哪所英国大学获得博士学位？","options":["牛津大学","剑桥大学","伯明翰大学","帝国理工学院"],"answer":2,"hint":"柯俊1944年赴英国伯明翰大学深造，师从著名金属学家D.Hanson教授，1948年获自然哲学博士学位。"},{"q":"柯俊的贝茵体切变机制证明了贝茵体与哪两种组织的区别？","options":["铁素体和渗碳体","珠光体和马氏体","奥氏体和铁素体","莱氏体和索氏体"],"answer":1,"hint":"柯俊首次证明贝茵体转变的切变位移机制，证明了贝茵体是不同于珠光体和马氏体的独特相变。"},{"q":"柯俊晚年开拓了哪个跨学科研究领域？","options":["生物冶金学","中国冶金史（科学技术史","太空材料学","纳米机器人学"],"answer":1,"hint":"70年代后柯俊创办中国第一个科学技术史专业，开拓了中国冶金史研究，被尊为「中国冶金史研究的开拓者」。"},{"q":"《钢铁金相学》以柯俊的姓氏命名了什么组织？","options":["柯氏珠光体","柯氏贝茵体（无碳贝茵体）","柯氏马氏体","柯氏奥氏体"],"answer":1,"hint":"《钢铁金相学》以柯俊的姓氏将无碳贝茵体命名为「柯氏贝茵体」（Ko's Bainite），这是中国人的姓氏第一次用于国际材料学命名。"},{"q":"柯俊在50年代首次观察到什么重要现象？","options":["贝茵体熔化过程","马氏体形成时基体的形变","铁素体磁性转变","奥氏体晶粒生长"],"answer":1,"hint":"20世纪50年代，柯俊首次观察到钢中马氏体形成时基体的形变和原子簇对马氏体长大的阻碍作用。"},{"q":"柯俊90年代推动的工程教育改革建立了什么试点？","options":["纳米材料试点班","大材料试点班","智能材料试点班","生物材料试点班"],"answer":1,"hint":"90年代柯俊推动全国工程教育改革，在北京科技大学建立「大材料」试点班，在全国产生广泛影响。"}]},
    {"id":3,"name":"肖纪美","title":"终身为士不为仕","emoji":"📖","badge":"🛡️","badgeName":"材料防护之章","color":"#4caf91","subtitle":"1920 - 2014 · 中国科学院院士","lifeStory":"肖纪美，1920年生于湖南凤凰县，与文坛巨匠沈从文、画家黄永玉并称「凤凰三杰」。1943年毕业于唐山交通大学。1948年赴美留学，两年半内先后取得密苏里大学硕士和博士学位。其后在美从事工业研究，积累了丰富实践经验。<br><br>1957年，他冲破美国政府重重阻挠，毅然回国。入境时美国移民局以中美未建交为由无理扣下他一万美金旅行支票。他微笑着说：「我先把钱存在你这里，但我要算利息的。」后来尼克松总统访华时，竟真的完成了「还钱」任务。<br><br>回国后在北京钢铁学院任教五十多年。秉持「终身为士不为仕」理念，谢绝多次担任行政领导机会，安心教书育人，培养六十余名研究生。九十高龄仍笔耕不辍，临终前还在撰写第30本著作。","achievements":"在发展铬锰氮不锈耐热钢中提出合金设计新方法，开创节镍不锈钢研究。在材料应力腐蚀和氢致开裂机理研究方面取得突破性成果，获1987年国家自然科学奖二等奖。将金属物理、断裂力学和腐蚀科学综合应用，解决了国民经济与国防建设中的若干重要断裂问题。一生撰写著作29部。2011年获中国金属学会冶金科技终身成就奖。","quote":"「智慧的牧羊人，具有善良的心肠。将可爱的羔羊，放到水草茂盛的地方，喜看羔羊们茁壮地成长。」——肖纪美以牧羊人比喻教师","timeline":[{"year":"1920","text":"生于湖南凤凰县"},{"year":"1943","text":"唐山交通大学毕业"},{"year":"1950","text":"获美国密苏里大学博士学位"},{"year":"1957","text":"冲破阻挠回国任教"},{"year":"1980","text":"当选中国科学院院士"},{"year":"1987","text":"获国家自然科学奖二等奖"},{"year":"2014","text":"逝世，享年94岁"}],"questions":[{"q":"肖纪美在哪个科研领域做出杰出贡献？","options":["量子计算","材料应力腐蚀和氢致开裂","基因编辑","人工智能"],"answer":1,"hint":"肖纪美在材料应力腐蚀和氢致开裂机理研究方面取得突破性成果，1987年获国家自然科学奖二等奖。"},{"q":"肖纪美秉持怎样的人生理念？","options":["天下为公","终身为士不为仕","知行合一","天行健君子以自强不息"],"answer":1,"hint":"肖纪美秉持「终身为士不为仕」的理念，谢绝多次担任行政领导的机会，安心教书育人五十余载。"},{"q":"肖纪美在哪所美国大学获得博士学位？","options":["哈佛大学","斯坦福大学","麻省理工学院","密苏里大学"],"answer":3,"hint":"肖纪美1948年赴美，两年半内在密苏里大学先后取得硕士和博士学位。"},{"q":"肖纪美回国被扣的一万美金后来由谁「还」了？","options":["基辛格","尼克松总统","卡特总统","联合国秘书长"],"answer":1,"hint":"1957年肖纪美回国时被扣下1万美金的旅行支票，他幽默地说「我先存你这里，但要算利息」。1972年尼克松访华时竟真的完成了「还钱」任务！"},{"q":"肖纪美开创了哪种新型不锈钢的研究方向？","options":["铬锰氮系节镍不锈钢","钛合金不锈钢","钴基合金钢","纯镍不锈钢"],"answer":0,"hint":"肖纪美开创了铬锰氮系节镍不锈钢的研究方向，提出用锰、氮部分或全部代替奥氏体不锈钢中的镍。"},{"q":"肖纪美一生共撰写了多少部著作？","options":["15部","22部","29部","35部"],"answer":2,"hint":"肖纪美一生撰写著作29部，九十高龄仍笔耕不辍，临终前还在撰写第30本著作《学科的融合》。"},{"q":"肖纪美与哪两位文化名人并称「凤凰三杰」？","options":["鲁迅和胡适","沈从文和黄永玉","郭沫若和巴金","老舍和曹禺"],"answer":1,"hint":"肖纪美出生于湖南凤凰县，与文坛巨匠沈从文、著名画家黄永玉并称「凤凰三杰」。"},{"q":"肖纪美临终前正在撰写的第30部著作名称是什么？","options":["《材料科学导论》","《学科的融合》","《金属的奥秘》","《腐蚀与防护》"],"answer":1,"hint":"肖纪美晚年笔耕不辍，临终前正在撰写第30部著作——《学科的融合》，体现了他一生推崇的「类比交叉」思想。"}]},
    {"id":4,"name":"张兴钤","title":"金石人生 · 核武报国","emoji":"☢️","badge":"⭐","badgeName":"国之重器之章","color":"#e8b640","subtitle":"1921 - 2022 · 中国科学院院士","lifeStory":"张兴钤，1921年生于河北武邑。1942年毕业于武汉大学矿冶系。1947年赴美实习，凭出色表现先后进入凯斯理工学院和麻省理工学院（MIT）深造，取得物理冶金硕士和博士学位。在MIT期间，他连续几天泡在实验室，用烟斗提神、闹钟计时，系统研究高温蠕变过程，所拍晶界运动照片的精美程度令日本学者叹为观止。<br><br>他在美国的金属蠕变结构研究被国际学术界视为奠基性工作，发表八篇论文被广泛引用。1952年博士毕业后经历重重阻挠，1955年终于踏上祖国土地。<br><br>回国后在北京钢铁工业学院参与筹建新中国第一个金属物理专业，编订教材《金属及合金的力学性质》。1963年奉调奔赴青海戈壁滩，隐姓埋名投身核武器研制，参与组织领导爆轰物理、特殊材料冶金、实验核物理等研究，为原子弹和氢弹的成功爆炸作出重大贡献。","achievements":"金属蠕变结构研究的奠基人之一。编订《金属及合金的力学性质》成为全国通用教材。在核武器研制中组织爆轰物理、核测试等多领域研究。1982年获国家自然科学奖一等奖，1985年获国家科学技术进步奖特等奖，2002年获何梁何利技术科学奖。","quote":"「将来学成后，要回国去，一起建设我们的新中国。」——张兴钤留学时许下的誓言","timeline":[{"year":"1921","text":"生于河北武邑"},{"year":"1942","text":"武汉大学矿冶系毕业"},{"year":"1952","text":"获MIT博士学位，金属蠕变研究震动国际学界"},{"year":"1955","text":"冲破阻挠回到祖国"},{"year":"1963","text":"奉调奔赴青海，投身核武器研制"},{"year":"1991","text":"当选中国科学院院士"},{"year":"2022","text":"逝世，享年101岁"}],"questions":[{"q":"张兴钤在哪所世界名校获得博士学位？","options":["哈佛大学","麻省理工学院（MIT）","普林斯顿大学","剑桥大学"],"answer":1,"hint":"张兴钤1952年在麻省理工学院（MIT）获得物理冶金博士学位，其高温蠕变研究震动国际学界。"},{"q":"张兴钤被国际学术界视为奠基性工作的是哪项研究？","options":["超导材料研究","金属蠕变结构研究","纳米材料研究","磁性材料研究"],"answer":1,"hint":"张兴钤在美期间系统研究了金属蠕变过程，发表八篇论文被广泛引用，成为全球金属蠕变结构研究的奠基性工作。"},{"q":"张兴钤隐姓埋名参与的国家重大工程是什么？","options":["三峡工程","南水北调","核武器研制（原子弹和氢弹）","载人航天工程"],"answer":2,"hint":"1963年张兴钤奉调奔赴青海戈壁滩，隐姓埋名投身核武器研制，为原子弹和氢弹的成功爆炸作出了重大贡献。"},{"q":"张兴钤获得过的最高级别奖项是？","options":["诺贝尔物理学奖","国家自然科学一等奖和国家科技进步特等奖","菲尔兹奖","普利策奖"],"answer":1,"hint":"张兴钤先后获得国家自然科学奖一等奖（1982年）和国家科学技术进步奖特等奖（1985年），这是我国科技领域的最高荣誉。"},{"q":"张兴钤为金属物理专业编写的教材是哪本？","options":["《材料科学基础》","《金属及合金的力学性质》","《冶金热力学》","《核物理导论》"],"answer":1,"hint":"张兴钤编订的《金属及合金的力学性质》后来成为全国通用教材。"},{"q":"张兴钤在MIT做实验时用什么提神？","options":["咖啡","茶","烟斗","能量饮料"],"answer":2,"hint":"在MIT实验室里，张兴钤用烟斗提神、闹钟计时，连续几天不间断地观察高温下材料的变化，其勤奋严谨令导师赞叹。"},{"q":"张兴钤被派到什么地方参与核武器研制？","options":["四川绵阳","青海戈壁滩","新疆罗布泊","甘肃酒泉"],"answer":1,"hint":"1963年张兴钤奉调奔赴青海戈壁滩的221基地，这里是中国第一个核武器研制基地。"},{"q":"张兴钤1940年在武汉大学加入了什么组织？","options":["学生会","中国共产党","国民党","共青团"],"answer":1,"hint":"张兴钤1940年在武汉大学加入中国共产党，一生与党同龄，被后人尊称为「与党同龄的科学家」。"}]},
    {"id":5,"name":"胡赓祥","title":"材料教育开拓者","emoji":"🎓","badge":"📚","badgeName":"材料育人之章","color":"#b878d4","subtitle":"上海交通大学教授","lifeStory":"胡赓祥，上海交通大学材料科学与工程学院教授，中国材料科学教育领域的重要开拓者。他长期坚守在教学和科研第一线，以严谨的治学态度和高尚的人格魅力影响了一代又一代材料学子。<br><br>20世纪80年代起，胡赓祥主讲的《材料科学基础》课程逐渐成为上海交通大学材料学院的王牌课程。他与蔡珣、戎咏华教授合编的同名教材，创造性地将传统的「物理冶金学」「高分子物理学」和「陶瓷学」三门专业基础课有机融合在一起，形成全新的材料科学基础理论体系——真正的融合而非简单的掺合。<br><br>该教材获评全国优秀教材一等奖、「十二五」国家级规划教材、国家精品课程教材。2025年仍被列为上海交通大学硕士研究生招生考试参考书，影响力深远。在科研方面，他主持了亚稳态Al3Ti合金转化生成复相组织及其强韧化机理等国家自然科学基金项目。","achievements":"主编《材料科学基础》（第三版），获全国优秀教材一等奖，被列为国家精品课程教材。该教材将金属、陶瓷、高分子三大材料的微观特性和宏观规律建立在共同理论基础上，在国内外材料教育界产生重大影响。主持国家自然科学基金面上项目，在亚稳态合金领域取得重要成果。","quote":"「胡老师性情温和，而又有着一身正气，遇到原则问题也会毫不退让。」——学生周浪","timeline":[{"year":"1980s","text":"《材料科学基础》课程成为上海交大王牌课程"},{"year":"1998","text":"主持国家自然科学基金亚稳态Al3Ti合金项目"},{"year":"2003","text":"《材料科学基础》获评国家精品课程"},{"year":"2020","text":"教材用于上海交大招收港澳台博士研究生参考书"},{"year":"2021","text":"《材料科学基础》（第三版）获全国优秀教材一等奖"},{"year":"2025","text":"仍被列为硕士招生考试参考书"}],"questions":[{"q":"胡赓祥主编的经典教材是什么？","options":["《材料科学基础》","《大学物理》","《有机化学》","《工程力学》"],"answer":0,"hint":"胡赓祥主编的《材料科学基础》是材料科学与工程专业的基础理论教材，获全国优秀教材一等奖，被数百万材料学子奉为经典。"},{"q":"胡赓祥在哪所大学任教？","options":["清华大学","北京大学","上海交通大学","浙江大学"],"answer":2,"hint":"胡赓祥是上海交通大学材料科学与工程学院教授，长期坚守在教学和科研第一线。"},{"q":"《材料科学基础》将哪三种材料融合在一个理论体系下？","options":["金属、玻璃、木材","金属、陶瓷、高分子","塑料、橡胶、纤维","钢铁、水泥、塑料"],"answer":1,"hint":"胡赓祥团队创造性地将金属、陶瓷、高分子三大材料的微观特性和宏观规律建立在共同理论基础上，是真正的学科融合。"},{"q":"胡赓祥主编的《材料科学基础》获得了什么奖项？","options":["国家自然科学奖","全国优秀教材一等奖","国家技术发明奖","何梁何利奖"],"answer":1,"hint":"2021年《材料科学基础》（第三版）获首届全国优秀教材一等奖，这是教材领域的最高荣誉。"},{"q":"胡赓祥在学生眼中是一位怎样的导师？","options":["严厉苛刻","温文尔雅、正直严谨","玩世不恭","不闻不问"],"answer":1,"hint":"学生周浪评价：「胡老师性情温和，而又有着一身正气，遇到原则问题也会毫不退让。」"},{"q":"《材料科学基础》的编写创新在于融合了哪三门传统课程？","options":["金属学、力学、化学","物理冶金学、高分子物理学、陶瓷学","晶体学、热力学、动力学","冶金学、材料力学、电子学"],"answer":1,"hint":"胡赓祥的创新在于将传统的「物理冶金学」「高分子物理学」「陶瓷学」三门独立课程有机融合在一起，形成统一的理论体系。"},{"q":"胡赓祥主持的国家自然科学基金项目研究什么材料？","options":["超导材料","亚稳态Al3Ti合金","纳米碳管","石墨烯"],"answer":1,"hint":"胡赓祥主持了亚稳态Al3Ti合金转化生成复相组织及其强韧化机理等国家自然科学基金项目。"},{"q":"2025年《材料科学基础》仍被用于什么场景？","options":["本科生毕业设计","硕士研究生招生考试参考书","博士论文答辩","高中物理竞赛"],"answer":1,"hint":"截至2025年，《材料科学基础》仍被列为上海交通大学硕士研究生招生考试参考书，影响力持续数十年。"}]}
]

# === DECISIONS DATA ===
DECISIONS = [
    {"masterId":1,"title":"1949·天津抉择","bg_desc":"1948年末，天津战役前夕。国民政府命令北洋大学南迁，一批知名教授包括魏寿昆在内均在计划南迁名单之中。此时的魏寿昆，已在国民党统治下目睹了太多腐败与黑暗……","optionA":"随国民政府南迁，去往南方继续教学","optionB":"接受共产党地下组织安排，留在天津迎接解放","resultA":{"title":"南下之路","text":"你选择了跟随国民政府南迁。在新的大学里，你继续教授冶金课程，但随着时局变化，教学条件日益艰苦。多年后，你成为一名受人尊敬的教授，但错过了参与创建新中国第一所钢铁高等学府的历史机遇。历史评价：一位优秀的教育者，但未能站在时代变革的最前沿。","badge":""},"resultB":{"title":"钢铁学院的奠基人","text":"你选择了留在天津迎接解放。1952年院系调整，你参与组建了新中国成立后创办的第一所钢铁工业高等学府——北京钢铁学院（现北京科技大学），被任命为第一任教务长。从此，你从这里出发，培养了四五代冶金科技人才。历史评价：中国冶金物理化学奠基人，钢铁摇篮的缔造者。","badge":"🏫"}},
    {"masterId":2,"title":"1953·归国决心","bg_desc":"1953年，柯俊已是世界知名的金属物理学家，美国芝加哥大学、德国马普钢铁研究所、印度国家冶金研究所等纷纷向他发出邀请。但大洋彼岸，新中国刚刚成立，百废待兴……","optionA":"接受海外顶尖机构的邀约，留在西方发展","optionB":"婉拒所有海外邀请，携家眷回国任教","resultA":{"title":"海外的星","text":"你接受海外邀约，继续在国际学术前沿深耕。你发表了许多高质量论文，成为国际知名学者。但夜深人静时，你总会想起那个遥远的东方故土。历史评价：一位杰出的国际学者，但中国失去了创立金属物理专业的最佳时机。","badge":""},"resultB":{"title":"「贝茵体先生」归来","text":"你婉拒了所有海外邀请，携妻儿几经波折回到祖国。1954年起，你在北京钢铁学院创立了中国第一个金属物理专业、第一个冶金物理化学专业，后又创办第一个科学技术史博士点。三个学科先后成为国家重点学科。你将毕生献给了中国的材料科学教育事业。历史评价：贝茵体切变理论创始人，中国金属物理和冶金史研究的开拓者。","badge":"🏛️"}},
    {"masterId":3,"title":"1957·万元之择","bg_desc":"1957年，肖纪美带着家人登上回国的轮船。美国移民局官员以中美未建交为由，无理扣下他一万美金的旅行支票——这在当时是一笔巨款。他们威胁利诱：「留在美国，一切好说；执意要走，这笔钱就别想要了。」","optionA":"为一万美金妥协，接受条件留在美国","optionB":"放弃钱财坚持回国，笑称「先存你这里，但要算利息」","resultA":{"title":"留在彼岸","text":"你为一万美金妥协了。在美国，你拥有稳定高薪的工作和优越的研究条件，成为了一名成功的材料工程师。但内心深处，你始终无法忘记那个新生的祖国和等待你的学生们。历史评价：一位优秀的工程师，但中国材料学失去了一位「凤凰三杰」之一。","badge":""},"resultB":{"title":"「先存你这里，但要算利息」","text":"你微笑着对美国官员说：「我先把钱存在你这里，但我要算利息的。」毅然踏上回国之路。15年后的1972年，尼克松总统访华时竟真的完成了「还钱」任务，这成了中美关系史上的一段趣闻。你回国后在北京钢铁学院任教五十余载，秉持「终身为士不为仕」的理念，培养六十余名研究生，著作等身。历史评价：中国材料学泰斗，「终身为士不为仕」的师者典范。","badge":"💎"}},
    {"masterId":4,"title":"1963·戈壁征召","bg_desc":"1963年，你已是北京钢铁工业学院知名的金属物理教授，正带领学生深入研究高温蠕变理论。一天，组织上秘密找到你：「国家需要你，去一个很远的地方，做一件很重要的事，但不能告诉任何人你去哪里、做什么。」","optionA":"留在学术界，继续培养研究生、著书立说","optionB":"隐姓埋名，奔赴青海戈壁滩投身核武器研制","resultA":{"title":"象牙塔中的学者","text":"你选择留在校园，继续从事金属物理教学和研究。你培养了许多优秀学生，发表了大量论文，在学术圈享有盛誉。但多年后，当蘑菇云在罗布泊升起的那一刻，你心中涌起一丝复杂的叹息。历史评价：一位杰出的教育家和学者，但错过了一段波澜壮阔的强国史诗。","badge":""},"resultB":{"title":"戈壁深处的无名英雄","text":"你接受了征召，隐姓埋名奔赴青海戈壁滩的221基地。从此，烟斗和闹钟陪伴着你在另一个战场——爆轰物理、特殊材料冶金、实验核物理的研究中继续奋战。1964年10月16日，当中国第一颗原子弹成功爆炸的消息传遍世界时，你默默地在戈壁滩上握紧了拳头，眼中满是泪水。历史评价：「两弹」功臣，金属蠕变研究奠基人，用一生践行「金石人生，只为兴邦」。","badge":"☢️"}},
    {"masterId":5,"title":"1980s·教材之路","bg_desc":"1980年代，胡赓祥在上海交通大学主讲《材料科学基础》。当时的材料科学教材分为三本独立的书：物理冶金学、高分子物理学、陶瓷学，学生需要同时学习三门课程，知识体系割裂。你想要改变这种状况……","optionA":"沿袭传统，分别编写三门独立教材","optionB":"大胆创新，将三门学科融合为一本统一教材","resultA":{"title":"守成的编者","text":"你选择沿袭传统路线，编写了三本各自独立的教材。虽然每本都很扎实，但学生们依然在三个割裂的知识体系之间来回切换，难以形成统一的材料科学思维。你的教材出版了，但很快被新的融合教材所取代。历史评价：一位尽职的教材编写者，但未能突破传统框架。","badge":""},"resultB":{"title":"融合的开创者","text":"你决定大胆创新，与蔡珣、戎咏华教授携手，将「物理冶金学」「高分子物理学」「陶瓷学」三门课程有机融合，编写了划时代的《材料科学基础》。这不是简单的拼凑，而是将三大材料的微观特性和宏观规律真正建立在共同理论基础上。教材先后获评国家精品课程、全国优秀教材一等奖，至今仍是数百万材料学子的必读经典。历史评价：中国材料科学教育体系的重要奠基人，融合教育的先行者。","badge":"📖"}}
]

# === CSS (expanded with new features) ===
css_str = '''*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg-dark:#0f0f14;--bg-card:#1a1a24;--bg-card-hover:#242432;--steel:#8a8fa3;--steel-light:#b8bcc9;--fire:#f4813a;--fire-bright:#ffb347;--gold:#e8b640;--gold-bright:#f5d76e;--success:#4caf91;--danger:#e05555;--text:#d8d8e0;--text-dim:#9a9ab0;--text-bright:#f0f0f5;--border:#2e2e3c;--accent-blue:#5b9ed4;--accent-purple:#b878d4;--shadow:0 4px 24px rgba(0,0,0,0.5)}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei","Helvetica Neue",sans-serif;background:var(--bg-dark);color:var(--text);min-height:100vh;overflow-x:hidden;position:relative}
body::before{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 50% 0%,rgba(244,129,58,0.12) 0%,transparent 50%),radial-gradient(ellipse at 80% 100%,rgba(91,158,212,0.08) 0%,transparent 50%),radial-gradient(ellipse at 20% 80%,rgba(184,120,212,0.06) 0%,transparent 50%);pointer-events:none;z-index:0}
#bg-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background-size:cover;background-position:center;background-repeat:no-repeat;opacity:.06;pointer-events:none;z-index:0;transition:all 1s ease}
#particles-container{position:fixed;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:0;overflow:hidden}
.particle{position:absolute;border-radius:50%;animation:floatUp linear infinite;opacity:0}
@keyframes floatUp{0%{transform:translateY(100vh) scale(0);opacity:0}10%{opacity:1}90%{opacity:.3}100%{transform:translateY(-10vh) scale(1);opacity:0}}
.container{max-width:520px;margin:0 auto;padding:20px 16px 60px;min-height:100vh;position:relative;z-index:2}
.screen{display:none}.screen.active{display:block;animation:fadeIn .5s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{box-shadow:0 0 8px rgba(244,129,58,.3)}50%{box-shadow:0 0 24px rgba(244,129,58,.6)}}
@keyframes badgeGlow{0%,100%{filter:drop-shadow(0 0 8px rgba(232,182,64,0.3))}50%{filter:drop-shadow(0 0 24px rgba(232,182,64,0.7))}}
@keyframes sparkle{0%,100%{opacity:.2;transform:translateY(0)}50%{opacity:1;transform:translateY(-12px)}}
@keyframes glimmer{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}

.home-header{text-align:center;padding:40px 0 20px}
.anvil-icon{font-size:60px;margin-bottom:8px;display:block;animation:pulse 2s ease-in-out infinite;filter:drop-shadow(0 0 16px rgba(244,129,58,.4))}
.home-header h1{font-size:30px;font-weight:800;background:linear-gradient(135deg,var(--fire-bright),var(--fire),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:3px;margin-bottom:8px}
.home-header .subtitle{font-size:14px;color:var(--text-dim);letter-spacing:2px}
.sparks{display:flex;justify-content:center;gap:10px;margin:12px 0 20px}
.spark{width:5px;height:5px;background:var(--fire);border-radius:50%;animation:sparkle 1.5s ease-in-out infinite}
.spark:nth-child(2){animation-delay:.3s;background:var(--gold)}.spark:nth-child(3){animation-delay:.6s;background:var(--fire-bright)}.spark:nth-child(4){animation-delay:.9s;background:var(--gold-bright)}.spark:nth-child(5){animation-delay:1.2s;background:var(--fire)}
.intro-text{text-align:center;font-size:14px;color:var(--text-dim);line-height:1.8;margin-bottom:28px;padding:0 12px}
.intro-text span{color:var(--fire);font-weight:600}
.btn{display:block;width:100%;padding:14px 24px;border:none;border-radius:12px;font-size:16px;font-weight:700;cursor:pointer;transition:all .2s;letter-spacing:1px;font-family:inherit;position:relative;overflow:hidden}
.btn:active{transform:scale(.97)}.btn-primary{background:linear-gradient(135deg,var(--fire),#d9632e);color:#fff;box-shadow:0 4px 16px rgba(244,129,58,.3)}.btn-primary:hover{box-shadow:0 6px 24px rgba(244,129,58,.45);transform:translateY(-1px)}.btn-secondary{background:var(--bg-card);color:var(--steel-light);border:1px solid var(--border)}.btn-secondary:hover{background:var(--bg-card-hover);border-color:var(--steel)}.btn-accent{background:linear-gradient(135deg,var(--gold),#c9942a);color:#1a1a1f;box-shadow:0 4px 16px rgba(232,182,64,.3)}.btn-accent:hover{box-shadow:0 6px 24px rgba(232,182,64,.45);transform:translateY(-1px)}
.home-actions{display:flex;flex-direction:column;gap:12px}
.stats-bar{display:flex;justify-content:center;gap:20px;margin-top:24px;padding:16px;background:rgba(26,26,36,.7);border-radius:12px;border:1px solid var(--border);flex-wrap:wrap;backdrop-filter:blur(10px)}
.stat-item{text-align:center;min-width:70px}.stat-value{font-size:24px;font-weight:800;color:var(--gold)}.stat-label{font-size:11px;color:var(--text-dim);margin-top:2px}
.back-btn{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--steel);cursor:pointer;padding:8px 0;margin-bottom:8px;border:none;background:none;font-family:inherit;transition:color .2s}.back-btn:hover{color:var(--steel-light)}
.screen-title{font-size:22px;font-weight:700;text-align:center;margin-bottom:6px;color:var(--text-bright)}.screen-subtitle{font-size:13px;color:var(--text-dim);text-align:center;margin-bottom:24px}

/* Level Cards */
.level-cards{display:flex;flex-direction:column;gap:12px}
.level-card{background:rgba(26,26,36,.85);border:1px solid var(--border);border-radius:14px;padding:16px 18px;cursor:pointer;transition:all .25s;display:flex;align-items:center;gap:14px;position:relative;overflow:hidden;backdrop-filter:blur(10px)}
.level-card:hover:not(.locked){background:rgba(36,36,50,.9);border-color:var(--fire);transform:translateX(4px);box-shadow:0 4px 20px rgba(244,129,58,.2)}
.level-card.locked{opacity:.45;cursor:not-allowed;filter:grayscale(.7)}.level-card.completed{border-color:var(--success)}
.level-card.completed::after{content:'\\2713';position:absolute;right:16px;top:50%;transform:translateY(-50%);font-size:22px;color:var(--success);font-weight:700}
.level-num{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;flex-shrink:0;background:rgba(15,15,20,.8);border:2px solid var(--border);color:var(--steel)}
.level-card.completed .level-num{background:linear-gradient(135deg,var(--success),#3a8a6e);color:#fff;border-color:var(--success)}.level-card:not(.locked):not(.completed) .level-num{border-color:var(--fire);color:var(--fire)}
.level-info{flex:1}.level-name{font-size:15px;font-weight:700;color:var(--text-bright);margin-bottom:3px}.level-master{font-size:12px;color:var(--steel)}.level-badge{font-size:26px;flex-shrink:0}.level-scores{font-size:11px;color:var(--text-dim);margin-top:2px}

/* Intro Screen */
.intro-screen{padding-top:4px}.intro-card{background:rgba(26,26,36,.9);border:1px solid var(--border);border-radius:20px;overflow:hidden;margin-bottom:16px;backdrop-filter:blur(10px)}
.intro-banner{background:linear-gradient(135deg,rgba(244,129,58,.15),rgba(91,158,212,.1));padding:20px;text-align:center;border-bottom:1px solid var(--border);position:relative}
.intro-portrait{width:100%;max-width:250px;border-radius:16px;margin:0 auto 12px;display:block;box-shadow:0 4px 20px rgba(0,0,0,.4);border:2px solid rgba(255,255,255,.1)}
.intro-banner .master-emoji{font-size:48px;display:block;margin-bottom:6px}.intro-banner .master-name{font-size:22px;font-weight:800;color:var(--text-bright);margin-bottom:4px}
.intro-banner .master-title{font-size:13px;color:var(--fire);font-weight:600}.intro-banner .master-subtitle{font-size:11px;color:var(--text-dim);margin-top:4px}
.intro-body{padding:16px 20px}.intro-section{margin-bottom:14px}.intro-section:last-child{margin-bottom:0}
.intro-section-title{font-size:13px;font-weight:700;color:var(--gold);margin-bottom:6px;display:flex;align-items:center;gap:6px}
.intro-section-title::before{content:'';display:inline-block;width:3px;height:14px;background:var(--gold);border-radius:2px}
.intro-section p{font-size:13px;color:var(--text-dim);line-height:1.8}
.intro-timeline{position:relative;padding-left:18px}.intro-timeline::before{content:'';position:absolute;left:4px;top:4px;bottom:4px;width:1px;background:var(--border)}
.timeline-item{position:relative;padding:0 0 8px 14px;font-size:11px;color:var(--text-dim);line-height:1.5}.timeline-item::before{content:'';position:absolute;left:-16px;top:5px;width:5px;height:5px;background:var(--fire);border-radius:50%}
.timeline-item .tl-year{color:var(--steel);font-weight:700;margin-right:4px}
.intro-quote{background:linear-gradient(135deg,rgba(244,129,58,.1),transparent);border-left:3px solid var(--fire);padding:10px 14px;margin:12px 0;border-radius:0 8px 8px 0}
.intro-quote p{font-size:13px;color:var(--fire-bright);font-weight:600;font-style:italic;line-height:1.5}
.intro-actions{padding:4px 20px 20px;display:flex;flex-direction:column;gap:8px}
.intro-decision-btn{background:linear-gradient(135deg,rgba(184,120,212,.15),rgba(91,158,212,.1));border:1.5px solid rgba(184,120,212,.3);color:var(--accent-purple);font-weight:700;font-size:14px;transition:all .2s}
.intro-decision-btn:hover{background:linear-gradient(135deg,rgba(184,120,212,.25),rgba(91,158,212,.15));border-color:var(--accent-purple)}

/* Quiz */
.quiz-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.quiz-master{font-size:13px;color:var(--fire);font-weight:600}.quiz-progress-text{font-size:12px;color:var(--text-dim)}
.progress-bar{width:100%;height:6px;background:rgba(26,26,36,.8);border-radius:3px;margin-bottom:24px;overflow:hidden;position:relative}
.progress-bar::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.05),transparent);animation:glimmer 2s linear infinite;background-size:200% 100%}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--fire),var(--fire-bright));border-radius:3px;transition:width .4s;box-shadow:0 0 10px rgba(244,129,58,.4)}
.question-card{background:rgba(26,26,36,.9);border:1px solid var(--border);border-radius:16px;padding:24px 20px;margin-bottom:16px;backdrop-filter:blur(10px)}
.question-num{font-size:11px;color:var(--steel);margin-bottom:6px}.question-text{font-size:15px;font-weight:600;color:var(--text-bright);line-height:1.7;margin-bottom:16px}
.options-list{display:flex;flex-direction:column;gap:8px}
.option-btn{display:block;width:100%;text-align:left;padding:13px 16px;background:rgba(15,15,20,.6);border:1.5px solid var(--border);border-radius:10px;color:var(--text);font-size:14px;cursor:pointer;transition:all .2s;font-family:inherit;line-height:1.4}
.option-btn:hover{background:rgba(42,42,54,.8);border-color:var(--steel)}.option-btn:active{transform:scale(.98)}
.option-btn.correct{background:rgba(76,175,145,.15);border-color:var(--success);color:var(--success);box-shadow:0 0 12px rgba(76,175,145,.2)}
.option-btn.wrong{background:rgba(224,85,85,.15);border-color:var(--danger);color:var(--danger);box-shadow:0 0 12px rgba(224,85,85,.2)}
.option-btn.disabled{pointer-events:none;opacity:.7}.option-btn.disabled:not(.correct):not(.wrong){opacity:.4}
.feedback-text{text-align:center;font-size:13px;margin:12px 0;min-height:18px;font-weight:600}
.feedback-text.correct{color:var(--success)}.feedback-text.wrong{color:var(--danger)}

/* Hint Button */
.hint-row{display:flex;justify-content:flex-end;margin-top:-10px;margin-bottom:12px}
.hint-btn{display:inline-flex;align-items:center;gap:5px;font-size:12px;color:var(--gold);background:rgba(232,182,64,.08);border:1px solid rgba(232,182,64,.25);border-radius:20px;padding:5px 14px;cursor:pointer;font-family:inherit;transition:all .2s}
.hint-btn:hover{background:rgba(232,182,64,.18);border-color:var(--gold);box-shadow:0 0 12px rgba(232,182,64,.15)}
.hint-btn:active{transform:scale(.96)}
.hint-btn.used{opacity:.4;pointer-events:none;color:var(--text-dim);border-color:var(--border);background:rgba(26,26,36,.5)}

/* Hint Overlay */
.hint-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:60;display:flex;align-items:center;justify-content:center;animation:fadeIn .25s ease}
.hint-popup{background:rgba(26,26,36,.98);border:2px solid var(--gold);border-radius:18px;padding:24px 22px;max-width:400px;width:90%;text-align:center;animation:slideUp .35s ease;box-shadow:0 8px 40px rgba(232,182,64,.2)}
.hint-popup .hint-icon{font-size:42px;display:block;margin-bottom:8px}
.hint-popup .hint-title{font-size:15px;font-weight:700;color:var(--gold);margin-bottom:12px}
.hint-popup .hint-text{font-size:13px;color:var(--text-bright);line-height:1.7;margin-bottom:18px}
.hint-popup .hint-close{display:inline-block;padding:8px 28px;background:linear-gradient(135deg,var(--gold),#c9942a);color:#1a1a1f;border:none;border-radius:10px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit;transition:all .2s}
.hint-popup .hint-close:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(232,182,64,.4)}

/* Wrong Answer Comic Popup */
.comic-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.7);z-index:50;display:flex;align-items:center;justify-content:center;animation:fadeIn .3s ease}
.comic-popup{background:rgba(26,26,36,.98);border:2px solid var(--fire);border-radius:20px;padding:24px 20px;max-width:380px;width:90%;text-align:center;animation:slideUp .4s ease;box-shadow:0 8px 40px rgba(244,129,58,.2)}
@keyframes slideUp{from{transform:translateY(40px);opacity:0}to{transform:translateY(0);opacity:1}}
.comic-avatar{width:90px;height:90px;border-radius:50%;margin:0 auto 12px;background-size:cover;background-position:center;border:3px solid var(--fire);box-shadow:0 0 20px rgba(244,129,58,.3);animation:badgeGlow 2s infinite}
.comic-name{font-size:16px;font-weight:800;color:var(--fire-bright);margin-bottom:4px}
.comic-bubble{background:rgba(244,129,58,.08);border:1px solid rgba(244,129,58,.2);border-radius:12px;padding:14px 16px;margin:12px 0;position:relative;font-size:13px;color:var(--text-bright);line-height:1.6}
.comic-bubble::before{content:'';position:absolute;top:-8px;left:50%;transform:translateX(-50%);width:0;height:0;border-left:8px solid transparent;border-right:8px solid transparent;border-bottom:8px solid rgba(244,129,58,.08)}
.comic-btn{display:inline-block;padding:10px 32px;background:linear-gradient(135deg,var(--fire),#d9632e);color:#fff;border:none;border-radius:10px;font-size:14px;font-weight:700;cursor:pointer;margin-top:8px;font-family:inherit;transition:all .2s}
.comic-btn:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(244,129,58,.4)}

/* Result */
.result-card{background:rgba(26,26,36,.9);border:1px solid var(--border);border-radius:20px;padding:28px 24px;text-align:center;margin-bottom:20px;backdrop-filter:blur(10px)}
.result-icon{font-size:56px;display:block;margin-bottom:10px}
.result-badge-icon{font-size:64px;display:block;margin-bottom:8px;animation:badgeGlow 2s ease-in-out infinite}
.result-title{font-size:20px;font-weight:700;color:var(--text-bright);margin-bottom:6px}
.result-badge-name{font-size:15px;font-weight:700;color:var(--gold);margin-bottom:12px}
.result-score{font-size:32px;font-weight:800;margin:8px 0}.result-score.pass{color:var(--success)}.result-score.fail{color:var(--danger)}
.result-detail{font-size:13px;color:var(--text-dim);line-height:1.8}
.result-ach{display:inline-block;background:rgba(232,182,64,.1);border:1px solid var(--gold);border-radius:8px;padding:5px 12px;margin:4px;font-size:11px;color:var(--gold);font-weight:600;animation:fadeIn .5s}
.result-actions{display:flex;flex-direction:column;gap:8px}

/* Decision Screen */
.decision-screen{padding-top:4px}.decision-card{background:rgba(26,26,36,.9);border:1px solid var(--border);border-radius:20px;overflow:hidden;margin-bottom:16px;backdrop-filter:blur(10px)}
.decision-scene{width:100%;height:200px;object-fit:cover;display:block;border-bottom:1px solid var(--border)}
.decision-body{padding:20px}.decision-label{font-size:11px;color:var(--accent-purple);font-weight:700;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px}
.decision-title{font-size:20px;font-weight:800;color:var(--text-bright);margin-bottom:12px}
.decision-desc{font-size:14px;color:var(--text-dim);line-height:1.8;margin-bottom:20px}
.decision-choices{display:flex;flex-direction:column;gap:12px}
.choice-btn{padding:16px 20px;background:rgba(15,15,20,.7);border:2px solid var(--border);border-radius:14px;text-align:left;cursor:pointer;transition:all .25s;font-family:inherit;color:var(--text)}
.choice-btn:hover{background:rgba(36,36,50,.8);border-color:var(--accent-purple);transform:translateX(4px);box-shadow:0 4px 16px rgba(184,120,212,.15)}
.choice-btn .choice-label{font-size:10px;color:var(--accent-purple);font-weight:700;letter-spacing:1px;margin-bottom:4px}
.choice-btn .choice-text{font-size:14px;color:var(--text-bright);font-weight:600;line-height:1.5}
.choice-btn .choice-hint{font-size:11px;color:var(--text-dim);margin-top:4px}

/* Decision Result */
.decision-result-card{background:rgba(26,26,36,.9);border:1px solid var(--border);border-radius:20px;overflow:hidden;margin-bottom:16px;backdrop-filter:blur(10px)}
.decision-result-banner{padding:28px 24px;text-align:center}
.decision-result-banner .dr-icon{font-size:56px;display:block;margin-bottom:8px}
.decision-result-banner .dr-title{font-size:18px;font-weight:800;color:var(--text-bright);margin-bottom:4px}
.decision-result-banner .dr-subtitle{font-size:12px;color:var(--text-dim)}
.decision-result-body{padding:16px 24px 24px}.decision-result-body p{font-size:13px;color:var(--text-dim);line-height:1.8}

/* Achievements */
.ach-categories{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px;justify-content:center}
.ach-cat-btn{font-size:11px;padding:6px 12px;border-radius:20px;border:1px solid var(--border);background:rgba(26,26,36,.8);color:var(--text-dim);cursor:pointer;font-family:inherit;transition:all .2s}
.ach-cat-btn.active{background:var(--fire);color:#fff;border-color:var(--fire)}.ach-cat-btn:hover:not(.active){border-color:var(--steel);color:var(--steel-light)}
.ach-count{text-align:center;font-size:13px;color:var(--text-dim);margin-bottom:14px}.ach-count span{color:var(--gold);font-weight:700;font-size:18px}
.achievements-grid{display:grid;grid-template-columns:1fr;gap:8px;margin-bottom:20px}@media(min-width:420px){.achievements-grid{grid-template-columns:repeat(2,1fr)}}
.achievement-card{background:rgba(26,26,36,.8);border:1px solid var(--border);border-radius:12px;padding:14px;display:flex;align-items:center;gap:10px;transition:all .2s}
.achievement-card.earned{border-color:var(--gold);background:linear-gradient(135deg,rgba(232,182,64,.06) 0%,rgba(26,26,36,.8) 100%)}
.achievement-card.locked{opacity:.35;filter:grayscale(.9)}
.ach-icon{font-size:28px;flex-shrink:0;width:38px;text-align:center}
.ach-detail{flex:1;min-width:0}.ach-detail-name{font-size:13px;font-weight:700;color:var(--text-bright);margin-bottom:2px}
.ach-detail-desc{font-size:10px;color:var(--text-dim);line-height:1.4}
.ach-category-tag{font-size:9px;padding:2px 7px;border-radius:10px;font-weight:600;display:inline-block;margin-top:3px}
.tag-badge{background:rgba(232,182,64,.15);color:var(--gold)}.tag-perfect{background:rgba(255,107,107,.15);color:#ff6b6b}
.tag-milestone{background:rgba(91,158,212,.15);color:var(--accent-blue)}.tag-skill{background:rgba(76,175,145,.15);color:var(--success)}
.tag-grit{background:rgba(244,129,58,.15);color:var(--fire)}.tag-ultimate{background:rgba(184,120,212,.15);color:var(--accent-purple)}
.tag-decision{background:rgba(184,120,212,.15);color:var(--accent-purple)}

/* Misc */
.forge-bg{position:fixed;bottom:0;left:0;right:0;height:250px;pointer-events:none;z-index:0;background:linear-gradient(0deg,rgba(244,129,58,.05) 0%,transparent 100%)}
.glow-line{height:1px;background:linear-gradient(90deg,transparent,rgba(244,129,58,.3),transparent);margin:8px 0}
.toast{position:fixed;top:20px;left:50%;transform:translateX(-50%);background:rgba(26,26,36,.95);color:var(--text-bright);padding:12px 24px;border-radius:10px;font-size:14px;font-weight:600;border:1px solid var(--gold);z-index:100;pointer-events:none;opacity:0;transition:opacity .3s;box-shadow:var(--shadow);max-width:90vw;text-align:center}
.toast.show{opacity:1;z-index:200}.toast.ach{animation:toastPop .5s ease}
@keyframes toastPop{0%{transform:translateX(-50%) scale(.8);opacity:0}50%{transform:translateX(-50%) scale(1.05)}100%{transform:translateX(-50%) scale(1);opacity:1}}
.reset-section{text-align:center;margin-top:28px;padding-top:16px;border-top:1px solid var(--border)}
.reset-btn{font-size:12px;color:var(--text-dim);background:none;border:none;cursor:pointer;font-family:inherit;padding:8px 16px;border-radius:8px;transition:all .2s}
.reset-btn:hover{color:var(--danger);background:rgba(224,85,85,.1)}
@media(max-width:360px){.home-header h1{font-size:24px}.level-card{padding:12px 14px}.intro-banner{padding:16px 14px}.intro-body{padding:14px}.comic-popup{padding:18px 14px}}

/* Decision badge highlight */
.decision-badge{display:inline-block;font-size:32px;padding:12px;background:rgba(26,26,36,.8);border-radius:16px;border:2px solid var(--accent-purple);margin:8px 0;animation:badgeGlow 2s ease-in-out infinite}
'''

# === GENERATE JS ===
js_code = '''var MASTERS=''' + json.dumps(MASTERS, ensure_ascii=False) + ''';\n
var DECISIONS=''' + json.dumps(DECISIONS, ensure_ascii=False) + ''';\n
var PORTRAITS=''' + json.dumps(portraits) + ''';\n
var SCENES=''' + json.dumps(scenes) + ''';\n
var FORGE_BG=''' + json.dumps(forge_bg) + ''';\n
''' + r'''
var ACHIEVEMENTS=[
  {id:'badge_1',name:'冶金热力学之章',desc:'通过第1关：魏寿昆',icon:'🧪',category:'badge',check:function(p){return!!p.badges[1]}},
  {id:'badge_2',name:'贝茵体相变之章',desc:'通过第2关：柯俊',icon:'⚙️',category:'badge',check:function(p){return!!p.badges[2]}},
  {id:'badge_3',name:'材料防护之章',desc:'通过第3关：肖纪美',icon:'🛡️',category:'badge',check:function(p){return!!p.badges[3]}},
  {id:'badge_4',name:'国之重器之章',desc:'通过第4关：张兴钤',icon:'⭐',category:'badge',check:function(p){return!!p.badges[4]}},
  {id:'badge_5',name:'材料育人之章',desc:'通过第5关：胡赓祥',icon:'📚',category:'badge',check:function(p){return!!p.badges[5]}},
  {id:'perfect_any',name:'完美学者',desc:'任意关卡获得满分 8/8',icon:'💯',category:'perfect',check:function(p){return Object.values(p.bestScores||{}).some(function(s){return s>=8})}},
  {id:'perfect_all',name:'钢铁完人',desc:'全部5个关卡均满分通关',icon:'🌟',category:'ultimate',check:function(p){return MASTERS.every(function(m){return (p.bestScores||{})[m.id]>=8})}},
  {id:'first_pass',name:'初生牛犊',desc:'首次通关任意关卡',icon:'🐂',category:'milestone',check:function(p){return Object.keys(p.completed||{}).length>=1}},
  {id:'scholar_3',name:'冶金学者',desc:'通过3个关卡',icon:'📜',category:'milestone',check:function(p){return Object.keys(p.completed||{}).length>=3}},
  {id:'master_all',name:'钢铁宗师',desc:'通过全部5个关卡',icon:'👑',category:'milestone',check:function(p){return Object.keys(p.completed||{}).length>=5}},
  {id:'one_life',name:'一命通关',desc:'某一关一次性通过（无失败重试）',icon:'🎯',category:'skill',check:function(p){return !!(p.oneShot&&Object.keys(p.oneShot).length>0)}},
  {id:'eagle_eye',name:'火眼金睛',desc:'单题在3秒内正确回答',icon:'👁',category:'skill',check:function(p){return !!p.eagleEye}},
  {id:'speed_3',name:'闪电答题',desc:'连续3题在6秒内正确回答',icon:'⚡',category:'skill',check:function(p){return !!p.speedStreak}},
  {id:'streak_5',name:'五连绝世',desc:'单关连续答对5题',icon:'✨',category:'skill',check:function(p){return !!p.streak5}},
  {id:'comeback',name:'钢铁意志',desc:'某关失败后重新挑战并通关',icon:'💪',category:'grit',check:function(p){return !!p.comeback}},
  {id:'persistent',name:'百折不挠',desc:'某一关累计失败3次后终于通过',icon:'🔥',category:'grit',check:function(p){return !!p.persistent}},
  {id:'tryhard',name:'千锤百炼',desc:'累计答题超过100题',icon:'⛏',category:'grit',check:function(p){return (p.totalAnswered||0)>=100}},
  {id:'decision_all',name:'命运抉择者',desc:'完成全部5位大师的历史抉择',icon:'🎲',category:'decision',check:function(p){return DECISIONS.every(function(d){return !!(p.decisions&&p.decisions[d.masterId])})}},
  {id:'collector',name:'勋章收藏家',desc:'集齐全部5枚大师勋章',icon:'🏆',category:'ultimate',check:function(p){return MASTERS.every(function(m){return !!p.badges[m.id]})}},
  {id:'god',name:'钢铁之神',desc:'解锁全部成就（除本成就外）',icon:'🔱',category:'ultimate',check:function(p){
    var others=ACHIEVEMENTS.filter(function(a){return a.id!=='god'});
    return others.every(function(a){return a.check(p)});
  }}
];

var STORAGE_KEY='steel_spirit_v3';

function loadProgress(){
  try{var d=localStorage.getItem(STORAGE_KEY);if(d)return JSON.parse(d)}catch(e){}
  return {completed:{},badges:{},bestScores:{},achievements:{},totalAnswered:0,
    fails:{},oneShot:{},eagleEye:false,speedStreak:false,streak5:false,
    comeback:false,persistent:false,decisions:{}};
}

function saveProgress(p){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(p))}catch(e){}}

var progress=loadProgress();
var currentLevel=null,currentQuestionIndex=0,currentScore=0;
var currentStreak=0,currentSpeedCount=0,questionStartTime=0,answered=false,levelHadFail=false;
var wrongAnswerQueue=null;

// === Particle Background ===
function initParticles(){
  var c=document.getElementById('particles-container');
  if(!c)return;
  c.innerHTML='';
  var colors=['#f4813a','#e8b640','#ffb347','#5b9ed4'];
  for(var i=0;i<25;i++){
    var p=document.createElement('div');p.className='particle';
    p.style.left=Math.random()*100+'%';p.style.width=p.style.height=(2+Math.random()*4)+'px';
    p.style.background=colors[Math.floor(Math.random()*colors.length)];
    p.style.animationDuration=(6+Math.random()*12)+'s';
    p.style.animationDelay=Math.random()*10+'s';
    c.appendChild(p);
  }
}

// === Navigation ===
function navigateTo(screen,data){
  document.querySelectorAll('.screen').forEach(function(s){s.classList.remove('active')});
  var t=document.getElementById('screen-'+screen);
  if(t)t.classList.add('active');
  if(screen==='levels')renderLevels();
  if(screen==='intro'&&data)renderIntro(data);
  if(screen==='quiz'&&data)startQuiz(data);
  if(screen==='home'){renderHomeStats();updateForgeBg();}
  if(screen==='achievements')renderAchievements('all');
  if(screen==='decision'&&data)renderDecision(data);
  if(screen==='decision-result')renderDecisionResult();
  if(screen!=='home')updateForgeBg(null);
  window.scrollTo({top:0,behavior:'smooth'});
}

function updateForgeBg(img){
  var el=document.getElementById('bg-overlay');
  if(!el)return;
  if(img)el.style.backgroundImage='url('+img+')';
  else if(FORGE_BG)el.style.backgroundImage='url('+FORGE_BG+')';
}

// === Home ===
function renderHomeStats(){
  var c=Object.keys(progress.completed||{}).length;
  var a=Object.keys(progress.achievements||{}).length;
  var d=Object.keys(progress.decisions||{}).length;
  document.getElementById('stats-bar').innerHTML=
    '<div class="stat-item"><div class="stat-value">'+c+'/5</div><div class="stat-label">已通关卡</div></div>'+
    '<div class="stat-item"><div class="stat-value">'+d+'/5</div><div class="stat-label">历史抉择</div></div>'+
    '<div class="stat-item"><div class="stat-value">'+a+'/'+ACHIEVEMENTS.length+'</div><div class="stat-label">成就解锁</div></div>';
}

// === Levels ===
function renderLevels(){
  document.getElementById('level-cards').innerHTML=MASTERS.map(function(m,i){
    var done=!!(progress.completed&&progress.completed[m.id]);
    var locked=i>0&&!(progress.completed&&progress.completed[MASTERS[i-1].id]);
    var best=(progress.bestScores&&progress.bestScores[m.id])||0;
    var cls=done?'completed':(locked?'locked':'');
    var click=locked?'':'navigateTo(\'intro\','+m.id+')';
    return '<div class="level-card '+cls+'" onclick="'+click+'">'+
      '<div class="level-num">'+(done?'✓':m.id)+'</div>'+
      '<div class="level-info"><div class="level-name">第'+m.id+'关 · '+m.title+'</div>'+
      '<div class="level-master">'+m.emoji+' '+m.name+'</div>'+
      (done?'<div class="level-scores">最高 '+best+'/8 分</div>':'')+'</div>'+
      '<div class="level-badge">'+(locked?'🔒':(done?m.badge:'➤'))+'</div></div>';
  }).join('');
}

// === Intro ===
function renderIntro(levelId){
  var m=MASTERS.find(function(x){return x.id===levelId});if(!m)return;
  var tl=m.timeline.map(function(t){return '<div class="timeline-item"><span class="tl-year">'+t.year+'</span> '+t.text+'</div>';}).join('');
  var done=!!(progress.completed&&progress.completed[m.id]);
  var best=(progress.bestScores&&progress.bestScores[m.id])||0;
  var portrait=PORTRAITS[m.id]||'';
  document.getElementById('intro-content').innerHTML=
    '<div class="intro-card">'+
    '<div class="intro-banner" style="background:linear-gradient(135deg,'+m.color+'22,var(--bg-card))">'+
    (portrait?'<img class="intro-portrait" src="'+portrait+'" alt="'+m.name+'" loading="lazy">':'')+
    '<span class="master-emoji">'+m.emoji+'</span><div class="master-name">'+m.name+'</div>'+
    '<div class="master-title">'+m.title+'</div><div class="master-subtitle">'+m.subtitle+'</div></div>'+
    '<div class="intro-body">'+
    '<div class="intro-section"><div class="intro-section-title">生平概述</div><p>'+m.lifeStory+'</p></div>'+
    '<div class="intro-section"><div class="intro-section-title">学术贡献</div><p>'+m.achievements+'</p></div>'+
    (m.quote?'<div class="intro-quote"><p>'+m.quote+'</p></div>':'')+
    '<div class="intro-section"><div class="intro-section-title">关键时间线</div><div class="intro-timeline">'+tl+'</div></div></div>'+
    '<div class="intro-actions">'+
    '<button class="btn btn-primary" onclick="navigateTo(\'quiz\','+m.id+')">'+
    (done?'重新挑战（最高 '+best+'/8 分）':'⚔️ 开始闯关！答对5/8题即可通关')+'</button>'+
    '<button class="btn intro-decision-btn" onclick="navigateTo(\'decision\','+m.id+')">🎲 历史抉择：'+DECISIONS.find(function(d){return d.masterId===m.id}).title+'</button>'+
    '<button class="btn btn-secondary" onclick="navigateTo(\'levels\')">返回选关</button></div></div>';
}

// === Quiz ===
function startQuiz(levelId){
  var m=MASTERS.find(function(x){return x.id===levelId});if(!m)return;
  currentLevel=m;currentQuestionIndex=0;currentScore=0;currentStreak=0;currentSpeedCount=0;answered=false;
  levelHadFail=!!(progress.fails&&progress.fails[m.id]&&progress.fails[m.id]>0);
  wrongAnswerQueue=null;
  document.getElementById('quiz-master-name').textContent=m.emoji+' '+m.name;
  updateForgeBg(FORGE_BG);
  renderQuestion();
}

function renderQuestion(){
  var m=currentLevel,q=m.questions[currentQuestionIndex];
  answered=false;questionStartTime=Date.now();
  document.getElementById('quiz-progress').textContent=(currentQuestionIndex+1)+' / '+m.questions.length;
  document.getElementById('progress-fill').style.width=((currentQuestionIndex/m.questions.length)*100)+'%';
  document.getElementById('question-num').textContent='第'+(currentQuestionIndex+1)+'题';
  document.getElementById('question-text').textContent=(currentQuestionIndex+1)+'. '+q.q;
  document.getElementById('feedback-text').textContent='';
  document.getElementById('feedback-text').className='feedback-text';
  // Reset hint button
  var hb=document.getElementById('hint-btn');if(hb)hb.className='hint-btn';
  var L=['A','B','C','D'];
  document.getElementById('options-list').innerHTML=q.options.map(function(o,i){return '<button class="option-btn" onclick="selectAnswer('+i+')">'+L[i]+'. '+o+'</button>';}).join('');
}

function selectAnswer(idx){
  if(answered)return;answered=true;
  var el=(Date.now()-questionStartTime)/1000;
  var m=currentLevel,q=m.questions[currentQuestionIndex],correct=q.answer,ok=idx===correct;
  if(ok){currentScore++;currentStreak++;
    if(el<=3&&!progress.eagleEye){progress.eagleEye=true;saveProgress(progress);checkAchievements();showToast('👁 解锁成就：火眼金睛！');}
    if(el<=6){currentSpeedCount++;if(currentSpeedCount>=3&&!progress.speedStreak){progress.speedStreak=true;saveProgress(progress);checkAchievements();showToast('⚡ 解锁成就：闪电答题！');}}
    if(currentStreak>=5&&!progress.streak5){progress.streak5=true;saveProgress(progress);checkAchievements();showToast('✨ 解锁成就：五连绝世！');}
  }else{currentStreak=0;currentSpeedCount=0;}
  progress.totalAnswered=(progress.totalAnswered||0)+1;saveProgress(progress);checkAchievements();
  var btns=document.querySelectorAll('.option-btn');
  btns.forEach(function(b,i){b.classList.add('disabled');if(i===correct)b.classList.add('correct');if(i===idx&&!ok)b.classList.add('wrong');});
  var fb=document.getElementById('feedback-text');
  fb.textContent=ok?('✓ 回答正确！ 用时 '+el.toFixed(1)+'秒'):'✗ 回答错误';
  fb.className='feedback-text '+(ok?'correct':'wrong');
  document.getElementById('progress-fill').style.width=(((currentQuestionIndex+1)/m.questions.length)*100)+'%';

  if(!ok){
    // Show comic popup for wrong answer
    wrongAnswerQueue={master:m,question:q,correctIdx:correct};
    setTimeout(function(){showComicHint();},600);
  }else{
    setTimeout(function(){nextQuestion();},1000);
  }
}

function showComicHint(){
  if(!wrongAnswerQueue)return;
  var m=wrongAnswerQueue.master,q=wrongAnswerQueue.question,correct=wrongAnswerQueue.correctIdx;
  var portrait=PORTRAITS[m.id]||'';
  var L=['A','B','C','D'];
  var overlay=document.createElement('div');overlay.className='comic-overlay';overlay.id='comic-overlay';
  overlay.innerHTML='<div class="comic-popup">'+
    (portrait?'<div class="comic-avatar" style="background-image:url('+portrait+')"></div>':'<div style="font-size:48px;margin-bottom:8px">'+m.emoji+'</div>')+
    '<div class="comic-name">'+m.name+' · '+m.title+'</div>'+
    '<div class="comic-bubble">🤔 这道题的正确答案是 <b style="color:var(--success)">'+L[correct]+'. '+q.options[correct]+'</b><br><br><span style="font-size:12px;color:var(--text-dim)">'+q.hint+'</span></div>'+
    '<button class="comic-btn" onclick="closeComic()">我记住了！</button></div>';
  document.body.appendChild(overlay);
}

function closeComic(){
  var o=document.getElementById('comic-overlay');if(o)o.remove();
  wrongAnswerQueue=null;
  nextQuestion();
}

// === Hint System ===
function showHint(){
  if(answered)return;
  var m=currentLevel,q=m.questions[currentQuestionIndex];
  // Mark hint as used (disable further hints for this question)
  var hb=document.getElementById('hint-btn');if(hb)hb.classList.add('used');
  var overlay=document.createElement('div');overlay.className='hint-overlay';overlay.id='hint-overlay';
  overlay.innerHTML='<div class="hint-popup">'+
    '<span class="hint-icon">💡</span>'+
    '<div class="hint-title">提示</div>'+
    '<div class="hint-text">'+q.hint+'</div>'+
    '<button class="hint-close" onclick="closeHint()">知道了</button>'+
    '</div>';
  document.body.appendChild(overlay);
}

function closeHint(){
  var o=document.getElementById('hint-overlay');if(o)o.remove();
}

function nextQuestion(){
  currentQuestionIndex++;
  if(currentQuestionIndex>=currentLevel.questions.length)showResult();
  else renderQuestion();
}

// === Result ===
function showResult(){
  var m=currentLevel,passed=currentScore>=5,perfect=currentScore>=8;
  updateForgeBg(null);
  if(passed){
    if(levelHadFail&&!progress.comeback){progress.comeback=true;saveProgress(progress);checkAchievements();}
    var firstTime=!progress.completed[m.id];
    if(firstTime){if(!progress.fails||!progress.fails[m.id]){if(!progress.oneShot)progress.oneShot={};progress.oneShot[m.id]=true;saveProgress(progress);checkAchievements();}}
    if(progress.fails&&progress.fails[m.id]&&progress.fails[m.id]>=3&&!progress.persistent){progress.persistent=true;saveProgress(progress);checkAchievements();showToast('🔥 解锁成就：百折不挠！');}
    progress.completed[m.id]=true;progress.badges[m.id]=true;
    var prev=progress.bestScores[m.id]||0;if(currentScore>prev)progress.bestScores[m.id]=currentScore;
    saveProgress(progress);checkAchievements();
  }else{
    if(!progress.fails)progress.fails={};progress.fails[m.id]=(progress.fails[m.id]||0)+1;saveProgress(progress);
  }
  var card=document.getElementById('result-card'),acts=document.getElementById('result-actions'),newA=checkAchievements(true);
  if(passed){
    card.innerHTML='<span class="result-badge-icon">'+m.badge+'</span><div class="result-title">🎉 恭喜通关！</div>'+
      '<div class="result-badge-name">获得「'+m.badgeName+'」'+(perfect?' 💯':'')+'</div>'+
      '<div class="result-score pass">'+currentScore+'/8</div>'+
      (perfect?'<div class="result-detail" style="color:var(--gold);font-weight:700">🌟 满分通关！太厉害了！</div>':'')+
      '<div class="result-detail">'+m.name+' · '+m.title+'</div>'+
      (newA.length>0?'<div style="margin-top:10px">'+newA.map(function(a){return '<span class="result-ach">'+a.icon+' '+a.name+'</span>';}).join('')+'</div>':'');
    var nid=m.id<5?m.id+1:null;
    acts.innerHTML=(nid?'<button class="btn btn-primary" onclick="navigateTo(\'intro\','+nid+')">进入下一关</button>':'')+
      '<button class="btn btn-secondary" onclick="navigateTo(\'quiz\','+m.id+')">重新挑战（刷分）</button>'+
      '<button class="btn intro-decision-btn" onclick="navigateTo(\'decision\','+m.id+')">🎲 历史抉择</button>'+
      '<button class="btn btn-secondary" onclick="navigateTo(\'levels\')">返回选关</button>';
  }else{
    card.innerHTML='<span class="result-icon">🔧</span><div class="result-title">还需努力</div>'+
      '<div class="result-score fail">'+currentScore+'/8</div>'+
      '<div class="result-detail">需要答对5题才能通关<br>钢铁的锻造成就于千锤百炼，再来一次！<br><br>💡 提示：可以先去了解一下大师的生平哦~</div>';
    acts.innerHTML='<button class="btn btn-primary" onclick="navigateTo(\'intro\','+m.id+')">查看生平介绍</button>'+
      '<button class="btn btn-primary" style="background:linear-gradient(135deg,#d9632e,var(--fire))" onclick="navigateTo(\'quiz\','+m.id+')">重新挑战</button>'+
      '<button class="btn btn-secondary" onclick="navigateTo(\'levels\')">返回选关</button>';
  }
  document.querySelectorAll('.screen').forEach(function(s){s.classList.remove('active')});
  document.getElementById('screen-result').classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
}

function confirmQuitQuiz(){
  if(currentQuestionIndex>0&&!answered){if(confirm('确定要放弃当前关卡吗？当前进度不会保存。'))navigateTo('levels');}
  else if(answered&&currentQuestionIndex<currentLevel.questions.length){if(confirm('确定要放弃当前关卡吗？'))navigateTo('levels');}
  else{navigateTo('levels');}
}

// === Achievements ===
function checkAchievements(silent){
  var nw=[];
  ACHIEVEMENTS.forEach(function(a){if(progress.achievements&&progress.achievements[a.id])return;if(a.check(progress)){if(!progress.achievements)progress.achievements={};progress.achievements[a.id]=true;nw.push(a);}});
  if(nw.length>0){saveProgress(progress);if(!silent)nw.forEach(function(a){showToast(a.icon+' 解锁成就：'+a.name+'!','ach');});}
  return nw;
}

var achFilter='all';

function renderAchievements(filter){
  if(filter)achFilter=filter;
  var cats=['all','badge','perfect','milestone','skill','grit','decision','ultimate'];
  var cn={all:'全部',badge:'关卡勋章',perfect:'满分成就',milestone:'里程碑',skill:'答题技巧',grit:'坚毅不屈',decision:'历史抉择',ultimate:'终极成就'};
  document.getElementById('ach-categories').innerHTML=cats.map(function(c){return '<button class="ach-cat-btn'+(achFilter===c?' active':'')+'" onclick="renderAchievements(\''+c+'\')">'+cn[c]+'</button>';}).join('');
  var filtered=ACHIEVEMENTS.filter(function(a){return achFilter==='all'||a.category===achFilter});
  var ul=filtered.filter(function(a){return progress.achievements&&progress.achievements[a.id]}).length;
  document.getElementById('ach-count').innerHTML='已解锁 <span>'+ul+'</span> / '+filtered.length+' 项成就';
  document.getElementById('achievements-grid').innerHTML=filtered.map(function(a){
    var earned=!!(progress.achievements&&progress.achievements[a.id]);
    return '<div class="achievement-card '+(earned?'earned':'locked')+'"><div class="ach-icon">'+(earned?a.icon:'🔒')+'</div>'+
      '<div class="ach-detail"><div class="ach-detail-name">'+a.name+'</div><div class="ach-detail-desc">'+a.desc+'</div>'+
      '<span class="ach-category-tag tag-'+a.category+'">'+cn[a.category]+'</span></div></div>';
  }).join('');
}

// === Toast ===
var toastTimer=null;
function showToast(msg,cls){
  var t=document.getElementById('toast');if(toastTimer)clearTimeout(toastTimer);
  t.textContent=msg;t.className='toast show'+(cls?' '+cls:'');
  toastTimer=setTimeout(function(){t.classList.remove('show');t.className='toast';},3000);
}

// === Decision System ===
var decisionState=null;

function renderDecision(levelId){
  var d=DECISIONS.find(function(x){return x.masterId===levelId});if(!d)return;
  var m=MASTERS.find(function(x){return x.id===levelId});
  decisionState={decision:d,master:m};
  var scene=SCENES[m.id]||'';
  updateForgeBg(SCENES[m.id]||FORGE_BG);
  document.getElementById('decision-content').innerHTML=
    '<div class="decision-card">'+
    (scene?'<img class="decision-scene" src="'+scene+'" alt="历史场景" loading="lazy">':'')+
    '<div class="decision-body">'+
    '<div class="decision-label">⚡ 历史抉择</div>'+
    '<div class="decision-title">'+d.title+'</div>'+
    '<div class="decision-desc">'+d.bg_desc+'</div>'+
    '<div class="decision-choices">'+
    '<div class="choice-btn" onclick="makeChoice(\'A\')"><div class="choice-label">选择 A</div><div class="choice-text">'+d.optionA+'</div><div class="choice-hint">不同的选择，不同的人生轨迹</div></div>'+
    '<div class="choice-btn" onclick="makeChoice(\'B\')"><div class="choice-label">选择 B</div><div class="choice-text">'+d.optionB+'</div><div class="choice-hint">这是历史上大师的真实选择</div></div>'+
    '</div></div></div>';
}

function makeChoice(choice){
  var d=decisionState.decision;
  var m=decisionState.master;
  var result=choice==='B'?d.resultB:d.resultA;
  var isHistorical=choice==='B';

  // Save decision
  if(!progress.decisions)progress.decisions={};
  progress.decisions[d.masterId]=choice;
  saveProgress(progress);
  checkAchievements();

  updateForgeBg(null);
  document.getElementById('decision-result-content').innerHTML=
    '<div class="decision-result-card">'+
    '<div class="decision-result-banner" style="background:linear-gradient(135deg,'+(isHistorical?'var(--success)':'var(--steel)')+'22,var(--bg-card))">'+
    (result.badge?('<div class="decision-badge">'+result.badge+'</div>'):'<span class="dr-icon">'+(isHistorical?'✨':'🔮')+'</span>')+
    '<div class="dr-title" style="color:'+(isHistorical?'var(--gold)':'var(--steel)')+'">'+result.title+'</div>'+
    '<div class="dr-subtitle">'+(isHistorical?'✅ 历史真实选择':'⬜ 另一种可能')+' · '+m.emoji+' '+m.name+'</div></div>'+
    '<div class="decision-result-body"><p>'+result.text+'</p></div></div>'+
    '<div style="display:flex;flex-direction:column;gap:8px;padding:0 4px">'+
    (!isHistorical?'<button class="btn btn-primary" onclick="makeChoice(\'B\')">🔄 回到历史真实选择</button>':'')+
    '<button class="btn btn-secondary" onclick="navigateTo(\'intro\','+m.id+')">返回人物介绍</button>'+
    '<button class="btn btn-secondary" onclick="navigateTo(\'levels\')">返回选关</button></div>';
  document.querySelectorAll('.screen').forEach(function(s){s.classList.remove('active')});
  document.getElementById('screen-decision-result').classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
}

// === Reset ===
function resetProgress(){
  if(confirm('⚠️ 确定要重置全部游戏进度吗？此操作不可恢复！')){
    progress={completed:{},badges:{},bestScores:{},achievements:{},totalAnswered:0,
      fails:{},oneShot:{},eagleEye:false,speedStreak:false,streak5:false,comeback:false,persistent:false,decisions:{}};
    saveProgress(progress);renderAchievements('all');navigateTo('home');showToast('已重置全部进度');
  }
}

// === Init ===
initParticles();
renderHomeStats();
updateForgeBg(FORGE_BG);
if(window.location.hash==='#achievements')navigateTo('achievements');
'''

# === BUILD HTML ===
html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>钢铁精神 — 冶金大师闯关</title>
<style>''' + css_str + '''</style>
</head>
<body>
<div id="bg-overlay"></div>
<div id="particles-container"></div>
<div class="forge-bg"></div>

<main class="container" id="app">
  <div class="screen active" id="screen-home">
    <div class="home-header">
      <span class="anvil-icon">&#9876;&#65039;</span>
      <h1>钢铁精神</h1>
      <p class="subtitle">冶金大师 · 闯关挑战 · 历史抉择</p>
    </div>
    <div class="sparks"><div class="spark"></div><div class="spark"></div><div class="spark"></div><div class="spark"></div><div class="spark"></div></div>
    <p class="intro-text">五位<span>冶金大先生</span>，以钢铁铸脊梁。<br>闯过五道关卡，在<span>历史抉择</span>中重走大师之路，<br>解锁<span>19+</span>种成就，收集<span>勋章</span>，<br>传承中国冶金人的<span>钢铁精神</span>。</p>
    <div class="home-actions">
      <button class="btn btn-primary" onclick="navigateTo('levels')">⚔️ 开始闯关</button>
      <button class="btn btn-secondary" onclick="navigateTo('achievements')">🏆 成就收藏</button>
    </div>
    <div class="stats-bar" id="stats-bar"></div>
  </div>

  <div class="screen" id="screen-levels">
    <button class="back-btn" onclick="navigateTo('home')">&#8592; 回到首页</button>
    <h2 class="screen-title">选择关卡</h2>
    <p class="screen-subtitle">每位大师背后，都是一段钢铁传奇</p>
    <div class="level-cards" id="level-cards"></div>
  </div>

  <div class="screen" id="screen-intro">
    <button class="back-btn" onclick="navigateTo('levels')">&#8592; 返回选关</button>
    <div class="intro-screen" id="intro-content"></div>
  </div>

  <div class="screen" id="screen-quiz">
    <button class="back-btn" onclick="confirmQuitQuiz()">&#8592; 放弃本关</button>
    <div class="quiz-header">
      <span class="quiz-master" id="quiz-master-name"></span>
      <span class="quiz-progress-text" id="quiz-progress"></span>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="progress-fill" style="width:0%"></div></div>
    <div class="question-card">
      <div class="question-num" id="question-num"></div>
      <div class="question-text" id="question-text"></div>
      <div class="hint-row"><button class="hint-btn" id="hint-btn" onclick="showHint()">💡 查看提示</button></div>
      <div class="options-list" id="options-list"></div>
    </div>
    <p class="feedback-text" id="feedback-text"></p>
  </div>

  <div class="screen" id="screen-result">
    <div class="result-card" id="result-card"></div>
    <div class="result-actions" id="result-actions"></div>
  </div>

  <div class="screen" id="screen-decision">
    <button class="back-btn" onclick="navigateTo('levels')">&#8592; 返回选关</button>
    <div class="decision-screen" id="decision-content"></div>
  </div>

  <div class="screen" id="screen-decision-result">
    <button class="back-btn" onclick="navigateTo('levels')">&#8592; 返回选关</button>
    <div id="decision-result-content"></div>
  </div>

  <div class="screen" id="screen-achievements">
    <button class="back-btn" onclick="navigateTo('home')">&#8592; 回到首页</button>
    <h2 class="screen-title">成就收藏</h2>
    <p class="screen-subtitle">解锁全部成就，传承钢钢铁精神</p>
    <div class="ach-categories" id="ach-categories"></div>
    <div class="ach-count" id="ach-count"></div>
    <div class="achievements-grid" id="achievements-grid"></div>
    <div class="reset-section">
      <button class="reset-btn" onclick="resetProgress()">重置全部进度</button>
    </div>
  </div>
</main>

<div class="toast" id="toast"></div>

<script>
''' + js_code + '''
</script>
</body>
</html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html_content)

total_kb = sum(len(v) for v in portraits.values()) + sum(len(v) for v in scenes.values()) + len(forge_bg)
print(f'Written {len(html_content):,} chars to {OUT}')
print(f'File size: {os.path.getsize(OUT):,} bytes')
print(f'Images (base64): ~{total_kb//1024:,}KB')
