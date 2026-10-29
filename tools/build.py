#!/usr/bin/env python3
"""Generates the alarifi.group pages (handheld design). Run from anywhere: python3 tools/build.py

Adding an app: add an entry to APPS with its slug, store link (None until it is live), texts and
images (assets/<slug>-art.jpg for the cartridge label, assets/<slug>-icon.jpg for the page header,
and assets/<slug>-screen.jpg if it will ever sit in the handheld), plus its support and privacy
pages. The first app sits in the handheld on the home page; every other app waits beside it as a
cartridge linking to its own page.
"""
import hashlib
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
EMAIL = 'nawaf@alarifi.group'


def asset_version(name):
    """Short content hash, so a changed stylesheet or script is never served from an old cache."""
    return hashlib.sha256((OUT / 'assets' / name).read_bytes()).hexdigest()[:10]


YEAR = 2026

HEAD_SCRIPT = (
    "(function(d){var l='en',t='';try{var m=/[?&]lang=(ar|en)(?:&|$)/.exec(location.search);"
    "if(m){l=m[1];localStorage.setItem('lang',l)}else if(localStorage.getItem('lang')==='ar'){l='ar'}"
    "t=localStorage.getItem('theme')||''}catch(e){}d.lang=l;d.dir=l==='ar'?'rtl':'ltr';"
    "if(l==='ar'){var a=d.getAttribute('data-title-ar');if(a)document.title=a}"
    "if(t==='light'||t==='dark')d.setAttribute('data-theme',t)})(document.documentElement)"
)

MAIL_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg>')


def t(en, ar, tag='span', attrs=''):
    """An English / Arabic pair; CSS shows the one matching <html lang>."""
    a = f' {attrs}' if attrs else ''
    return f'<{tag}{a} data-when="en">{en}</{tag}><{tag}{a} data-when="ar" lang="ar">{ar}</{tag}>'


def tt(pair, tag='span', attrs=''):
    return t(pair[0], pair[1], tag, attrs)


# ---------------------------------------------------------------- apps
APPS = [
    dict(
        slug='reddot',
        store='https://apps.apple.com/app/id6824105925',
        app_id='6824105925',
        name=('Red Dot', 'النقطة الحمراء'),
        subtitle=('Cat Laser Chase', 'مطاردة القط'),
        full=('Red Dot: Cat Laser Chase', 'النقطة الحمراء: مطاردة القط'),
        pitch=("You're the laser pointer. Basbousa the cat wants the dot. Keep him chasing, never let him catch it, and never let him get bored.",
               'أنت مؤشر الليزر. بسبوسة القط يبغى النقطة. خلّه يطارد، لا تخليه يمسكها، ولا تخليه يملّ.'),
        more=("Walk the whole neighbourhood! Lure cats into the pool, get help from Jasmine's broom and survive lights out. How far can you lead Basbousa?",
              'امشِ في الحي كله! ودّ القطط للمسبح، خلّ مكنسة ياسمين تساعدك، واصمد لما ينطفي النور. لين تقدر توصل مع بسبوسة؟'),
        facts=[
            (('Price', 'السعر'), ('Free, with in-app purchases', 'مجانية، مع مشتريات داخل التطبيق')),
            (('Device', 'الجهاز'), ('iPhone', 'آيفون')),
            (('Languages', 'اللغات'), ('English and Arabic', 'العربية والإنجليزية')),
            (('Age rating', 'التصنيف العمري'), ('9+', '9+')),
            (('Offline play', 'اللعب بدون إنترنت'), ('Yes', 'نعم')),
        ],
        screen_alt=('Red Dot gameplay: Basbousa the cat chasing the red laser dot across a rug',
                    'لقطة من النقطة الحمراء: بسبوسة القط يطارد نقطة الليزر الحمراء'),
        desc="You're the laser pointer. Basbousa the cat wants the dot. Red Dot: Cat Laser Chase for iPhone, by Alarifi Group.",
    ),
    dict(
        slug='ansure',
        store=None,  # not on the App Store yet; becomes 'https://apps.apple.com/app/id6802869721' once live
        app_id='6802869721',
        name=('Ansure', 'أنشر'),
        subtitle=('Scorekeeper', 'سجل الصكة'),
        full=('Ansure', 'أنشر: سجل الصكة'),
        pitch=('Ansure (أنشر) is a scorekeeping app for Baloot, Bint Al-Sabeet and Trix.',
               'أنشر تطبيق لتسجيل نتائج البلوت وبنت السبيت وتريكس.'),
        more=('There are no accounts, no sign-in and no servers of our own: your scores and settings stay on your device.',
              'لا حسابات، ولا تسجيل دخول، ولا خوادم خاصة بنا: نتائجك وإعداداتك تبقى على جهازك فقط.'),
        facts=[
            (('Price', 'السعر'), ('Free, with a one-time Remove Ads purchase', 'مجاني، مع شراء لمرة واحدة لإزالة الإعلانات')),
            (('Games', 'الألعاب'), ('Baloot, Bint Al-Sabeet and Trix', 'بلوت وبنت السبيت وتريكس')),
            (('Account', 'الحساب'), ('None, no sign-in', 'لا حسابات ولا تسجيل دخول')),
            (('Your scores', 'نتائجك'), ('Stay on your device', 'تبقى على جهازك')),
            (('Platform', 'المنصة'), ('iOS', 'iOS')),
        ],
        # the app's own colours, taken from its support and privacy pages
        cart_style='--plastic-hi:#34444d;--plastic:#1f2a31;--plastic-lo:#141b20;--label:#eef2f4',
        art_bg='#b8c8d0',
        band='#bf181b',
        desc='Ansure (أنشر) is a scorekeeping app for Baloot, Bint Al-Sabeet and Trix, by Alarifi Group.',
    ),
]


