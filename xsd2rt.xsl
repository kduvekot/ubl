<?xml version="1.0" encoding="UTF-8"?>
<!--
  Derive a run-time (RT) schema module from an annotated schema module.

  The xsdrt trees exist for instance validation, so they carry no
  documentation ballast: every xsd:annotation and every comment inside the
  schema element is discarded, together with the whitespace those nodes
  leave behind.

  Comments *outside* the schema element are kept. That is where the module
  header and the OASIS copyright and IPR notices live, and deleting them
  would strip the legal text from the distribution. Only the Module: line of
  the header is rewritten, to name the run-time location of the module.

  This reproduces, for the hand-maintained modules, what the generator
  already does for every generated module. Verified by transforming the
  published UBL 2.5 OS xsd/common modules and comparing the result with the
  published xsdrt/common modules.
-->
<xsl:stylesheet version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema">

<xsl:output method="xml" encoding="UTF-8" indent="yes"/>

<!--The source layout is not worth preserving once the documentation is gone:
    discarding it and letting the serialiser re-indent gives uniform output
    instead of a mixture of original and regenerated indentation. Schema
    documents carry no mixed content outside xsd:annotation, which is removed
    here anyway, so no significant whitespace is at risk.-->
<xsl:strip-space elements="*"/>

<xsl:template match="@*|node()">
  <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
</xsl:template>

<!--documentation ballast-->
<xsl:template match="xsd:annotation"/>
<xsl:template match="/*//comment()"/>

<!--header: name the run-time location of the module. Comments outside the
    schema element that carry no Module: line, such as the trailing OASIS
    notices, pass through unchanged.-->
<xsl:template match="/comment()">
  <xsl:comment>
    <xsl:value-of select="replace(.,
                                  '(\n\s*Module:[ \t]+)(xsd/common/|xsdrt/common/)?',
                                  '$1xsdrt/common/')"/>
  </xsl:comment>
</xsl:template>

</xsl:stylesheet>
