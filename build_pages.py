#!/usr/bin/env python3
"""Session House — template v2 generator (websites lane, t_737649d7, 2026-11-22).
Copy discipline: only facts verified on the card + its cited sources
(Dorchester Reporter 2026-09-24, What Now Boston feature, Boston.com 2026-11-03
roundup, the shop's own FB intro + IG bio, Nominatim geocode of 782 Adams St).
No phone, no hours, no prices, no menu items — none published; unknown = omitted.
Output: public/*.html + sitemap.xml + robots.txt. Run before `railway up`."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")
ORIGIN = "https://session-house-boston-demo.up.railway.app"
BUILT = "2026-11-22"

NAP_LINE = "782 Adams St, Adams Village, Dorchester, Boston, MA 02124"
ADDRESS_HTML = "782 Adams St<br>Adams Village, Dorchester<br>Boston, MA 02124"
MAP_Q = "782+Adams+St,+Boston,+MA+02124"
EMAIL = "info@sessionhouseboston.com"
FB = "https://www.facebook.com/profile.php?id=61595767970369"
IG = "https://www.instagram.com/sessionhouseboston/"
DOTNEWS = "https://www.dotnews.com/2026/09/24/irish-pub-that-plans-live-irish-music-approved-in-adams-village/"
WHATCHNOW = "https://whatnow.com/boston/restaurants/session-house-to-bring-irish-music-elevated-pub-fare-and-soulful-spirit-to-dorchesters-adams-village/"
BOSTONCOM = "https://www.boston.com/food/restaurants/2026/11/03/5-restaurants-we-cant-wait-to-try-in-november-2026/"

LAT, LON = 42.283086, -71.055643

# Side-struck wire harp line-mark (pub identity; stroke inherits color)
HARP = ('<svg class="harp" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path d="M4.5 18.5C4.5 8.8 9.2 5 17.7 5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
        '<path d="M4.5 18.5h13.2M17.7 5v13.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
        '<path d="M8.4 18.5V6.2M11.6 18.5V5.35M14.8 18.5V5.05" fill="none" stroke="currentColor" stroke-width="0.9"/></svg>')

# Soundwave arcs radiging from a point (the one-mic motif; in-flow decor only)
WAVE = ('<svg class="wave" viewBox="0 0 140 44" aria-hidden="true" focusable="false">'
        '<circle cx="14" cy="22" r="2.6" fill="currentColor"/>'
        '<path d="M24 10a17 17 0 0 1 0 24M34 4a27 27 0 0 1 0 36M44 -2a37 37 0 0 1 0 48" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" opacity=".55"/>'
        '<path d="M126 10a17 17 0 0 0 0 24M116 4a27 27 0 0 0 0 36M106 -2a37 37 0 0 0 0 48" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" opacity=".55"/></svg>')

HEADER = (f'<a class="skip" href="#main">Skip to content</a>\n'
          '<header class="site"><div class="wrap hdr">'
          f'<a class="wm" href="/">{HARP}<span>Session House</span></a>'
          '<nav aria-label="Site"><ul>'
          '<li><a href="/live-music">Live Music</a></li>'
          '<li><a href="/irish-trad-music-dorchester">Trad Sessions</a></li>'
          '<li><a href="/pub-grub-adams-village">Pub Grub</a></li>'
          '<li><a href="/story">Our Story</a></li>'
          '<li><a href="/visit">Visit</a></li>'
          '</ul></nav>'
          '<a class="btn sm" href="/contact">Send a note</a>'
          '</div></header>')

FOOTER = ('<footer class="site"><div class="wrap foottop">'
          f'<div><p class="fbrand">{HARP}<span>Session House</span></p>'
          '<p class="ftag">Irish sessions &middot; elevated pub grub &middot; whiskey, cocktails, wine &amp; beer</p>'
          '<div class="fnaps"><p class="ftown">Find us</p>'
          f'<address class="addr">{ADDRESS_HTML}</address>'
          f'<p class="fhrs">Opening mid-November 2026 &mdash; hours land when the first session does</p>'
          f'<p>Questions: <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="/contact">contact form</a></p></div></div>'
          '<nav aria-label="Footer"><ul>'
          '<li><a href="/live-music">Live music</a></li>'
          '<li><a href="/irish-trad-music-dorchester">Trad sessions</a></li>'
          '<li><a href="/pub-grub-adams-village">Pub grub &amp; the board</a></li>'
          '<li><a href="/story">Our story</a></li>'
          '<li><a href="/visit">Visit</a></li>'
          '<li><a href="/contact">Contact</a></li>'
          '<li><a href="/privacy">Privacy</a></li>'
          '</ul></nav>'
          '<p class="fpress">In the news:<br>'
          f'<a href="{DOTNEWS}" rel="noopener">Dorchester Reporter: licensing approval</a><br>'
          f'<a href="{WHATCHNOW}" rel="noopener">What Now Boston: the SOUL CE&Oacute;L feature</a></p>'
          '</div><div class="wrap"><p class="footline">'
          f'&copy; 2026 Session House &middot; Irish pub &amp; live music venue &middot; {NAP_LINE}'
          '</p></div></footer>')

def head(title, desc, path, og=True):
    canonical = ORIGIN + ("" if path == "/" else path)
    ogblock = ""
    if og:
        ogblock = (f'<meta property="og:type" content="website">\n'
                   '<meta property="og:site_name" content="Session House">\n' +
                   f'<meta property="og:title" content="{title}">\n'
                   f'<meta property="og:description" content="{desc}">\n'
                   f'<meta property="og:url" content="{canonical}">\n'
                   f'<meta property="og:image" content="{ORIGIN}/og.png">\n'
                   '<meta name="twitter:card" content="summary_large_image">\n'
                   f'<meta name="twitter:title" content="{title}">\n'
                   f'<meta name="twitter:description" content="{desc}">\n'
                   f'<meta name="twitter:image" content="{ORIGIN}/og.png">\n')
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<!-- BUILT-{BUILT} -->\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n'
            f'<meta name="description" content="{desc}">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            f'<link rel="canonical" href="{canonical}">\n'
            + ogblock +
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="stylesheet" href="/style.css">\n</head>')

def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>\n'

def page(title, desc, path, body, ldobj=None, og=True):
    return (head(title, desc, path, og) + (ldobj or "") + '<body>\n' + HEADER +
            '\n<main id="main">\n' + body + '\n</main>\n' + FOOTER + '\n</body>\n</html>\n')

def faq(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in items]}

def crumb(steps):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + p}
        for i, (n, p) in enumerate(steps)]}

# ---------------------------------------------------------------- HOME
PUB_ND = {
    "@type": "BarOrPub", "@id": ORIGIN + "/#pub", "name": "Session House",
    "description": ("New Irish pub and live-music venue in Adams Village, Dorchester, from Esteemed Hospitality, LLC. "
                    "Traditional Irish sessions and contemporary performances, elevated pub grub drawn from Irish and "
                    "New England traditions, and a seasonal beverage program. Opening mid-November 2026 at 782 Adams Street."),
    "url": ORIGIN + "/", "image": ORIGIN + "/og.png",
    "email": EMAIL,
    "servesCuisine": "Irish pub grub",
    "address": {"@type": "PostalAddress", "streetAddress": "782 Adams St",
                "addressLocality": "Boston", "addressRegion": "MA",
                "postalCode": "02124", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
    "sameAs": [FB, IG]}
# no telephone, no openingHours, no priceRange — none published yet; omit, never fake

HOME_LDS = {"@graph": [
    {"@type": "WebSite", "@id": ORIGIN + "/#website", "name": "Session House", "url": ORIGIN + "/"},
    {"@type": "WebPage", "@id": ORIGIN + "/#webpage",
     "name": "Session House — Irish Pub & Live Music, Adams Village, Boston MA",
     "url": ORIGIN + "/", "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#pub"}},
    PUB_ND,
    faq([
        ("When does Session House open?",
         "Mid-November 2026 — Boston.com's November openings roundup lists the pub as opening mid-November at 782 Adams St. First session dates and opening hours land on Facebook and Instagram as the opening nears."),
        ("Where is Session House?",
         "At 782 Adams Street in Adams Village, Dorchester, Boston — the former Scobie's Cafe & Bar space."),
        ("What kind of music will you have?",
         "Live traditional Irish sessions plus contemporary performances — five to seven nights a week on the plans — with much of it played by local musicians."),
        ("Is it family-friendly?",
         "Yes — managing partner Teresa Murphy told the licensing board the pub is planned as a family-friendly place to bring kids to see live music."),
        ("What's on the menu?",
         "Elevated pub grub drawn from both Irish and New England traditions. The dish list and prices live at the door, not on this site."),
        ("Is there a website I can watch for opening news?",
         "This page carries what's known now. Opening-night dates land on the pub's Facebook and Instagram pages first.")])] }

HOME = page(
    "Session House — Irish Pub &amp; Live Music, Adams Village, Boston MA",
    "Session House opens mid-November 2026 at 782 Adams St, Adams Village, Dorchester: trad Irish sessions five to seven nights a week, elevated pub grub, and a whiskey, cocktail, wine and beer board.",
    "/",
    f'''
<section class="band ink hero"><div class="wrap center">
  {WAVE}
  <p class="eyebrow">Opening mid-November 2026 &middot; Adams Village, Dorchester</p>
  <h1 class="big">Session <em>House</em></h1>
  <p class="lede">An Irish pub built around one microphone in the middle of the room &mdash;
  trad sessions, contemporary sets, elevated pub grub, and a board that turns with the season.
  <strong class="tag">Come for the music. Stay for the soul.</strong></p>
  <div class="ctarow"><a class="btn gold" href="/live-music">See the music program</a>
  <a class="btn ghost" href="/contact">Send a note</a></div>
</div></section>

<section class="band paper"><div class="wrap narrow center">
  <p class="eyebrow">How the room works</p>
  <h2 class="sec">One microphone. Ten musicians. No stage.</h2>
  <p class="secsub">Frank Delaney told the Dorchester Reporter what the room is built for:
  &ldquo;It&rsquo;s basically what the Burren does in Somerville &mdash; where there could be
  one to five, ten musicians, but one general microphone in the middle to pick up&hellip;
  But it&rsquo;s very civilized. We&rsquo;re not talking about DJs and big bands.&rdquo;</p>
  <div class="steps">
    <div class="step"><p class="num">01</p><h3 class="stept">Bring the instrument</h3>
      <p class="stepd">Players from around the neighborhood gather with their instruments.
      &ldquo;How many Irish musicians live in this area&rdquo; &mdash; Delaney counted them
      before he built the room, and they&rsquo;ve been reaching out to play.</p></div>
    <div class="step"><p class="num">02</p><h3 class="stept">Or just bring your ears</h3>
      <p class="stepd">Managing partner Teresa Murphy wants a place families can bring kids
      to hear live music: trad sessions that carry the room without drowning it.</p></div>
    <div class="step"><p class="num">03</p><h3 class="stept">Trad plus contemporary</h3>
      <p class="stepd">Traditional Irish sessions five to seven nights a week on the plans,
      with contemporary performances alongside &mdash; much of it by local players.</p></div>
  </div>
</div></section>

<section class="band cream"><div class="wrap">
  <p class="eyebrow">Inside the plan &middot; three things to know now</p>
  <h2 class="sec">What the pub is being built for</h2>
  <p class="secsub">Every claim on this page comes from the pub&rsquo;s licensing filings, its
  own pages, and the press that covered them. Nothing is guessed.</p>
  <div class="tickets">
    <a class="ticket t-green" href="/irish-trad-music-dorchester"><p class="tkick">The sessions</p>
      <h3 class="tname">Trad &amp; seisi&uacute;n</h3>
      <p class="tper">A session is musicians playing together &mdash; the communal tradition
      the pub is named for. One shared mic, tunes by ear, everyone in the room.</p>
      <p class="tmore">Trad sessions page &rarr;</p></a>
    <a class="ticket t-gold" href="/pub-grub-adams-village"><p class="tkick">The kitchen &amp; bar</p>
      <h3 class="tname">Pub grub,<br>elevated</h3>
      <p class="tper">Dishes drawn from Irish and New England traditions, and a seasonal
      board of whiskey, cocktails, wine and thoughtfully chosen beers.</p>
      <p class="tmore">Pub grub &amp; drinks &rarr;</p></a>
    <a class="ticket t-cream" href="/story"><p class="tkick">The people</p>
      <h3 class="tname">Coming home to Adams Street</h3>
      <p class="tper">Frank Delaney &mdash; Broadside Tavern, The Merchant &mdash; and Teresa
      Murphy, taking over the old Scobie&rsquo;s space where Delaney&rsquo;s first apartment stood.</p>
      <p class="tmore">Our story &rarr;</p></a>
  </div>
</div></section>

<section class="band ink"><div class="wrap split">
  <div>
    <p class="eyebrow">SOUL CE&Oacute;L &middot; soul music</p>
    <h2 class="sec light">Music is the purpose. The building is the part after it.</h2>
    <p class="bodycopy">SOUL CE&Oacute;L &mdash; &ldquo;soul music&rdquo; &mdash; is the pub&rsquo;s
    own name for its theme: the connection between Irish music and the communities that keep
    those traditions alive. Adams Village is one of those communities, and the room is being
    finished in rich dark tones with warm gold accents and traditional musical imagery, so it
    reads like a place that&rsquo;s always been there.</p>
    <p class="quote">&ldquo;Great music, great food, a great pint, a beautiful room &mdash; and
    most importantly, a sense that everybody is welcome at the table.&rdquo;<span class="attrib">The founding team, via What Now Boston</span></p>
    <div class="ctarow"><a class="btn gold" href="/live-music">The music program</a></div>
  </div>
  <aside class="infocard">
    <h3 class="infh">Opening card</h3>
    <dl class="factlist">
      <div><dt>Opening</dt><dd>Mid-November 2026<br><span class="fine">Nights &amp; hours land with the first session dates</span></dd></div>
      <div><dt>Where</dt><dd>782 Adams St<br>Adams Village, Dorchester<br>Boston, MA 02124</dd></div>
      <div><dt>On the plan</dt><dd>Trad sessions 5&ndash;7 nights<br>contemporary sets<br>whiskey &middot; cocktails &middot; wine &middot; beer</dd></div>
      <div><dt>Run by</dt><dd>Esteemed Hospitality, LLC<br>Frank Delaney &amp; Teresa Murphy</dd></div>
    </dl>
    <p class="bigm"><a href="/visit">Directions &amp; opening info</a></p>
  </aside>
</div></section>

<section class="band cream"><div class="wrap narrow">
  <p class="eyebrow">New here?</p>
  <h2 class="sec">The press found it first</h2>
  <p class="bodycopy">The Boston Licensing Board approved Session House in September 2026;
  Boston.com put it on its November openings list (&ldquo;Opens: Mid-November&rdquo;); What Now
  Boston profiled the plan, the name, and the SOUL CE&Oacute;L theme in full.</p>
  <p class="note">Read them: <a href="{DOTNEWS}" rel="noopener">Dorchester Reporter</a> &middot;
  <a href="{BOSTONCOM}" rel="noopener">Boston.com</a> &middot;
  <a href="{WHATCHNOW}" rel="noopener">What Now Boston</a>. Watch for the first session:
  <a href="{IG}" rel="noopener">Instagram</a> &middot; <a href="{FB}" rel="noopener">Facebook</a>.</p>
  <div class="ctarow"><a class="btn" href="/contact">Ask us something</a>
  <a class="btn ghost" href="/live-music">The music program</a></div>
</div></section>
''',
    ld(HOME_LDS))

# ---------------------------------------------------------------- LIVE MUSIC HUB
MUSIC_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Live Music at Session House — Adams Village, Boston",
     "url": ORIGIN + "/live-music", "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#pub"}},
    crumb([("Home", "/"), ("Live Music", "/live-music")]),
    {"@type": "Service", "name": "Live traditional Irish sessions and contemporary performances",
     "serviceType": "Live music programming", "areaServed": {"@type": "City", "name": "Boston"},
     "provider": {"@id": ORIGIN + "/#pub"}},
    faq([
        ("When does the music start?",
         "Mid-November 2026 is the opening window. Session nights and start times post to the pub's Facebook and Instagram pages as the opening nears."),
        ("What kind of music, exactly?",
         "Traditional Irish sessions plus contemporary performances — five to seven nights a week on the plans, with much of it played by local musicians."),
        ("Do I need an instrument to enjoy it?",
         "No. Players gather around the room's one shared microphone; the rest of the pub listens. You can come with nothing but ears."),
        ("Can I bring kids?",
         "Yes. Managing partner Teresa Murphy told the Boston Licensing Board the pub is planned as a family-friendly restaurant where you can bring kids to see live music."),
        ("Is there a cover charge?",
         "Nothing is published about cover. Anything the door charges will live at the door and on the pub's social pages, not on this site.")])] }

MUSIC = page(
    "Live Music at Session House — Irish Sessions &amp; Contemporary, Adams Village Boston",
    "SOUL CEÓL: trad Irish sessions and contemporary performances five to seven nights a week at Session House, 782 Adams St, Adams Village, Boston — built around one microphone in the middle.",
    "/live-music",
    f'''
<section class="band ink herol"><div class="wrap">
  <p class="eyebrow">SOUL CE&Oacute;L &middot; the music program</p>
  <h1>One mic in the middle of the room</h1>
  <p class="lede">Live music here isn&rsquo;t a nightly event layered onto a bar &mdash; it&rsquo;s
  what the building was chosen for. Traditional Irish sessions plus contemporary performances,
  five to seven nights a week on the plans, much of it played by musicians who live in this
  neighborhood.</p>
</div></section>

<section class="band paper"><div class="wrap plate">
  <h2 class="pname bigname">What a &ldquo;session&rdquo; is</h2>
  <p class="tagline">The tradition the pub is named for</p>
  <p class="bodycopy">A session is the communal tradition of musicians gathering to play
  together &mdash; tunes carried by ear, players trading the lead, the circle deciding what
  plays next. The pub calls itself Session House for that: &ldquo;session&rdquo; for the music,
  &ldquo;house&rdquo; for the warmth of a neighborhood home. The Irish word for the gathering
  is <em>seisi&uacute;n</em>, and the Dorchester Reporter quoted the team&rsquo;s plan in exactly
  that word: Irish pub grub &ldquo;accompanied by Irish seisi&uacute;n music &mdash; much of it
  by local musicians.&rdquo;</p>
</div></section>

<section class="band cream"><div class="wrap plate">
  <h2 class="pname bigname">The Burren model, in Adams Village</h2>
  <p class="tagline">Civilized by design</p>
  <p class="bodycopy">&ldquo;It&rsquo;s basically what the Burren does in Somerville,&rdquo;
  Frank Delaney told the licensing board, &ldquo;where there could be one to five, ten
  musicians, but one general microphone in the middle to pick up&hellip; But it&rsquo;s very
  civilized. We&rsquo;re not talking about DJs and big bands.&rdquo; One shared microphone
  keeps the music at conversation level: you can hear the set <em>and</em> the table next to
  you.</p>
  <div class="ctarow"><a class="btn" href="/irish-trad-music-dorchester">Trad sessions in depth</a>
  <a class="btn ghost" href="/pub-grub-adams-village">What&rsquo;s eating and pouring</a></div>
</div></section>

<section class="band ink"><div class="wrap split">
  <div>
    <p class="eyebrow">For families &middot; for players</p>
    <h2 class="sec light">Bring the kids. Bring the fiddle.</h2>
    <p class="quote">&ldquo;We&rsquo;re really interested in having like a family-friendly
    restaurant that you can bring kids to see&hellip; live music. We&rsquo;ll have traditional
    Irish music and some contemporary as well.&rdquo;<span class="attrib">Teresa Murphy, managing partner, to the Boston Licensing Board</span></p>
    <p class="bodycopy">And for players: Delaney pointed the board at the neighborhood itself
    &mdash; &ldquo;I&rsquo;m sure living in the area you&rsquo;re aware of how many musicians,
    Irish musicians live in this area, and how many musicians have reached out to us looking to
    play.&rdquo; The room is being built for exactly that bench.</p>
  </div>
  <aside class="infocard">
    <h3 class="infh">The music, plainly</h3>
    <dl class="factlist">
      <div><dt>Trad</dt><dd>Irish sessions &middot; seisi&uacute;n, five to seven nights on the plans</dd></div>
      <div><dt>Contemporary</dt><dd>Sets alongside the trad program</dd></div>
      <div><dt>The rig</dt><dd>One general microphone, mid-room</dd></div>
      <div><dt>The level</dt><dd>Conversation-friendly &mdash; no DJs, no big bands</dd></div>
    </dl>
    <p class="bigm"><a href="/contact">Play with us? Leave a note</a></p>
  </aside>
</div></section>
''',
    ld(MUSIC_LDS))

# ---------------------------------------------------------------- TRAD DETAIL
TRAD_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Traditional Irish Sessions & Seisiún — Session House, Dorchester Boston",
     "url": ORIGIN + "/irish-trad-music-dorchester", "isPartOf": {"@id": ORIGIN + "/#website"}},
    crumb([("Home", "/"), ("Live Music", "/live-music"), ("Trad Sessions", "/irish-trad-music-dorchester")]),
    {"@type": "Service", "name": "Traditional Irish music sessions",
     "serviceType": "Live traditional Irish music",
     "areaServed": [{"@type": "City", "name": "Boston"}, {"@type": "AdministrativeArea", "name": "Dorchester"}],
     "provider": {"@id": ORIGIN + "/#pub"}},
    faq([
        ("What is a seisiún?",
         "The Irish-language word for a music session — musicians gathering to play together, trad tunes carried by ear. The Dorchester Reporter used the word in its Session House licensing-approval report."),
        ("Which nights are trad?",
         "The plans carry traditional sessions five to seven nights a week. Named nights and start times post to Facebook and Instagram when the opening window arrives in mid-November 2026."),
        ("Do I have to play to be included?",
         "No — listeners are half of every good session. The circle plays; the room drinks it in."),
        ("Will my table still be able to talk?",
         "Yes. The room runs on one general microphone and keeps things conversation-level: 'very civilized,' in Frank Delaney's words — no DJs, no big bands."),
        ("Where is it?",
         "782 Adams St, Adams Village, Dorchester — Boston, MA 02124. Opening mid-November 2026.")])] }

TRAD = page(
    "Traditional Irish Sessions &amp; Seisi&uacute;n — Session House, Dorchester Boston MA",
    "Trad Irish sessions at Session House: the Burren-style one-mic model, local musicians, conversation-level sound, five to seven nights a week on the plans. Adams Village, Dorchester.",
    "/irish-trad-music-dorchester",
    '''
<section class="band forest herol"><div class="wrap">
  <p class="eyebrow">Trad &middot; Dorchester</p>
  <h1>The seisi&uacute;n, near you</h1>
  <p class="lede">There is a bench of Irish musicians around Adams Village &mdash; Delaney
  counted them when he was still testifying for the room. Session House is the pub being built
  for them: sessions five to seven nights a week on the plans, tunes by ear, one microphone
  doing the work.</p>
</div></section>

<section class="band paper"><div class="wrap plates2">
  <div class="platecard">
    <h2 class="pname">How a session runs</h2>
    <p class="tagline">Circles, not stages</p>
    <p class="bodycopy">Players gather close so they can hear each other &mdash; a fiddle, a
    box, a flute, a bodhr&aacute;n, somebody&rsquo;s daughter on vocals. Someone starts a
    set, the circle follows, and the next player leads the one after that. Nobody needs
    a soundcheck. That&rsquo;s the tradition, and it&rsquo;s why the pub named itself after it.</p>
  </div>
  <div class="platecard">
    <h2 class="pname">How the room holds it</h2>
    <p class="tagline">One mic. Conversation level.</p>
    <p class="bodycopy">&ldquo;One to five, ten musicians, but one general microphone in the
    middle to pick up&hellip; very civilized&rdquo; &mdash; the room plan as Delaney described
    it to the board. The sound lifts off the circle, not off a PA stack, so the pint-and-talk
    layer of the night survives it.</p>
  </div>
</div></section>

<section class="band cream"><div class="wrap plate">
  <h2 class="pname bigname">The musicians are already here</h2>
  <p class="tagline">Adams Village &middot; Cedar Grove &middot; the St. Brendan&rsquo;s side of Dorchester</p>
  <p class="bodycopy">&ldquo;I grew up in this area,&rdquo; Delaney told the licensing board
  &mdash; Irish-born, first apartment on Adams Street, children and grandchildren at
  St. Brendan&rsquo;s. He told board chair Kathleen Joyce he knew how many Irish musicians
  live in the area, and how many had already reached out wanting to play at Session House.
  The pub isn&rsquo;t importing a concept; it&rsquo;s opening a room for players who already
  live on these streets.</p>
  <div class="ctarow"><a class="btn" href="/live-music">The whole music program</a>
  <a class="btn ghost" href="/contact">Leave a note for the players&rsquo; desk</a></div>
</div></section>
''',
    ld(TRAD_LDS))

# ---------------------------------------------------------------- PUB GRUB DETAIL
GRUB_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Elevated Pub Grub, Whiskey & the Seasonal Board — Session House, Adams Village Boston",
     "url": ORIGIN + "/pub-grub-adams-village", "isPartOf": {"@id": ORIGIN + "/#website"}},
    crumb([("Home", "/"), ("Live Music", "/live-music"), ("Pub Grub", "/pub-grub-adams-village")]),
    {"@type": "Service", "name": "Elevated pub grub and a seasonal drinks program",
     "serviceType": "Food and drink service",
     "areaServed": {"@type": "City", "name": "Boston"},
     "provider": {"@id": ORIGIN + "/#pub"}},
    faq([
        ("What kind of food?",
         "A refined take on pub fare — elevated dishes drawing inspiration from both Irish and New England traditions, per the pub's plan as covered by What Now Boston."),
        ("Can I see the menu online?",
         "The menu is being written as the kitchen comes together. Dish names and prices will live at the door when the pub opens, so this page carries the published plan rather than guessed dishes."),
        ("What's on the drinks side?",
         "The plan calls for an extensive, seasonally shifting beverage program: whiskey, cocktails, wine, and thoughtfully chosen beers."),
        ("Is there food during the music?",
         "The pub grub is built to run alongside the sessions — the room plan keeps music at conversation level, so plates and sets share the room without fighting."),
        ("Where is it?",
         "782 Adams St, Adams Village, Dorchester, Boston MA 02124 — opening mid-November 2026.")])] }

GRUB = page(
    "Elevated Pub Grub, Whiskey &amp; the Seasonal Board — Session House, Adams Village Boston",
    "Session House serves a refined take on pub grub drawn from Irish and New England traditions, with a seasonal board of whiskey, cocktails, wine and thoughtfully chosen beers. Boston, MA.",
    "/pub-grub-adams-village",
    '''
<section class="band ink herol"><div class="wrap">
  <p class="eyebrow">The kitchen &middot; the bar</p>
  <h1>Pub grub, elevated</h1>
  <p class="lede">The plan, in What Now Boston&rsquo;s words: &ldquo;a refined take on pub
  fare, with elevated dishes drawing inspiration from both Irish and New England
  traditions&rdquo; &mdash; food that keeps pub plainness out of its vocabulary but keeps the
  pub&rsquo;s welcome intact.</p>
</div></section>

<section class="band paper"><div class="wrap plate">
  <h2 class="pname bigname">Two traditions on one plate</h2>
  <p class="tagline">Irish &middot; New England</p>
  <p class="bodycopy">Irish pub cooking and New England cooking were always cousins: butter,
  shellfish, soda bread, stews, the Sunday roast that feeds six people in a small kitchen.
  The kitchen here is being planned as the elevated version of that shared table &mdash;
  pub grub done with technique, not pub grub done away. The same hands run the group&rsquo;s
  other rooms: Broadside Tavern on the waterfront, The Merchant Kitchen &amp; Drinks.</p>
</div></section>

<section class="band cream"><div class="wrap plate">
  <h2 class="pname bigname">The board turns with the season</h2>
  <p class="tagline">Whiskey &middot; cocktails &middot; wine &middot; beer</p>
  <p class="bodycopy">The published plan: &ldquo;an extensive, seasonally shifting beverage
  program&hellip; whiskey, cocktails, wine, and thoughtfully chosen beers.&rdquo; For an Irish
  pub, the whiskey shelf is the headline; the founding team&rsquo;s own statement puts &ldquo;a
  great pint&rdquo; in the same breath as great music and a beautiful room.</p>
  <div class="ctarow"><a class="btn" href="/story">Who&rsquo;s running the kitchens</a>
  <a class="btn ghost" href="/visit">Find 782 Adams St</a></div>
</div></section>

<section class="band forest"><div class="wrap narrow">
  <p class="eyebrow">The honest note</p>
  <h2 class="sec light">No menu invented here</h2>
  <p class="bodycopy">Dish names and prices will be written on boards at the door when the
  pub opens &mdash; so this page carries only what the pub&rsquo;s own team and the press have
  published about the food and drink program. When the first menu posts, it&rsquo;s an edit
  away, not a guess away.</p>
</div></section>
''',
    ld(GRUB_LDS))

# ---------------------------------------------------------------- STORY
STORY_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Our Story — Frank Delaney, Teresa Murphy & Session House",
     "url": ORIGIN + "/story", "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#pub"}},
    crumb([("Home", "/"), ("Our Story", "/story")]),
    {"@type": "Person", "name": "Frank Delaney", "jobTitle": "Restaurateur",
     "worksFor": {"@type": "Organization", "name": "Esteemed Hospitality, LLC"},
     "description": "Boston restaurateur behind Session House; operates Broadside Tavern and The Merchant Kitchen & Drinks; formerly The Times Irish Pub & Restaurant."},
    {"@type": "Person", "name": "Teresa Murphy", "jobTitle": "Managing partner",
     "worksFor": {"@id": ORIGIN + "/#pub"}},
    faq([
        ("Who runs Session House?",
         "Esteemed Hospitality, LLC — Frank Delaney's restaurant group (Broadside Tavern; The Merchant Kitchen & Drinks; formerly The Times Irish Pub & Restaurant) with managing partner Teresa Murphy."),
        ("What happened to Scobie's?",
         "Session House takes over the former Scobie's Cafe & Bar space at 782 Adams St. The family-run Scobie's opened in September 2024 and closed in February 2026; its renovation-and-reopen plans did not come to fruition."),
        ("Will the space look different?",
         "Light renovations are underway. The published plan: rich dark tones, warm gold accents, traditional musical imagery and an intimate feel — less a brand-new restaurant than a room that's always been there. Delaney told the Dorchester Reporter the interior is being re-designed with artist Vincent Crotty."),
        ("Why 'Session House'?",
         "'Session' for the communal tradition of musicians playing together; 'house' for the warmth and welcome of a neighborhood home — the naming the team published with What Now Boston."),
        ("When does it open?",
         "Mid-November 2026 per Boston.com's November openings roundup. Follow Facebook and Instagram for first-session dates.")])] }

STORY = page(
    "Our Story: Frank Delaney &amp; Teresa Murphy — Session House, Adams Village Boston",
    "Session House comes from Esteemed Hospitality — Frank Delaney (Broadside Tavern, The Merchant) and Teresa Murphy, in the old Scobie's space at 782 Adams St, where Delaney's first apartment stood.",
    "/story",
    f'''
<section class="band ink herol"><div class="wrap">
  <p class="eyebrow">The people &middot; the room</p>
  <h1>Coming home to Adams Street</h1>
  <p class="lede">&ldquo;I&rsquo;m from Ireland, but I say I grew up in this area because my
  first apartment was on Adams Street.&rdquo; Frank Delaney told the licensing board that, in
  September 2026, asking them to approve the pub he&rsquo;s putting in the old Scobie&rsquo;s
  space &mdash; his children went to St. Brendan&rsquo;s, he said, and his grandchildren go
  there now.</p>
</div></section>

<section class="band paper"><div class="wrap plate">
  <h2 class="pname bigname">Esteemed Hospitality, LLC</h2>
  <p class="tagline">The group behind the pub</p>
  <p class="bodycopy">Delaney runs <a href="https://broadsidetavernboston.com/" rel="noopener">Broadside Tavern</a>
  and <a href="https://www.themerchantboston.com/" rel="noopener">The Merchant Kitchen &amp; Drinks</a>
  in Boston, and formerly ran The Times Irish Pub &amp; Restaurant. Session House is the
  group&rsquo;s newest concept, with Teresa Murphy as managing partner &mdash; the voice on
  the licensing filings and the one guiding the renovation.</p>
</div></section>

<section class="band cream"><div class="wrap split">
  <div>
    <p class="eyebrow">The building</p>
    <h2 class="sec">The old Scobie&rsquo;s space, given a second life</h2>
    <p class="bodycopy">782 Adams Street has been a pub corner of the neighborhood&rsquo;s
    memory since the family-run Scobie&rsquo;s opened there in September 2024. Scobie&rsquo;s
    closed in February 2026, and Session House is taking the space with light renovations:
    rich dark tones, warm gold accents, traditional musical imagery &mdash; built, in What Now
    Boston&rsquo;s report, to feel like a well-established gathering place rather than a new
    restaurant. The interior is being re-designed with artist Vincent Crotty.</p>
  </div>
  <aside class="infocard">
    <h3 class="infh">The naming</h3>
    <dl class="factlist">
      <div><dt>Session</dt><dd>The communal tradition of musicians gathering to play together</dd></div>
      <div><dt>House</dt><dd>The warmth and welcome of a neighborhood home</dd></div>
      <div><dt>Soul</dt><dd>SOUL CE&Oacute;L &mdash; &ldquo;soul music&rdquo;: music and the community that keeps it alive</dd></div>
    </dl>
    <p class="bigm"><a href="/live-music">How the music works</a></p>
  </aside>
</div></section>

<section class="band forest"><div class="wrap narrow center">
  <p class="eyebrow">The team&rsquo;s own words</p>
  <p class="bigquote">&ldquo;Session House is about creating a place where people can come
  together. Great music, great food, a great pint, a beautiful room &mdash; and most
  importantly, a sense that everybody is welcome at the table.&rdquo;</p>
  <p class="note">The founding team, via What Now Boston &middot; the invitation they print with it:
  <em>Come for the music. Stay for the soul.</em></p>
  <p class="note">Watch for opening-night sessions: <a href="{IG}" rel="noopener">Instagram</a>
  &middot; <a href="{FB}" rel="noopener">Facebook</a> &middot; sources:
  <a href="{DOTNEWS}" rel="noopener">Dorchester Reporter</a> &middot;
  <a href="{WHATCHNOW}" rel="noopener">What Now Boston</a></p>
</div></section>
''',
    ld(STORY_LDS))

# ---------------------------------------------------------------- VISIT
VISIT_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Visit Session House — 782 Adams St, Adams Village, Boston",
     "url": ORIGIN + "/visit", "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#pub"}},
    crumb([("Home", "/"), ("Visit", "/visit")]),
    faq([
        ("Where exactly is Session House?",
         "782 Adams Street, in Adams Village (the Cedar Grove side) of Dorchester, Boston MA 02124 — the former Scobie's Cafe & Bar space."),
        ("When does it open?",
         "Mid-November 2026, per Boston.com's November openings roundup and the pub's own social bios."),
        ("What are the hours?",
         "Hours haven't been published yet — they post with the opening news on the pub's Facebook and Instagram pages, along with the first session dates."),
        ("Is there parking?",
         "Nothing about parking has been published yet. Ask through the contact form and the team answers."),
        ("How do we reach the team before opening?",
         "Email info@sessionhouseboston.com or use the contact form on this site.")])] }

VISIT = page(
    "Visit: 782 Adams St, Adams Village — Session House, Boston MA",
    "Session House opens mid-November 2026 at 782 Adams St, Adams Village, Dorchester, Boston MA 02124. Map, directions, opening info and contacts.",
    "/visit",
    f'''
<section class="band ink herol"><div class="wrap">
  <p class="eyebrow">Visit</p>
  <h1>Find 782 Adams St</h1>
  <p class="lede">Adams Village &mdash; the Dorchester side where the St. Brendan&rsquo;s
  parish life and the Adams Street stores meet. The building is the old Scobie&rsquo;s;
  the pub going into it opens mid-November 2026.</p>
</div></section>

<section class="band cream"><div class="wrap cardgrid">
  <div class="infocard"><h3 class="infh">Address</h3>
    <address class="addr">{ADDRESS_HTML}</address>
    <p class="note">Former Scobie&rsquo;s Cafe &amp; Bar space, Adams Village.</p>
    <p class="bigm"><a href="https://www.google.com/maps/dir/?api=1&amp;destination={MAP_Q}" rel="noopener">Get directions</a></p></div>
  <div class="infocard"><h3 class="infh">Opening</h3>
    <dl class="factlist">
      <div><dt>Window</dt><dd>Mid-November 2026</dd></div>
      <div><dt>Hours</dt><dd>Publish with the opening news</dd></div>
      <div><dt>Sessions</dt><dd>First dates land on Facebook &amp; Instagram</dd></div>
    </dl></div>
  <div class="infocard"><h3 class="infh">Reach the team</h3>
    <p class="note">Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use the
    <a href="/contact">contact form</a>.</p>
    <p class="note">Opening news: <a href="{IG}" rel="noopener">Instagram</a>
    &middot; <a href="{FB}" rel="noopener">Facebook</a></p></div>
</div></section>

<section class="band paper"><div class="wrap">
  <div class="mapcell"><iframe src="https://www.google.com/maps?q={MAP_Q}&amp;output=embed"
    title="Map: Session House, 782 Adams St, Adams Village, Boston, MA 02124" loading="lazy"></iframe></div>
  <p class="fineprint">Map: 782 Adams St, Adams Village, Boston, MA 02124 &mdash; the former Scobie&rsquo;s space.</p>
</div></section>

<section class="band ink"><div class="wrap narrow center">
  <h2 class="sec light">Before the first night</h2>
  <p class="secsub">The music program, the kitchen and bar plan, and the people behind the
  pub are all written up while the renovations finish.</p>
  <div class="ctarow"><a class="btn gold" href="/live-music">The music program</a>
  <a class="btn ghost" href="/contact">Send a note</a></div>
</div></section>
''',
    ld(VISIT_LDS))

# ---------------------------------------------------------------- CONTACT
CONTACT_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Contact Session House — Adams Village, Boston MA", "url": ORIGIN + "/contact",
     "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#pub"}},
    crumb([("Home", "/"), ("Contact", "/contact")])]}

CONTACT = page(
    "Contact Session House — Adams Village, Boston MA",
    "Questions for Session House in Adams Village, Boston: sessions, private tables, press or opening hours — the form and info@sessionhouseboston.com both reach the pub.",
    "/contact",
    f'''
<section class="band ink herol"><div class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Send the pub a note</h1>
  <p class="lede">Session nights, private tables for a party, press questions, opening
  hours &mdash; this form lands with the pub, same as email to {EMAIL}.</p>
</div></section>

<section class="band paper"><div class="wrap contactgrid">
  <div class="formside"><form class="cform" method="post" action="/contact" accept-charset="utf-8">
    <h2 class="infh">Leave a note</h2>
    <div class="fields">
      <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field full"><label for="f-email">Email <span class="opt">(optional &mdash; so we can answer)</span></label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      <div class="field full"><label for="f-msg">Your message</label><textarea id="f-msg" name="message" required></textarea></div>
    </div>
    <p class="formnote">Notes are read in the order they arrive.</p>
    <button class="btn full" type="submit">Send it</button>
  </form></div>
  <aside class="infocard"><h3 class="infh">Other ways</h3>
    <p class="note">Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <address class="addr">{ADDRESS_HTML}</address>
    <p class="note">Opening mid-November 2026 &mdash; hours land on
    <a href="{IG}" rel="noopener">Instagram</a> &middot;
    <a href="{FB}" rel="noopener">Facebook</a> with the first session dates.</p>
    <p class="note">Seen in: <a href="{DOTNEWS}" rel="noopener">Dorchester Reporter &mdash; licensing approval</a>
    &middot; <a href="{WHATCHNOW}" rel="noopener">What Now Boston</a></p>
  </aside>
</div></section>
''',
    ld(CONTACT_LDS))

# ---------------------------------------------------------------- PRIVACY
PRIVACY_LDS = {"@graph": [
    {"@type": "WebPage", "name": "Privacy — Session House, Boston MA", "url": ORIGIN + "/privacy",
     "isPartOf": {"@id": ORIGIN + "/#website"}},
    crumb([("Home", "/"), ("Privacy", "/privacy")])]}

PRIVACY = page(
    "Privacy — Session House, Boston MA",
    "How the Session House site handles the contact form: what it collects, what it doesn't, and who reads it.",
    "/privacy",
    f'''
<section class="band ink herol"><div class="wrap">
  <p class="eyebrow">Privacy</p>
  <h1>What this site does with your information</h1>
</div></section>

<section class="band paper"><div class="wrap narrow">
  <h2 class="sec">The contact form</h2>
  <p class="bodycopy">The form asks for a name and a message, and optionally a phone number and
  an email address. Those details go to Session House so the pub can answer you &mdash; nothing
  else. Notes are kept only as long as it takes to reply and settle whatever you asked about.</p>
  <h2 class="sec">No cookies, no trackers</h2>
  <p class="bodycopy">This site sets no cookies, runs no advertising pixels and loads no
  third-party scripts. There is no analytics software watching your visit and nothing to opt
  out of.</p>
  <h2 class="sec">The map</h2>
  <p class="bodycopy">The Visit page embeds a Google Maps view. When that map loads, Google
  receives the standard request data of your browser (including its IP address), under
  Google&rsquo;s own privacy terms. Every other page loads without contacting Google.</p>
  <h2 class="sec">Questions about your note</h2>
  <p class="bodycopy">Ask the pub through the <a href="/contact">contact form</a> to see,
  correct or delete what a note contains. We will honor it.</p>
  <p class="note">Postal address: {NAP_LINE}.</p>
</div></section>
''',
    ld(PRIVACY_LDS))

# ---------------------------------------------------------------- 404 / THANKS
THANKS = page(
    "Thank You — Session House, Boston MA",
    "Your note has reached Session House. The pub answers messages in the order they arrive.",
    "/thanks",
    '''
<section class="band forest herol"><div class="wrap narrow center">
  <p class="eyebrow">Note received</p>
  <h1>Your message is in.</h1>
  <p class="lede">The pub reads every note and answers in the order they arrive. First
  session dates and opening hours land on Instagram and Facebook.</p>
  <div class="ctarow center"><a class="btn" href="/">Back to the front page</a>
  <a class="btn ghost" href="/live-music">The music program</a></div>
</div></section>
''', None, og=False)

E404 = page(
    "Page Not Found — Session House, Boston MA",
    "That page isn't here. The music program, the pub grub page and the visit page are one click away.",
    "/404",
    '''
<section class="band cream herol"><div class="wrap narrow center">
  <p class="eyebrow">404</p>
  <h1>That tune isn&rsquo;t in the book.</h1>
  <p class="lede">No page at this set list. Try one of these:</p>
  <div class="ctarow center"><a class="btn" href="/">Front page</a>
  <a class="btn ghost" href="/live-music">Live music</a>
  <a class="btn ghost" href="/contact">Contact</a></div>
</div></section>
''', None, og=False)

# ---------------------------------------------------------------- sitemap / robots
PAGES_SITEMAP = ["/", "/live-music", "/irish-trad-music-dorchester", "/pub-grub-adams-village",
                 "/story", "/visit", "/contact", "/privacy"]
sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
for pp in PAGES_SITEMAP:
    sitemap += f'<url><loc>{ORIGIN}/</loc><lastmod>{BUILT}</lastmod></url>\n' if pp == "/" else f'<url><loc>{ORIGIN}{pp}</loc><lastmod>{BUILT}</lastmod></url>\n'
sitemap += "</urlset>\n"

robots = f"""User-agent: *
Disallow: /thanks
Disallow: /404

Sitemap: {ORIGIN}/sitemap.xml
"""

FILES = {"index.html": HOME, "live-music.html": MUSIC, "irish-trad-music-dorchester.html": TRAD,
         "pub-grub-adams-village.html": GRUB, "story.html": STORY, "visit.html": VISIT,
         "contact.html": CONTACT, "privacy.html": PRIVACY, "thanks.html": THANKS, "404.html": E404,
         "sitemap.xml": sitemap, "robots.txt": robots}

os.makedirs(PUBLIC, exist_ok=True)
for name, content in FILES.items():
    with open(os.path.join(PUBLIC, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, len(content.encode("utf-8")), "bytes")