# ---------------------------------------------------------------- page shell
def page(*, path, root, title_en, title_ar, desc, canonical, body, extra_head='', preload=()):
    home = root or './'
    preloads = ''.join(f'<link rel="preload" href="{root}{p}" as="{"font" if p.endswith(".woff2") else "image"}"'
                       f'{" type=\"font/woff2\" crossorigin" if p.endswith(".woff2") else ""}>\n' for p in preload)
    html = f'''<!doctype html>
<html lang="en" dir="ltr" data-title-en="{title_en}" data-title-ar="{title_ar}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title_en}</title>
<script>{HEAD_SCRIPT}</script>
<meta name="description" content="{desc}">
{f'<link rel="canonical" href="{canonical}">' if canonical else ''}
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
<meta name="theme-color" content="#dedcd6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#211f1d" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Alarifi Group">
<meta property="og:title" content="{title_en}">
<meta property="og:description" content="{desc}">
{f'<meta property="og:url" content="{canonical}">' if canonical else ''}
<meta property="og:image" content="https://alarifi.group/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{extra_head}<link rel="preload" href="{root}assets/michroma-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/readex-latin.woff2" as="font" type="font/woff2" crossorigin>
{preloads}<link rel="stylesheet" href="{root}assets/site.css?v={asset_version('site.css')}">
<script src="{root}assets/site.js?v={asset_version('site.js')}" defer></script>
</head>
<body>
<header class="top wrap">
  <a class="mark" href="{home}"><span class="sr">Alarifi Group</span><span aria-hidden="true" dir="ltr">alarifi<span class="dot">.</span>group</span></a>
  <button class="key key-pill key-desk" type="button" data-toggle-lang><span class="key-face"><span class="key-text"><span data-when="en" lang="ar">العربية</span><span data-when="ar" lang="en">English</span></span></span></button>
</header>
{body}
<footer class="foot">
  <div class="foot-in wrap">
    <p>© {YEAR} {t('Alarifi Group', 'مجموعة العريفي')}</p>
    <ul class="foot-links">
{footer_links(root)}
    </ul>
    <div class="switch" role="group" aria-label="Theme">
      <button type="button" data-set-theme="auto" aria-pressed="true">{t('Auto', 'تلقائي')}</button>
      <button type="button" data-set-theme="light" aria-pressed="false">{t('Light', 'فاتح')}</button>
      <button type="button" data-set-theme="dark" aria-pressed="false">{t('Dark', 'داكن')}</button>
      <span class="switch-knob" aria-hidden="true"></span>
    </div>
  </div>
</footer>
</body>
</html>
'''
    html = '\n'.join(line for line in html.split('\n') if line.strip() != '') + '\n'
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print('wrote', out.relative_to(OUT), len(html.encode()), 'bytes')


