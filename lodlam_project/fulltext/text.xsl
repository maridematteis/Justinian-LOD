<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- Root template -->
  <xsl:template match="/tei:TEI">
    <html lang="en">
      <head>
        <title>
          <xsl:value-of select="normalize-space(tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main'])"/>
          <xsl:if test="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='sub']">
            <xsl:text> - </xsl:text>
            <xsl:value-of select="normalize-space(tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='sub'])"/>
          </xsl:if>
          <xsl:text> — A digital edition</xsl:text>
        </title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <style>
          /* CSS copied and adapted from your HTML (kept intentionally identical) */
          body {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f3efe6;
            color: #333;
            display: flex;
            justify-content: center;
            position: relative;
            overflow-x: hidden;
          }
          body::before {
            content: "";
            position: fixed;
            inset: 0;
            background: url("assets/img/6538981_1482.svg") center / cover no-repeat;
            filter: blur(1px);
            opacity: 0.5;
            transform: scale(1.05);
            z-index: -1;
            pointer-events: none;
          }
          .container {
            max-width: 860px;
            background: white;
            padding: 40px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            border: 1px solid #ddd;
          }
          h1, h2, h3, h4 {
            color: #5a3921;
            font-family: Georgia, serif;
          }
          h1 {
            border-bottom: 2px solid #c9ad7f;
            padding-bottom: 15px;
            margin-bottom: 30px;
            text-align: center;
          }
          h2 {
            border-left: 4px solid #c9ad7f;
            padding-left: 15px;
            margin-top: 40px;
          }
          h3 {
            color: #7a5c39;
            margin-top: 30px;
          }
          .author-info {
            font-style: italic;
            text-align: center;
            margin-bottom: 20px;
            color: #666;
          }
          .metadata-section {
            border: 1px solid #ddd;
            padding: 20px;
            margin-bottom: 30px;
            background-color: #f8f5ef;
            border-radius: 5px;
          }
          .bibl-info {
            margin-left: 10px;
            font-size: 0.95em;
            color: #555;
          }
          .bibl-info p { margin: 6px 0; }
          .meta-info { font-size: 0.9em; color: #777; margin-bottom: 10px; }
          .person-name, .place-name, .term-concept { font-weight: bold; color: #8b4513; }
          .note { font-size: 0.85em; color: #888; margin-left: 15px; border-left: 2px solid #ddd; padding-left: 8px; }
          .list-people, .list-places { margin-top: 12px; padding-left: 0; list-style: none; }
          .list-people li, .list-places li { margin-bottom: 8px; }
          .keywords-list { list-style: none; padding: 0; display: flex; flex-wrap: wrap; margin: 0; }
          .keywords-list li { background-color: #e6d7c1; border-radius: 3px; padding: 5px 10px; margin: 0 6px 6px 0; font-size: 0.9em; }
          .chapter { margin-bottom: 36px; text-align: justify; }
          p { text-align: justify; margin: 12px 0; }
          .page-break { font-size: 0.85em; color: #aaa; text-align: center; margin: 10px 0; font-style: italic; }
          .center { text-align: center; }
          .bold { font-weight: bold; }
          .italic { font-style: italic; }
          a { color: #8b4513; text-decoration: none; }
          a:hover { text-decoration: underline; }
          .pers { font-weight: 700; color: #6d4a2a; }
          .place { font-weight: 700; color: #5a5a5a; }
          .date { font-style: italic; color: #444; }
          .term { background-color: #fff3cd; color: #856404; padding: 2px 6px; border-radius: 3px; border: 1px solid #ffeaa7; font-weight: normal; }
          .term:hover { background-color: #ffeaa7; cursor: help; }
          @media (max-width: 768px) {
            .container { padding: 24px; margin: 10px; }
          }
        </style>
      </head>

      <body>
        <div class="container">
          <!-- Title -->
          <h1>
            <xsl:text>Procopius - History of the Wars (Books I-II)</xsl:text>
          </h1>
          <h2 class="center">A digital edition</h2>

          <!-- METADATA SECTION (fixed text to match your HTML exactly) -->
          <div class="metadata-section">
            <h2>Edition Information — Source Description</h2>
            <div style="display:flex; gap:18px; flex-wrap:wrap;">
              <div style="flex:1; min-width:260px; background:#fff; padding:12px; border-radius:4px; border:1px solid #e6ded2;">
                <h3>Original Edition</h3>
                <div class="bibl-info">
                  <p><strong>Title:</strong> Procopius — <em>History of the Wars, Books I and II</em></p>
                  <p><strong>Translator / Editor: </strong><a href="https://viaf.org/viaf/89376420" rel="noopener noreferrer" target="_blank">H.B.Dewing</a> (Loeb Classical Library)</p>
                  <p><strong>Publisher:</strong> Harvard University Press; William Heinemann Ltd.</p>
                  <p><strong>Place of publication:</strong> Cambridge, MA; London</p>
                  <p><strong>Imprint date:</strong> <span class="date">1961</span></p>
                  <p><strong>Identifiers:</strong> ISBN 9780674990548; id: procopius0001proc (Internet Archive)</p>
                  <p><strong>Online copy:</strong> <a href="https://archive.org/details/procopius0001proc" target="_blank">Internet Archive</a></p>
                  <p class="note">Loeb Classical Library. Vol. 1 contains History of the Wars, Books I-II (The Persian War).</p>
                </div>
              </div>

              <div style="flex:1; min-width:260px; background:#f0f8ff; padding:12px; border-radius:4px; border:1px solid #d8ecff;">
                <h3>Digital Edition (2025)</h3>
                <div class="bibl-info">
                  <p><strong>Project:</strong> Iustinianus LOD — course "Information Science and Cultural Heritage", University of Bologna</p>
                  <p><strong>Digital title:</strong> History of the Wars, Books I and II: A digital edition</p>
                  <p><strong>Digital curator / encoder:</strong> Maria Concetta De Matteis</p>
                  <p><strong>Digital publication date:</strong> 2025</p>
                  <p><strong>License:</strong><a href="https://creativecommons.org/licenses/by/4.0/" target="_blank"> CC-BY</a></p>
                </div>
              </div>
            </div>

            <h3>Project Description</h3>
            <p>Text encoded in XML/TEI for the project "Iustinianus LOD", developed for the course "Information Science and Cultural Heritage" (Digital Humanities and Digital Knowledge, University of Bologna). Selections document the reign and actions of Emperor <span class="pers">Justinian I</span> to support prosopographical and event-level analysis.</p>

            <h3>Cited People (selection)</h3>
            <ul class="list-people">
              <!-- These entries are hard-coded to match your HTML selection/order.
                   Where possible we attempt to fetch the @sameAs from the TEI; if not present
                   we still show the label. -->
              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='PR']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='PR']/tei:persName"/>
                </a>
                <xsl:text> — Author, historian (6th c.).</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='JUST']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='JUST']/tei:persName"/>
                </a>
                <xsl:text> — Emperor (527-565).</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='BEL']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='BEL']/tei:persName"/>
                </a>
                <xsl:text> — General under Justinian.</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='THEO']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='THEO']/tei:persName"/>
                </a>
                <xsl:text> — Empress (wife of Justinian).</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='ANT']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='ANT']/tei:persName"/>
                </a>
                <xsl:text> — Wife of Belisarius.</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='BOUZ']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='BOUZ']/tei:persName"/>
                </a>
                <xsl:text> — Officer (brother of Coutzes).</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='PHAR']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='PHAR']/tei:persName"/>
                </a>
                <xsl:text> — Leader (Eruli) active in Mesopotamia.</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='SUN']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='SUN']/tei:persName"/>
                </a>
                <xsl:text> — Commander (Massagetae).</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='AIG']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='AIG']/tei:persName"/>
                </a>
                <xsl:text> — Commander (Massagetae).</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='HERM']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='HERM']/tei:persName"/>
                </a>
                <xsl:text> — Magister who assisted Belisarius.</xsl:text>
              </li>

              <li>
                <a class="person-name" href="{/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='BARES']/@sameAs}"
                   rel="noopener noreferrer" target="_blank">
                  <xsl:value-of select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person[@xml:id='BARES']/tei:persName"/>
                </a>
                <xsl:text> — Persian commander.</xsl:text>
              </li>
            </ul>

            <h3>Places (selection)</h3>
            <ul class="list-places">
              <!-- hard-coded links to match your HTML -->
              <li><a class="place-name" href="https://pleiades.stoa.org/places/874444" rel="noopener noreferrer" target="_blank">Daras</a> — Frontier city in Mesopotamia.</li>
              <li><a class="place-name" href="https://pleiades.stoa.org/places/874623" rel="noopener noreferrer" target="_blank">Nisibis</a> — City on the Roman-Persian frontier.</li>
              <li><a class="place-name" href="https://pleiades.stoa.org/places/520985" rel="noopener noreferrer" target="_blank">Byzantium / Constantinople</a> — Imperial capital.</li>
              <li><a class="place-name" href="https://pleiades.stoa.org/places/874602" rel="noopener noreferrer" target="_blank">Mesopotamia</a> — Region of operations.</li>
            </ul>

            <h3>Keywords</h3>
            <ul class="keywords-list">
              <li>Battle</li>
              <li>Phalanx</li>
              <li>Massagetae (<a href="https://www.wikidata.org/wiki/Q379821" target="_blank">↗</a>)</li>
              <li>Immortals (<a href="https://www.wikidata.org/wiki/Q213165" target="_blank">↗</a>)</li>
            </ul>
          </div>

          <h2>Annotated Text Content</h2>

          <!-- Now transform the actual TEI text (front + body) -->
          <xsl:apply-templates select="tei:text"/>
        </div>
      </body>
    </html>
  </xsl:template>

  <!-- text -> process front and body -->
  <xsl:template match="tei:text">
    <xsl:apply-templates select="tei:front"/>
    <xsl:apply-templates select="tei:body"/>
  </xsl:template>

  <!-- front: map title_page and introduction -->
  <xsl:template match="tei:front">
    <div class="chapter">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <!-- body wrapper -->
  <xsl:template match="tei:body">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- div types -->
  <xsl:template match="tei:div[@type='title_page']">
    <div class="chapter">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="tei:div[@type='introduction']">
    <div class="chapter">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="tei:div[@type='workDesc']">
    <div class="chapter">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="tei:div[@type='chapter']">
    <div class="chapter">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <!-- head -> h3 or h2 depending on ancestor: keep simple: if parent is chapter then h3 -->
  <xsl:template match="tei:head">
    <h3>
      <xsl:apply-templates/>
    </h3>
  </xsl:template>

  <!-- p -> <p> with class if rend=center -->
  <xsl:template match="tei:p">
    <p>
      <xsl:choose>
        <xsl:when test="@rend='center'">
          <xsl:attribute name="class">center</xsl:attribute>
        </xsl:when>
      </xsl:choose>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!-- page break -->
  <xsl:template match="tei:pb">
    <div class="page-break">
      <xsl:text>[Page </xsl:text>
      <xsl:value-of select="@n"/>
      <xsl:text>]</xsl:text>
    </div>
  </xsl:template>

  <!-- lb -> line break -->
  <xsl:template match="tei:lb"><br/></xsl:template>

  <!-- hi -> bold/italic -->
  <xsl:template match="tei:hi">
    <xsl:choose>
      <xsl:when test="@rend='italic'">
        <span class="italic"><xsl:apply-templates/></span>
      </xsl:when>
      <xsl:when test="@rend='bold'">
        <span class="bold"><xsl:apply-templates/></span>
      </xsl:when>
      <xsl:otherwise>
        <span><xsl:apply-templates/></span>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- persName: try to create link using @ref (http or #ref -> lookup sameAs in profileDesc) -->
  <xsl:template match="tei:persName">
    <xsl:variable name="r" select="@ref"/>
    <xsl:choose>
      <!-- direct http(s) ref -->
      <xsl:when test="string-length($r) &gt; 0 and (substring($r,1,4) = 'http')">
        <a class="person-name" href="{$r}" target="_blank" rel="noopener noreferrer">
          <xsl:apply-templates/>
        </a>
      </xsl:when>

      <!-- local reference like #PR -->
      <xsl:when test="string-length($r) &gt; 0 and substring($r,1,1)='#'">
        <xsl:variable name="id" select="substring-after($r,'#')"/>
        <xsl:variable name="same" select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc//tei:person[@xml:id=$id]/@sameAs"/>
        <xsl:choose>
          <xsl:when test="string-length($same) &gt; 0">
            <a class="person-name" href="{$same}" target="_blank" rel="noopener noreferrer">
              <xsl:apply-templates/>
            </a>
          </xsl:when>
          <xsl:otherwise>
            <span class="person-name">
              <xsl:apply-templates/>
            </span>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>

      <!-- fallback: no ref -->
      <xsl:otherwise>
        <span class="person-name"><xsl:apply-templates/></span>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- placeName: similar approach to persName -->
  <xsl:template match="tei:placeName">
    <xsl:variable name="r" select="@ref"/>
    <xsl:choose>
      <xsl:when test="string-length($r) &gt; 0 and (substring($r,1,4) = 'http')">
        <a class="place-name" href="{$r}" target="_blank" rel="noopener noreferrer">
          <xsl:apply-templates/>
        </a>
      </xsl:when>

      <xsl:when test="string-length($r) &gt; 0 and substring($r,1,1)='#'">
        <xsl:variable name="id" select="substring-after($r,'#')"/>
        <xsl:variable name="same" select="/tei:TEI/tei:teiHeader/tei:profileDesc/tei:settingDesc//tei:place[@xml:id=$id]/@sameAs"/>
        <xsl:choose>
          <xsl:when test="string-length($same) &gt; 0">
            <a class="place-name" href="{$same}" target="_blank" rel="noopener noreferrer">
              <xsl:apply-templates/>
            </a>
          </xsl:when>
          <xsl:otherwise>
            <span class="place-name"><xsl:apply-templates/></span>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>

      <xsl:otherwise>
        <span class="place-name"><xsl:apply-templates/></span>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- term -> highlighted concept -->
  <xsl:template match="tei:term">
    <span class="term-concept"><xsl:apply-templates/></span>
  </xsl:template>

  <!-- date -->
  <xsl:template match="tei:date">
    <span class="date"><xsl:apply-templates/></span>
  </xsl:template>

  <!-- note -->
  <xsl:template match="tei:note">
    <span class="note"><xsl:apply-templates/></span>
  </xsl:template>

  <!-- fallback for other elements: copy text -->
  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
    <xsl:text> </xsl:text>
  </xsl:template>

  <!-- ignore attributes not needed -->
  <xsl:template match="tei:ref | tei:idno | tei:editor | tei:editorialDesc | tei:projectDesc | tei:listBibl" />

</xsl:stylesheet>
