import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

BASE_URL = "https://lordcika.github.io"

INDEX_PATH = Path("index.html")
FEED_PATH = Path("feed.xml")
ARTICLES_JSON_PATH = Path("content/articles.json")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def load_articles() -> list[dict]:
    data = json.loads(read_text(ARTICLES_JSON_PATH))
    if not isinstance(data, list) or not data:
        raise ValueError("content/articles.json deve contenere una lista non vuota di articoli.")
    return data


def replace_marker_block(html: str, marker_name: str, new_content: str) -> str:
    start = f"<!-- AUTO:{marker_name}:start -->"
    end = f"<!-- AUTO:{marker_name}:end -->"

    pattern = re.compile(
        rf"({re.escape(start)})(.*)({re.escape(end)})",
        re.DOTALL
    )

    if not pattern.search(html):
        raise ValueError(f"Marker non trovato in index.html: {marker_name}")

    replacement = f"{start}\n{new_content}\n{end}"
    return pattern.sub(replacement, html, count=1)


def html_escape(text: str) -> str:
    return escape(text, {"'": "&#39;", '"': "&quot;"})


def article_absolute_url(article_url: str) -> str:
    return f"{BASE_URL}/{article_url}"


def image_absolute_url(image_url: str) -> str:
    return f"{BASE_URL}/{image_url}"


def build_latest_button(article: dict) -> str:
    return f'<a href="{html_escape(article["article_url"])}" class="cta">Leggi l\'ultimo</a>'


def build_hero(article: dict) -> str:
    title = html_escape(article["title"])
    article_url = html_escape(article["article_url"])
    cover_image = html_escape(article["cover_image"])
    display_date = html_escape(article["display_date"])
    hero_excerpt = html_escape(article["hero_excerpt"])
    author = html_escape(article["author"])

    return f"""<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <article class="hero-main glass" style="--hero-bg: url('{cover_image}');">
        <a
          class="hero-main-link"
          href="{article_url}"
          aria-label="Leggi {title}"
        ></a>

        <div class="hero-content">
          <span class="eyebrow">In evidenza · {display_date}</span>
          <h1 class="hero-title">{title}</h1>
          <p class="hero-copy">
            {hero_excerpt}
          </p>
          <div class="hero-author">di {author}</div>
        </div>
      </article>

      <div class="hero-side">
        <div class="panel glass identity-panel">
          <div>
            <h3>About</h3>
            <div class="identity-about">
              <p>
                INOoriginal è un archivio editoriale personale in cui raccolgo articoli, analisi
                e riflessioni su propaganda, disinformazione, Israele, media digitali, conflitti
                narrativi e intelligenza artificiale.
              </p>
              <p>
                È uno spazio autoriale: meno rumore da social, più contesto, struttura e lettura
                critica. Non inseguo il flusso delle notizie: provo a capire come vengono
                raccontate, deformate e usate.
              </p>
              <p>
                L'idea della pagina è semplice: osservare il linguaggio, smontare la propaganda e
                dare agli eventi una forma più leggibile.
              </p>
            </div>
          </div>

          <div class="identity-socials">
            <div class="identity-socials-label">Segui il progetto</div>

            <div
              class="identity-socials-row"
              aria-label="Social e condivisione sito"
            >
              <a
                class="identity-social-btn"
                href="https://www.facebook.com/zavathalavudvash"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Facebook"
                title="Facebook"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.9.3-1.6 1.6-1.6H17V3.8c-.3 0-.9-.1-1.8-.1-1.8 0-3.1 1.1-3.1 3.3V10H9.5v3h2.6v8h1.4z"/>
                </svg>
                <span>Facebook</span>
              </a>

              <a
                class="identity-social-btn"
                href="https://www.linkedin.com/in/marco-d-80026a149"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="LinkedIn"
                title="LinkedIn"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M6.9 8.5A1.9 1.9 0 1 1 6.9 4.7a1.9 1.9 0 0 1 0 3.8zM5.1 9.9h3.5V20H5.1V9.9zm5.5 0H14v1.4h.1c.5-.9 1.6-1.7 3.2-1.7 3.4 0 4 2.2 4 5.2V20h-3.5v-4.6c0-1.1 0-2.5-1.5-2.5s-1.8 1.2-1.8 2.4V20h-3.5V9.9z"/>
                </svg>
                <span>LinkedIn</span>
              </a>

              <a
                class="identity-social-btn"
                href="https://x.com/LordWiesenthal"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="X"
                title="X"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M18.9 3H21l-4.6 5.3L21.8 21h-4.7l-3.7-4.8L9.2 21H7.1l5-5.8L2.8 3h4.8l3.3 4.4L14.8 3h4.1zm-1.6 16h1.3L6.7 4.9H5.3L17.3 19z"/>
                </svg>
                <span>X</span>
              </a>

              <button
                class="identity-social-btn"
                id="shareSiteBtn"
                type="button"
                aria-label="Condividi sito"
                title="Condividi sito"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M18 16.1c-.8 0-1.5.3-2 .8l-7.1-4.1c.1-.3.1-.5.1-.8s0-.5-.1-.8l7-4.1c.5.5 1.2.8 2 .8a3 3 0 1 0-2.9-3.6L8 8.4a3 3 0 1 0 0 7.2l7 4.1a3 3 0 1 0 3-3.6z"/>
                </svg>
                <span>Condividi</span>
              </button>
            </div>
          </div>
        </div>

        <div class="panel glass live-panel">
          <h3>Direzione</h3>
          <p>Monitor live degli alert missilistici su Israele.</p>

          <div class="live-widget-wrap">
            <iframe
              class="live-widget"
              src="https://rocketalert.live/"
              title="Rocket alerts live in Israel"
              loading="lazy"
              referrerpolicy="no-referrer"
            ></iframe>
          </div>

          <div class="live-fallback">
            Se il widget non si carica, aprilo direttamente qui:
            <a
              href="https://rocketalert.live/"
              target="_blank"
              rel="noopener noreferrer"
            >rocketalert.live</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""


def build_featured_card(article: dict) -> str:
    title = html_escape(article["title"])
    category = html_escape(article["category"])
    author = html_escape(article["author"])
    description = html_escape(article["description"])
    article_url = html_escape(article["article_url"])
    cover_image = html_escape(article["cover_image"])
    date = html_escape(article["date"])

    return f"""<article class="card glass" data-date="{date}">
  <div
    class="card-media"
    style="background-image: linear-gradient(180deg, rgba(6,8,12,0.08), rgba(6,8,12,0.18)), url('{cover_image}');"
  ></div>

  <div class="card-body glass">
    <span class="eyebrow">{category}</span>
    <h3 class="card-title">{title}</h3>
    <div class="card-author">{author}</div>
    <div class="card-copy">
      {description}
    </div>

    <div class="tag-row">
      <span class="tag">{category}</span>
      <span class="tag">{author}</span>
    </div>

    <a class="card-link article-link" href="{article_url}">
      Leggi articolo
    </a>

    <div class="share-buttons" data-share-title="{title}">
      <a class="share-btn share-facebook" href="#" target="_blank" rel="noopener noreferrer">Facebook</a>
      <a class="share-btn share-x" href="#" target="_blank" rel="noopener noreferrer">X</a>
      <a class="share-btn share-linkedin" href="#" target="_blank" rel="noopener noreferrer">LinkedIn</a>
    </div>
  </div>