def footer_links(root):
    items = []
    for app in APPS:
        items.append(f'<a href="{root}{app["slug"]}/">{tt(app["name"])}</a>')
    if len(APPS) == 1:
        slug = APPS[0]['slug']
        items.append(f'<a href="{root}{slug}/support">{t("Support", "الدعم")}</a>')
        items.append(f'<a href="{root}{slug}/privacy">{t("Privacy", "الخصوصية")}</a>')
    items.append(f'<a href="mailto:{EMAIL}"><bdi>{EMAIL}</bdi></a>')
    return '\n'.join(f'      <li>{i}</li>' for i in items)


# ---------------------------------------------------------------- objects
def has_asset(name):
    return (OUT / 'assets' / name).exists()


def cartridge(app, root, link=True):
    """An app as a cartridge. As a link it opens the app's page; otherwise it is a picture (aria-hidden)."""
    s = app['slug']
    style = f' style="{app["cart_style"]}"' if app.get('cart_style') else ''
    open_tag = f'<a class="cart" href="{root}{s}/"{style}>' if link else f'<div class="cart" aria-hidden="true"{style}>'
    close_tag = '</a>' if link else '</div>'
    if has_asset(f'{s}-art.jpg'):
        art = f'<img class="cart-art" src="{root}assets/{s}-art.jpg" width="480" height="480" alt="">'
    else:
        # no label art yet: the name in the other language, so the label never repeats itself
        art = (f'<span class="cart-art cart-art-type" style="background:{app.get("art_bg", "#d8cebd")}" aria-hidden="true">'
               f'<span data-when="en" lang="ar">{app["name"][1]}</span><span data-when="ar" lang="en">{app["name"][0]}</span></span>')
    return f'''{open_tag}
      <span class="cart-label">
        <span class="cart-name">{tt(app['name'])}</span>
        {art}
        <span class="cart-sub">{tt(app['subtitle'])}</span>
      </span>
    {close_tag}'''


def handheld(app, root):
    """The one-button handheld with an app's cartridge in the slot. app=None draws an empty slot."""
    if app is None:
        return f'''<div class="console empty" aria-hidden="true">
  <div class="dev">
    <div class="bezel"><span class="led"></span><div class="lcd"><p class="lcd-note">{t("No cartridge", "ما فيه شريط")}</p></div></div>
    <p class="brand"><span>Alarifi Group</span></p>
    <span class="key key-play"><span class="key-face"></span></span>
    <span class="grille"></span>
  </div>
</div>'''
    s = app['slug']
    alt_en, alt_ar = app['screen_alt']
    return f'''<div class="console">
  {cartridge(app, root)}
  <div class="dev">
    <div class="bezel">
      <span class="led" aria-hidden="true"></span>
      <div class="lcd"><img data-when="en" src="{root}assets/{s}-screen.jpg" width="600" height="845" alt="{alt_en}"><img data-when="ar" src="{root}assets/{s}-screen.jpg" width="600" height="845" alt="{alt_ar}"></div>
    </div>
    <p class="brand" aria-hidden="true"><span>Alarifi Group</span></p>
    <a class="key key-play" href="{app['store']}">
      <span class="key-face"><span class="key-text">{t('Play', 'العب')}</span>{t(f' {app["name"][0]} on the ', f' {app["name"][1]} من ', 'span', 'class="sr"')}<span class="key-sub">App Store</span></span>
    </a>
    <nav class="dev-keys" aria-label="{app['name'][0]}">
      <a class="key key-pill" href="{root}{s}/support"><span class="key-face"><span class="key-text">{t('Support', 'الدعم')}</span></span></a>
      <a class="key key-pill" href="{root}{s}/privacy"><span class="key-face"><span class="key-text">{t('Privacy', 'الخصوصية')}</span></span></a>
    </nav>
    <span class="grille" aria-hidden="true"></span>
  </div>
</div>'''


