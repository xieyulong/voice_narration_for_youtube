"""Create the Step 1 bilingual timing-table copy for the White Pass redo."""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "materials_for_whitepass_train/Time_point_WhitePassScenicTrian.xlsx"
OUTPUT = ROOT / (
    "materials_for_whitepass_train/"
    "WhitePassScenicTrainRide_Redo_2026_06_24_27m15s_timing_narration.xlsx"
)


NARRATIONS = [
    [
        (
        "White Pass Scenic Train Ride begins in Skagway, Alaska.",
        "白隘口观光铁路之旅，就从阿拉斯加的史凯威开始。",
        ),
    ],
    [
        (
        "From sea level, the train begins climbing toward White Pass.",
        "列车从海平面的史凯威出发，开始向白隘口一路爬升。",
        ),
    ],
    [
        (
            "This is the White Pass railway maintenance base,",
            "这里是白隘口铁路的维修基地，",
        ),
        (
            "where locomotives and passenger cars are inspected and repaired",
            "机车和客车都在这里检修，",
        ),
        (
            "before they are ready to cross the mountains.",
            "为穿越山区做好准备。",
        ),
    ],
    [
        (
            "After reaching Denver,",
            "到达丹佛地区后，",
        ),
        (
            "the train crosses the east fork of the Skagway River.",
            "列车跨过史凯威河东支流。",
        ),
        (
            "Nearby, the Denver Glacier trail leads higher into the mountains.",
            "附近的丹佛冰川步道，通往更高处的山地。",
        ),
    ],
    [
        (
        "Clifton is a small railway point beside the green Skagway River valley.",
        "这里是克利夫顿铁路点。列车沿着史凯威河谷前进，铁路两旁是茂密的绿色山坡。",
        ),
    ],
    [
        (
            "The distant canyon wall once carried the words",
            "远处岩壁上曾写着",
        ),
        (
            "\"On to Alaska with Buchanan.\"",
            "“和布坎南一起前往阿拉斯加”。",
        ),
        (
            "The Buchanan Boys travel group came here year after year,",
            "布坎南男孩旅行团曾年年来到这里，",
        ),
        (
            "making this sign a classic landmark.",
            "让这块标语成为经典景点。",
        ),
    ],
    [
        (
            "Bridal Veil Falls begins in the glaciers",
            "新娘面纱瀑布发源于",
        ),
        (
            "of Mount Cleveland and Mount Clifford.",
            "克利夫兰山和克利福德山的冰川。",
        ),
        (
            "White water pours down the rock wall",
            "白色水流沿山壁倾泻而下，",
        ),
        (
            "like a drifting veil.",
            "像一层飘动的面纱。",
        ),
    ],
    [
        (
            "This is Black Cross Rock.",
            "这里是黑十字岩。",
        ),
        (
            "On August 3, 1898,",
            "1898年8月3日，",
        ),
        (
            "two railway workers died in a blasting accident.",
            "两名铁路工人在爆破事故中遇难，",
        ),
        (
            "The black cross on the rock honors their memory.",
            "岩石上的黑色十字架就是对他们的纪念。",
        ),
    ],
    [
        (
            "Heney Station is named for railway contractor Michael J. Heney.",
            "亨尼站以铁路承包商迈克尔·J·亨尼命名。",
        ),
        (
            "During the Gold Rush, freight first moved down by tramway,",
            "淘金时代，货物先通过缆车运下山谷，",
        ),
        (
            "then continued toward White Pass by pack horse.",
            "再由驮马送往白隘口。",
        ),
    ],
    [
        (
            "Glacier Station was once an important water stop",
            "冰川站曾是蒸汽机车爬坡时",
        ),
        (
            "for steam locomotives climbing the grade.",
            "的重要补水点。",
        ),
        (
            "Railway workers also stayed here",
            "铁路工人也曾在这里驻守，",
        ),
        (
            "to maintain this mountain line.",
            "维护这条高山线路。",
        ),
    ],
    [
        (
            "At Slippery Rock,",
            "在滑石岩，",
        ),
        (
            "the railway clings to the steep mountain wall,",
            "铁路贴着陡峭山壁穿行，",
        ),
        (
            "with Glacier Gorge directly below.",
            "下面就是冰川峡谷。",
        ),
        (
            "Early workers drilled and blasted into dangerous rock faces",
            "铁路早期施工时，工人必须在险峻的岩壁上钻孔爆破，",
        ),
        (
            "to carve out this roadbed.",
            "开出这条路基。",
        ),
    ],
    [
        (
            "This is Tunnel Mountain.",
            "这里是隧道山。",
        ),
        (
            "The train moves along a narrow mountainside,",
            "列车沿着狭窄的山腰前进，",
        ),
        (
            "where tunnels, bridges, and sharp curves",
            "铁路以隧道、桥梁和急弯",
        ),
        (
            "overcame the rugged White Pass terrain.",
            "克服了白隘口的险峻地形。",
        ),
    ],
    [
        (
            "Looking out from Inspiration Point,",
            "从灵感角望出去，",
        ),
        (
            "you can see Lynn Canal, Harding Mountain, and the Coast Range.",
            "可以看到林恩运河、哈丁山和海岸山脉。",
        ),
        (
            "This is one of the classic mountain views",
            "这是白隘口旅程中",
        ),
        (
            "on the White Pass journey.",
            "最经典的高山景观之一。",
        ),
    ],
    [
        (
            "Below the railway is Dead Horse Gulch,",
            "铁路下方就是死马峡谷，",
        ),
        (
            "a reminder of the difficult Gold Rush trail.",
            "提醒人们这里曾是艰难的淘金古道。",
        ),
        (
            "An estimated three thousand pack horses died on the White Pass route,",
            "据估计，约有三千匹驮马死在白隘口路上，",
        ),
        (
            "which is why it was also called the Dead Horse Trail.",
            "因此这条路也被称为“死马道”。",
        ),
    ],
    [
        (
            "This is the famous 18A Steel Bridge.",
            "这里是著名的18A钢桥。",
        ),
        (
            "It was once one of the most representative landmarks",
            "它曾是白隘口铁路",
        ),
        (
            "of the White Pass railway.",
            "最具代表性的地标之一，",
        ),
        (
            "Later, trains moved to a new alignment,",
            "列车后来改走新线路，",
        ),
        (
            "and the old bridge was retired from service.",
            "老桥也随之退出使用。",
        ),
    ],
    [
        (
            "Ahead is the tunnel on the newer route.",
            "前方是新线路上的隧道。",
        ),
        (
            "It bypassed the old Steel Bridge,",
            "它绕开了旧钢桥，",
        ),
        (
            "allowing the railway to carry heavier trains",
            "使铁路能够承载更重的列车，",
        ),
        (
            "and improving modern operating safety.",
            "也提高了现代运行的安全性。",
        ),
    ],
    [
        (
            "At White Pass Summit,",
            "到达白隘口山顶时，",
        ),
        (
            "nearly 3,000 ft above sea level near the U.S.-Canada border,",
            "铁路已经接近三千英尺，进入美加边境附近。",
        ),
        (
            "prospectors were once inspected",
            "淘金者当年要在这里接受检查，",
        ),
        (
            "and required to prove they carried a year's worth of supplies.",
            "并证明自己携带了足够维持一年生活的补给。",
        ),
    ],
    [
        (
            "On the return, as we pass the Steel Bridge again,",
            "回程再次经过钢桥时，",
        ),
        (
            "we see it quietly spanning the green slopes from a new angle.",
            "我们从不同角度看见它静静横跨在绿色山坡之间。",
        ),
        (
            "It makes it easier to feel how the early railway",
            "它让人更直观地感受到，",
        ),
        (
            "once crossed this gorge.",
            "早期铁路曾经怎样穿越这道峡谷。",
        ),
    ],
    [
        (
            "On the return past Inspiration Point,",
            "回程经过灵感角时，",
        ),
        (
            "Lynn Canal and the valley open before us again.",
            "林恩运河和山谷再次展现在眼前。",
        ),
        (
            "As the train descends toward Skagway,",
            "随着列车向史凯威下降，",
        ),
        (
            "the same scenery reveals different layers.",
            "同一片景色也呈现出不同的层次。",
        ),
    ],
    [
        (
            "On the descent,",
            "下山途中，",
        ),
        (
            "the train passes Tunnel Mountain again.",
            "列车再次经过隧道山。",
        ),
        (
            "As the elevation drops,",
            "随着海拔下降，",
        ),
        (
            "the exposed alpine slopes give way to thicker forest.",
            "裸露的高山坡地逐渐被更加茂密的森林取代。",
        ),
    ],
    [
        (
            "Near Foy,",
            "经过福伊附近时，",
        ),
        (
            "the railway enters mountain forest again.",
            "铁路重新进入山地森林。",
        ),
        (
            "After leaving the open alpine section,",
            "离开开阔的高山区域后，",
        ),
        (
            "the green scenery comes closer to the window.",
            "绿色景色变得更加贴近车窗。",
        ),
    ],
    [
        (
            "On the return past Black Cross Rock,",
            "回程经过黑十字岩时，",
        ),
        (
            "the roadside sign makes this memorial site clearer.",
            "路旁的标志让这处纪念地点更加清晰。",
        ),
        (
            "It honors two workers",
            "它纪念的是两名",
        ),
        (
            "who lost their lives building the railway.",
            "在铁路建设中失去生命的工人。",
        ),
    ],
    [
        (
            "Seen from the return side,",
            "从回程这一侧看，",
        ),
        (
            "Buchanan Rock blends into the forested canyon wall.",
            "布坎南岩融入了森林覆盖的峡谷山壁。",
        ),
        (
            "The old giant sign is now hard to read,",
            "昔日的巨大标语已经不易看清，",
        ),
        (
            "but this route still keeps the scenery that once drew visitors.",
            "但这条路线依然保留着当年吸引游客的景观。",
        ),
    ],
    [
        (
            "Descending, we see Clifton again,",
            "下山时再次看到克利夫顿，",
        ),
        (
            "marked by a simple sign beside the track.",
            "路旁的简单标牌标记着这个铁路地点。",
        ),
        (
            "These small railway points helped workers identify",
            "正是这些小型铁路点，帮助工作人员识别",
        ),
        (
            "and maintain the long mountain line.",
            "和维护漫长的山地线路。",
        ),
    ],
    [
        (
            "Back at Rocky Point,",
            "回到落基角时，",
        ),
        (
            "the train is already far below the summit.",
            "列车已经明显低于山顶。",
        ),
        (
            "Looking back through the forest,",
            "透过森林回望，",
        ),
        (
            "it is hard to imagine this journey climbed from sea level",
            "很难想象这趟旅程曾从海平面",
        ),
        (
            "all the way above the mountains.",
            "一路攀升到高山之上。",
        ),
    ],
    [
        (
            "On the return through Denver,",
            "回程再次经过丹佛，",
        ),
        (
            "we can see the place sign and a red railway car beside the track.",
            "路旁可以看到地点标牌和红色铁路车厢。",
        ),
        (
            "As Skagway gets closer,",
            "随着史凯威越来越近，",
        ),
        (
            "the river valley becomes greener again.",
            "河谷也重新变得更加翠绿。",
        ),
    ],
    [
        (
            "Back at Mile 2,",
            "回到2英里处，",
        ),
        (
            "the maintenance base marks the final stretch of the trip.",
            "维修基地标志着铁路旅程即将结束。",
        ),
        (
            "This working railway carried us into the mountains,",
            "正是这条仍在运转的铁路，把我们带入山中，",
        ),
        (
            "and it will continue welcoming the next train.",
            "也将继续迎接下一趟列车。",
        ),
    ],
    [
        (
            "After descending from White Pass,",
            "从白隘口下行之后，",
        ),
        (
            "the train returns to sea level in Skagway.",
            "列车回到海平面的史凯威。",
        ),
        (
            "This journey crossed magnificent natural scenery",
            "这趟旅程穿过壮丽的自然风景，",
        ),
        (
            "and the history left by the Klondike Gold Rush.",
            "也穿过了克朗代克淘金热留下的历史。",
        ),
    ],
]