</article>"""


def build_latest_articles(articles: list[dict]) -> str:
    latest_three = articles[:3]
    return "\n\n".join(build_featured_card(article) for article in latest_three)


def build_archive_card(article: dict) -> str:
    title = html_escape(article["title"])
    author = html_escape(article["author"])
    article_url = html_escape(article["article_url"])
    cover_image = html_escape(article["cover_image"])
    display_date = html_escape(article["display_date"])
    date = html_escape(article["date"])

    return f"""<article class="archive-card" data-date="{date}">
  <a class="archive-cover-link article-link" href="{article_url}">
    <img class="archive-cover" src="{cover_image}" alt="{title}" loading="lazy" />
  </a>
  <div class="archive-content">
    <h3><a class="archive-title-link article-link" href="{article_url}">{title}</a></h3>
    <div class="archive-author">{author}</div>
    <p>{display_date}</p>
    <div class="share-buttons archive-share" data-share-title="{title}">
      <a class="share-btn share-facebook" href="#" target="_blank" rel="noopener noreferrer">Facebook</a>
      <a class="share-btn share-x" href="#" target="_blank" rel="noopener noreferrer">X</a>
      <a class="share-btn share-linkedin" href="#" target="_blank" rel="noopener noreferrer">LinkedIn</a>
    </div>
  </div>
</article>"""


def build_archive(articles: list[dict]) -> str:
    return "\n\n".join(build_archive_card(article) for article in articles)


def build_feed_item(article: dict) -> str:
    title = escape(article["title"])
    description = escape(article["description"])
    url = escape(article_absolute_url(article["article_url"]))
    guid = url
    pub_date = escape(article["date"])

    return f"""    <item>
      <title>{title}</title>
      <link>{url}</link>
      <guid>{guid}</guid>
      <description>{description}</description>
      <pubDate>{pub_date}</pubDate>
    </item>"""


def build_feed(articles: list[dict]) -> str:
    items = "\n".join(build_feed_item(article) for article in articles)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>INOoriginal</title>
    <link>{BASE_URL}/</link>
    <description>Archivio editoriale personale di Lord Cika</description>
    <language>it-it</language>
{items}
  </channel>
</rss>
"""


def update_index(articles: list[dict]) -> None:
    latest = articles[0]
    html = read_text(INDEX_PATH)

    html = replace_marker_block(html, "latest-button", build_latest_button(latest))
    html = replace_marker_block(html, "hero", build_hero(latest))
    html = replace_marker_block(html, "latest-articles", build_latest_articles(articles))
    html = replace_marker_block(html, "archive", build_archive(articles))

    write_text(INDEX_PATH, html)


def update_feed(articles: list[dict]) -> None:
    feed_content = build_feed(articles)
    write_text(FEED_PATH, feed_content)


def main() -> None:
    articles = load_articles()
    update_index(articles)
    update_feed(articles)
    print("OK: index.html e feed.xml aggiornati.")


if __name__ == "__main__":
    main()