# ---------------------------------------------------------------- home
def build_home():
    first, others = APPS[0], APPS[1:]
    rack = ''
    if others:
        carts = '\n'.join(
            f'      <li>{cartridge(a, "")}'
            + ('' if a['store'] else t('Coming soon', 'قريبًا', 'span', 'class="rack-note"'))
            + '</li>' for a in others)
        rack = f'''
  <ul class="rack">
{carts}
  </ul>'''
    body = f'''<main class="home wrap">
  <section class="intro">
    <h1>{t('One game. One finger.', 'لعبة واحدة. إصبع واحد.')}</h1>
    {t("We make simple apps and games. Red Dot is the first: you're the laser pointer, and Basbousa the cat wants the dot.",
       'نصنع تطبيقات وألعابًا بسيطة. النقطة الحمراء أولها: أنت مؤشر الليزر، وبسبوسة القط يبغى النقطة.', 'p', 'class="lede"')}
    {t('The big button opens Red Dot on the App Store.', 'الزر الكبير يفتح النقطة الحمراء في App Store.', 'p', 'class="hint"')}
  </section>
  <div class="stage{' has-rack' if others else ''}">
{handheld(first, '')}{rack}
  </div>
</main>'''
    page(path='index.html', root='', title_en='Alarifi Group', title_ar='مجموعة العريفي',
         desc='Alarifi Group makes simple apps and games, including Red Dot: Cat Laser Chase for iPhone.',
         canonical='https://alarifi.group/', body=body,
         preload=(f'assets/{first["slug"]}-screen.jpg',))


# ---------------------------------------------------------------- app page
def build_app(app):
    s = app['slug']
    facts = '\n'.join(f'      <div><dt>{tt(k)}</dt><dd>{tt(v) if v[0] != v[1] else v[0]}</dd></div>'
                      for k, v in app['facts'])
    if app['store']:
        get_it = (f'<a class="key key-cream" href="{app["store"]}"><span class="key-face"><span class="key-text">'
                  f'{t("Get it on the App Store", "حمّلها من App Store")}</span></span></a>')
    else:
        get_it = f'<p class="app-soon">{t("Coming soon to the App Store", "قريبًا على App Store")}</p>'
    more = tt(app['more'], 'p', 'class="more"') if app.get('more') else ''
    body = f'''<main class="app-page wrap">
  <div class="app-object">
    {cartridge(app, '../', link=False)}
  </div>
  <section class="app-info">
    <h1>{tt(app['name'])}<span class="sr">: </span><span class="h1-sub">{tt(app['subtitle'])}</span></h1>
    {tt(app['pitch'], 'p', 'class="lede"')}
    {more}
    <div class="app-actions">
      {get_it}
    </div>
    <dl class="spec">
{facts}
    </dl>
    <nav class="app-links" aria-label="{app['name'][0]}">
      <a class="key key-pill key-desk" href="support"><span class="key-face"><span class="key-text">{t('Support', 'الدعم')}</span></span></a>
      <a class="key key-pill key-desk" href="privacy"><span class="key-face"><span class="key-text">{t('Privacy policy', 'سياسة الخصوصية')}</span></span></a>
    </nav>
  </section>
</main>'''
    page(path=f'{s}/index.html', root='../', title_en=app['full'][0], title_ar=app['full'][1],
         desc=app['desc'], canonical=f'https://alarifi.group/{s}/', body=body,
         extra_head=f'<meta name="apple-itunes-app" content="app-id={app["app_id"]}">\n' if app['store'] else '')


# ---------------------------------------------------------------- support / privacy
def sheet(app, current, content):
    sup = ' aria-current="page"' if current == 'support' else ''
    pri = ' aria-current="page"' if current == 'privacy' else ''
    band = f' style="--band:{app["band"]}"' if app.get('band') else ''
    icon = (f'<img src="../assets/{app["slug"]}-icon.jpg" width="48" height="48" alt="">'
            if has_asset(f'{app["slug"]}-icon.jpg') else '')
    return f'''<main class="doc-page wrap">
  <article class="sheet"{band}>
    <header class="sheet-head">
      <a class="sheet-app" href="./">
        {icon}
        <span><b>{tt(app['full'])}</b><small>{t('Alarifi Group', 'مجموعة العريفي')}</small></span>
      </a>
      <nav class="sheet-tabs" aria-label="{app['name'][0]}">
        <a class="key key-pill" href="support"{sup}><span class="key-face"><span class="key-text">{t('Support', 'الدعم')}</span></span></a>
        <a class="key key-pill" href="privacy"{pri}><span class="key-face"><span class="key-text">{t('Privacy policy', 'سياسة الخصوصية')}</span></span></a>
      </nav>
    </header>
    <div class="sheet-body">
{content}
    </div>
  </article>
</main>'''