def narration_pair(index: int) -> tuple[str, str]:
    segments = NARRATIONS[index]
    english = " ".join(segment[0] for segment in segments)
    chinese = "".join(segment[1] for segment in segments)
    return english, chinese


MISC_NARRATIONS = [
    (
        "01:00:07:03",
        [
            (
                "Today is day five of our Discovery Princess cruise from Vancouver to Anchorage.",
                "今天是我们乘坐“探索公主号”从温哥华前往安克雷奇航程的第五天。",
            ),
            (
                "After arriving in Skagway, we explored the town's historic downtown that morning.",
                "邮轮抵达史凯威后，我们上午游览了这座小镇历史悠久的市中心。",
            ),
            (
                "Now we are taking the shuttle ashore again to board the White Pass scenic train.",
                "现在，我们今天第二次乘坐接驳船上岸，准备搭乘白隘口观光火车。",
            ),
            (
                "Although Skagway has under 1,000 residents, its port is packed with cruise passengers.",
                "史凯威虽然人口不足一千，但港口依然挤满了来自各艘邮轮的游客。",
            ),
        ],
    ),
    (
        "01:02:20:02",
        [
            (
                "The train has no assigned seats, so passengers can choose any open seat.",
                "火车不设指定座位，乘客可以任选空位就座。",
            ),
        ],
    ),
    (
        "01:02:58:10",
        [
            (
                "The helicopter overhead likely carries visitors to nearby glaciers and other sights.",
                "盘旋在空中的直升机，很可能正载着游客前往附近的冰川和其他景点。",
            ),
        ],
    ),
    (
        "01:03:16:23",
        [
            (
                "The conductor checked our tickets, and the attendant explained the safety rules.",
                "列车员检查了车票，乘务员随后讲解了安全规定。",
            ),
        ],
    ),
    (
        "01:03:30:20",
        [
            (
                "As the train slowly leaves Skagway, the White Pass railway journey begins.",
                "随着火车缓缓驶出史凯威，白隘口铁路之旅正式开始。",
            ),
        ],
    ),
    (
        "01:03:38:28",
        [
            (
                "This 110-mile railway was built during the 1898 Klondike Gold Rush.",
                "这条铁路全长一百一十英里，修建于 1898 年的克朗代克淘金热时期。",
            ),
        ],
    ),
    (
        "01:03:48:12",
        [
            (
                "Back then, thousands of prospectors started here for Canada's Yukon goldfields.",
                "当年，成千上万的淘金者正是从这里踏上前往加拿大育空地区的寻金之路。",
            ),
        ],
    ),
    (
        "01:03:56:02",
        [
            (
                "In just over twenty miles, we will climb from sea level to nearly 3,000 feet.",
                "短短二十多英里，我们就将从海平面一路攀升到接近三千英尺的白隘口。",
            ),
        ],
    ),
    (
        "01:04:30:24",
        [
            (
                "Passengers begin stepping onto the open platforms between the cars.",
                "乘客们开始走到车厢连接处的露天平台。",
            ),
            (
                "They can enjoy better views and a more immersive experience.",
                "在那里可以欣赏更好的景色，获得更身临其境的体验。",
            ),
        ],
    ),
    (
        "01:05:00:00",
        [
            (
                "A reminder: if you stay on the open platform, wear warm clothing.",
                "特别提醒：如果打算长时间待在露天平台，一定要穿上保暖衣物。",
            ),
            (
                "After the morning downtown tour, I left my heavy coat in the cabin.",
                "上午游览完市中心后，我把厚外套留在了船舱里。",
            ),
            (
                "I did not expect to spend hours outside on the train, and regretted it later.",
                "因为没想到会在火车旅途中在户外待上几个小时，后来十分后悔。",
            ),
        ],
    ),
]