mail = f'<a href="mailto:{EMAIL}"><bdi>{EMAIL}</bdi></a>'


def build_reddot_docs(app):
    support = f'''      <h1>{t('Support', 'الدعم')}</h1>
      {t(f"Questions, bugs, or a purchase that didn't arrive: email {mail} with your device model and iOS version. Replies within two working days.",
         f'عندك سؤال، أو واجهت خللًا، أو ما وصلك شيء اشتريته؟ راسلنا على {mail} مع طراز جهازك وإصدار iOS. نرد خلال يومي عمل.', 'p')}
      <ul class="qa">
        {t("<b>A purchase didn't show up.</b> Open the shop in the game and tap Restore purchases. If it still doesn't appear, email us with the receipt from Apple.",
           '<b>ما ظهر شيء اشتريته.</b> افتح المتجر في اللعبة واضغط «استعادة المشتريات». إذا ما ظهر بعدها، راسلنا مع إيصال الشراء من Apple.', 'li')}
        {t("<b>The cat feels too fast or too slow.</b> Tell us your best score and we'll look at the difficulty curve.",
           '<b>القط سريع جدًا أو بطيء جدًا.</b> أرسل لنا أفضل نتيجة لك وبنراجع مستوى الصعوبة.', 'li')}
        {t('<b>Refunds</b> are handled by Apple at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.',
           '<b>الاسترداد</b> تتولاه Apple عبر <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.', 'li')}
      </ul>
      <p><a class="key key-red" href="mailto:{EMAIL}?subject=Red%20Dot%20support"><span class="key-face">{MAIL_ICON}<span class="key-text">{t('Email support', 'راسل الدعم')}</span></span></a></p>'''
    page(path='reddot/support.html', root='../', title_en='Red Dot support', title_ar='دعم النقطة الحمراء',
         desc='Help with Red Dot: Cat Laser Chase. Email nawaf@alarifi.group.',
         canonical='https://alarifi.group/reddot/support', body=sheet(app, 'support', support))

    sections = [
        ('What stays on your device', 'ما يبقى على جهازك',
         "Your best score, fish treats, which cat you picked, its accessories and what you've bought are stored on your phone only. Deleting the app deletes them.",
         'أفضل نتيجة لك، والسمك الذي جمعته، والقط الذي اخترته وإكسسواراته، وما اشتريته، كلها محفوظة على جوالك فقط. حذف التطبيق يحذفها.'),
        ('Purchases', 'المشتريات',
         'Purchases are processed by Apple through the App Store, directly between your device and Apple. We never see your payment details, and we run no server of our own. Restore purchases asks Apple for what you already own.',
         'تعالج Apple المشتريات عبر App Store، مباشرة بين جهازك وApple. لا نرى بيانات الدفع الخاصة بك أبدًا، ولا نشغّل أي خادم خاص بنا. خيار «استعادة المشتريات» يطلب من Apple ما تملكه مسبقًا.'),
        ('Ads', 'الإعلانات',
         "The free version shows banner ads and optional reward videos from Google AdMob. We request non-personalized ads only, so the app does not ask to track you across other apps. AdMob may still receive your device's advertising identifier, IP address, approximate location and basic usage data to serve and measure ads, as described in <a href=\"https://policies.google.com/privacy\">Google's privacy policy</a>. Buying Remove ads turns banner ads off for good.",
         'تعرض النسخة المجانية إعلانات شريطية ومقاطع فيديو اختيارية بمكافأة من Google AdMob. نطلب إعلانات غير مخصصة فقط، لذلك لا يطلب التطبيق إذنك لتتبعك عبر التطبيقات الأخرى. ومع ذلك قد يتلقى AdMob معرّف الإعلانات الخاص بجهازك، وعنوان IP، وموقعك التقريبي، وبيانات استخدام أساسية لعرض الإعلانات وقياسها، كما توضح <a href="https://policies.google.com/privacy">سياسة الخصوصية لدى Google</a>. شراء «إزالة الإعلانات» يوقف الإعلانات الشريطية نهائيًا.'),
        ('Children', 'الأطفال',
         'The game is rated 9+, shows no personalized ads, and does not knowingly collect personal information from anyone, including children.',
         'تصنيف اللعبة 9+، ولا تعرض إعلانات مخصصة، ولا تجمع عن علم أي معلومات شخصية من أي شخص، بما في ذلك الأطفال.'),
        ('Changes', 'التغييرات',
         'If this policy changes, the new version appears on this page with a new effective date.',
         'إذا تغيّرت هذه السياسة، تظهر النسخة الجديدة في هذه الصفحة بتاريخ سريان جديد.'),
    ]
    sections_html = '\n'.join(f'      {t(he, ha, "h2")}\n      {t(pe, pa, "p")}' for he, ha, pe, pa in sections)
    privacy = f'''      <h1>{t('Privacy policy', 'سياسة الخصوصية')}</h1>
      {t('Effective 19 October 2026', 'سارية من 19 أكتوبر 2026', 'p', 'class="meta"')}
      {t('Red Dot does not ask you to create an account and does not collect your name, email, contacts or photos. There is nothing to sign up for.',
         'لا تطلب منك لعبة النقطة الحمراء إنشاء حساب، ولا تجمع اسمك أو بريدك الإلكتروني أو جهات اتصالك أو صورك. لا يوجد أي تسجيل.', 'p')}
{sections_html}
      {t('Contact', 'التواصل', 'h2')}
      <p>{mail}</p>'''
    page(path='reddot/privacy.html', root='../', title_en='Red Dot privacy policy', title_ar='سياسة الخصوصية: النقطة الحمراء',
         desc='Privacy policy for Red Dot: Cat Laser Chase by Alarifi Group.',
         canonical='https://alarifi.group/reddot/privacy', body=sheet(app, 'privacy', privacy))


# ---------------------------------------------------------------- Ansure support / privacy
# Arabic first, right to left, with the English section underneath, as Boss wrote them.
# Generated once from the files Boss sent on 29 Oct 2026 (text unchanged).
ANSURE_SUPPORT_AR = '''\
        <div class="doc-brand"><h1>أنشر</h1><span class="doc-latin" lang="en" dir="ltr">ANSURE</span></div>
        <p class="lead">سجل الصكة: حاسبة بلوت وبنت السبيت وتريكس، بلا حسابات وبلا إنترنت.</p>
        <h2>الدعم</h2>
        <p>واجهت مشكلة أو عندك اقتراح؟ راسلنا على <a href="mailto:nawaf@alarifi.group">nawaf@alarifi.group</a> واذكر نوع الجهاز وإصدار iOS، وإن أمكن صورة للشاشة.</p>
        <ul class="qa">
          <li><strong>الإعلانات لا تختفي بعد الشراء؟</strong> افتح الملف الشخصي واضغط "استعادة المشتريات" وأنت مسجّل بنفس Apple ID.</li>
          <li><strong>تنبيه أوقات الصلاة لا يظهر؟</strong> يحتاج إذن الموقع (أثناء الاستخدام) من إعدادات iOS، ويظهر فقط والتطبيق مفتوح.</li>
          <li><strong>ضاعت نتائجي؟</strong> النتائج محفوظة على الجهاز نفسه فقط؛ حذف التطبيق يحذفها معه.</li>
        </ul>
        <h2>الخصوصية</h2>
        <p>كل شيء على جهازك. التفاصيل في <a href="privacy">سياسة الخصوصية</a>.</p>
'''

ANSURE_SUPPORT_EN = '''\
        <h2>Support (English)</h2>
        <p>Questions or problems? Email <a href="mailto:nawaf@alarifi.group">nawaf@alarifi.group</a> with your device model and iOS version. Privacy policy: <a href="privacy">Privacy policy</a>.</p>
'''