def inline_cell(reference: str, value: str, style: int) -> str:
    escaped = escape(value)
    return (
        f'<c r="{reference}" s="{style}" t="inlineStr">'
        f'<is><t xml:space="preserve">{escaped}</t></is></c>'
    )


def build_styles(styles: bytes) -> bytes:
    text = styles.decode("utf-8")
    text = text.replace('<cellXfs count="10">', '<cellXfs count="11">')
    wrapped = (
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="3" '
        'xfId="0" applyFont="1" applyBorder="1">'
        '<alignment vertical="top" wrapText="1"/></xf>'
    )
    text = text.replace("</cellXfs>", wrapped + "</cellXfs>")
    return text.encode("utf-8")


def build_sheet(sheet: bytes) -> bytes:
    text = sheet.decode("utf-8")
    text = text.replace('spans="2:4"', 'spans="2:5"')
    text = text.replace('max="5" width="16.6640625"', 'max="5" width="110"')
    text = text.replace(
        '<row r="2" spans="2:4"',
        '<row r="2" spans="2:5" ht="30"',
    )
    text = text.replace(
        '<row r="2" spans="2:5" ht="30" thickBot="1"',
        '<row r="2" spans="2:5" ht="30" thickBot="1"',
    )
    text = text.replace(
        '<row r="2" spans="2:5" ht="19" thickBot="1" x14ac:dyDescent="0.25"/>',
        '<row r="2" spans="2:5" ht="30" thickBot="1" x14ac:dyDescent="0.25">'
        + inline_cell("E2", "Bilingual Narration", 10)
        + "</row>",
    )

    def add_narration(match: re.Match[str]) -> str:
        row_number = int(match.group("row"))
        if not 3 <= row_number <= 30:
            return match.group(0)
        english, chinese = narration_pair(row_number - 3)
        cell = inline_cell("E" + str(row_number), english + "\n" + chinese, 10)
        opening = match.group("opening")
        inner = match.group("inner")
        opening = opening.replace(' spans="2:4"', ' spans="2:5"')
        if ' ht="' not in opening:
            opening = opening.replace("<row ", '<row ht="92" ', 1)
        return opening + inner + cell + "</row>"

    pattern = re.compile(
        r'(?P<opening><row\s+r="(?P<row>\d+)"[^>]*>)'
        r'(?P<inner>.*?)</row>',
        re.DOTALL,
    )
    text = pattern.sub(add_narration, text)
    return text.encode("utf-8")


def main() -> None:
    if len(NARRATIONS) != 28:
        raise RuntimeError("Narration count must match timing rows 3 through 30")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(SOURCE, "r") as source, zipfile.ZipFile(
        OUTPUT, "w", compression=zipfile.ZIP_DEFLATED
    ) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == "xl/worksheets/sheet1.xml":
                data = build_sheet(data)
            elif item.filename == "xl/styles.xml":
                data = build_styles(data)
            target.writestr(item, data)
    print(OUTPUT)


if __name__ == "__main__":
    main()