ANSURE_PRIVACY_AR = '''\
        <div class="doc-brand"><h1>أنشر</h1><span class="doc-latin" lang="en" dir="ltr">ANSURE</span></div>
        <p class="meta">سياسة الخصوصية · آخر تحديث: 26 أكتوبر 2026</p>
        <h2>باختصار</h2>
        <p>أنشر تطبيق لتسجيل نتائج البلوت وبنت السبيت وتريكس. لا حسابات، ولا تسجيل دخول، ولا خوادم خاصة بنا: نتائجك وإعداداتك تبقى على جهازك فقط. الشيء الوحيد الذي يتصل بالإنترنت هو الإعلانات في النسخة المجانية.</p>

        <h2>ما الذي يبقى على جهازك</h2>
        <ul class="doc-list">
          <li><strong>النتائج والسجل والإحصائيات:</strong> تُحفظ في ذاكرة التطبيق على جهازك، ولا تُرسل إلى أي جهة.</li>
          <li><strong>الموقع (اختياري):</strong> إن فعّلت "تنبيه أوقات الصلاة" يطلب التطبيق إذن الموقع لحساب أوقات الصلاة على الجهاز نفسه. الموقع لا يغادر الجهاز، ويمكنك تعطيل الميزة أو سحب الإذن في أي وقت من إعدادات iOS.</li>
          <li><strong>الكاميرا والصور (اختياري):</strong> "صور مع الأكة" تلتقط صورتك بعد الفوز وتحفظها في ألبوم الصور لديك. الصور لا تُرفع إلى أي مكان.</li>
        </ul>

        <h2>الإعلانات</h2>
        <p>تعرض النسخة المجانية إعلانات عبر Google AdMob. قد تجمع Google عند عرض الإعلان معرّف الإعلان الخاص بالجهاز (إن سمحت بالتتبع)، وعنوان IP، ومعلومات عن الجهاز والإعلانات التي شاهدتها، وفق <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">سياسة خصوصية Google</a>. عند أول تشغيل يسألك iOS إن كنت تسمح بالتتبع؛ إن رفضت تُعرض إعلانات غير مخصصة. يمكنك تغيير ذلك لاحقاً من إعدادات iOS › الخصوصية والأمان › التتبع.</p>

        <h2>إزالة الإعلانات</h2>
        <p>شراء "إزالة الإعلانات" يتم عبر Apple داخل التطبيق. لا نستلم أي بيانات دفع؛ يُحفظ على جهازك فقط أن الشراء تم، ويمكن استعادته على أي جهاز بنفس Apple ID من زر "استعادة المشتريات".</p>

        <h2>ما لا نفعله</h2>
        <ul class="doc-list">
          <li>لا نجمع أسماء اللاعبين أو النتائج أو أي بيانات شخصية.</li>
          <li>لا نستخدم أدوات تحليلات أو تتبّع من طرفنا.</li>
          <li>لا نبيع أي بيانات، ولا نشاركها مع أي جهة عدا ما تجمعه Google لعرض الإعلانات كما هو موضح أعلاه.</li>
        </ul>

        <h2>الأطفال</h2>
        <p>التطبيق غير موجّه للأطفال دون 13 عاماً، ولا نجمع عن قصد أي بيانات منهم.</p>

        <h2>التغييرات</h2>
        <p>إن تغيّرت هذه السياسة سننشر النسخة الجديدة هنا مع تاريخ التحديث.</p>

        <h2>تواصل معنا</h2>
        <p>لأي سؤال عن الخصوصية: <a href="mailto:nawaf@alarifi.group">nawaf@alarifi.group</a></p>
'''

ANSURE_PRIVACY_EN = '''\
        <h2>Privacy Policy (English)</h2>
        <p class="meta">Last updated: October 26, 2026</p>
        <p>Ansure (أنشر) is a scorekeeping app for Baloot, Bint Al-Sabeet and Trix. There are no accounts, no sign-in and no servers of our own: your scores and settings stay on your device. The only thing that talks to the internet is advertising in the free version.</p>

        <h2>What stays on your device</h2>
        <ul class="doc-list">
          <li><strong>Scores, history and statistics</strong> are stored in the app's local storage and are never sent anywhere.</li>
          <li><strong>Location (optional):</strong> if you turn on prayer-time alerts, the app asks for location permission to compute prayer times on the device itself. Your location never leaves the device; you can turn the feature off or revoke the permission in iOS Settings at any time.</li>
          <li><strong>Camera and Photos (optional):</strong> the "ace photo" feature takes a picture after a win and saves it to your Photos library. Photos are never uploaded.</li>
        </ul>

        <h2>Advertising</h2>
        <p>The free version shows ads through Google AdMob. When an ad is shown, Google may collect your device's advertising identifier (if you allow tracking), IP address, device information and ad-interaction data, as described in the <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a>. On first launch iOS asks whether you allow tracking; if you decline, non-personalized ads are shown. You can change this later in iOS Settings › Privacy &amp; Security › Tracking.</p>

        <h2>Remove Ads purchase</h2>
        <p>"Remove Ads" is a one-time in-app purchase handled by Apple. We never receive payment details; only the fact that the purchase was made is stored on your device, and it can be restored on any device signed in with the same Apple ID using "Restore Purchases".</p>

        <h2>What we don't do</h2>
        <ul class="doc-list">
          <li>We don't collect player names, scores or any personal data.</li>
          <li>We don't use analytics or tracking tools of our own.</li>
          <li>We don't sell data and don't share it with anyone, apart from what Google collects to serve ads as described above.</li>
        </ul>

        <h2>Children</h2>
        <p>The app is not directed at children under 13 and we do not knowingly collect any data from them.</p>

        <h2>Changes</h2>
        <p>If this policy changes, the new version will be published here with its update date.</p>

        <h2>Contact</h2>
        <p>Privacy questions: <a href="mailto:nawaf@alarifi.group">nawaf@alarifi.group</a></p>
'''



def bilingual(ar, en):
    # keep "Apple ID" on one line inside right-to-left text (markup only, the words are unchanged)
    ar = ar.replace('Apple ID', '<span class="nobr">Apple ID</span>')
    return (f'      <section class="doc-part" lang="ar" dir="rtl">\n{ar}      </section>\n'
            f'      <section class="doc-part" lang="en" dir="ltr">\n{en}      </section>')


def build_ansure_docs(app):
    page(path='ansure/support.html', root='../', title_en='Ansure support', title_ar='الدعم | أنشر',
         desc='Support for Ansure (أنشر), the scorekeeper for Baloot, Bint Al-Sabeet and Trix. Email nawaf@alarifi.group.',
         canonical='https://alarifi.group/ansure/support',
         body=sheet(app, 'support', bilingual(ANSURE_SUPPORT_AR, ANSURE_SUPPORT_EN)))
    page(path='ansure/privacy.html', root='../', title_en='Ansure privacy policy', title_ar='سياسة الخصوصية | أنشر',
         desc='Privacy policy for Ansure (أنشر) by Alarifi Group.',
         canonical='https://alarifi.group/ansure/privacy',
         body=sheet(app, 'privacy', bilingual(ANSURE_PRIVACY_AR, ANSURE_PRIVACY_EN)))


# ---------------------------------------------------------------- 404
def build_404():
    body = f'''<main class="lost wrap">
  <div class="stage">
{handheld(None, '/')}
  </div>
  <section>
    <h1>{t('Nothing in this slot.', 'ما فيه شي هنا.')}</h1>
    {t("This page doesn't exist.", 'هذه الصفحة غير موجودة.', 'p')}
    <a class="key key-cream" href="/"><span class="key-face"><span class="key-text">{t('Go to the home page', 'الذهاب إلى الصفحة الرئيسية')}</span></span></a>
  </section>
</main>'''
    page(path='404.html', root='/', title_en='Page not found', title_ar='الصفحة غير موجودة',
         desc='This page does not exist on alarifi.group.', canonical='', body=body)


build_home()
for a in APPS:
    build_app(a)
BY_SLUG = {a['slug']: a for a in APPS}
build_reddot_docs(BY_SLUG['reddot'])
build_ansure_docs(BY_SLUG['ansure'])
build_404()
