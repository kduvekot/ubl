<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:gc="http://docs.oasis-open.org/codelist/ns/genericode/1.0/"
  exclude-result-prefixes="gc">

<!--
  Automatically update row number references in UBL.xml based on the actual
  row positions in the UBL-Entities genericode file.

  Usage:
    java -jar utilities/saxon9he/saxon9he.jar \
      -xsl:utilities/update-ubl-row-numbers.xsl \
      -s:UBL.xml \
      -o:UBL-updated.xml \
      gc-uri=UBL-Entities-2.5.gc

  This script updates all <ulink role="DEN-Row"> elements to match the
  actual row numbers calculated from the .gc file, using the same algorithm
  as hub-integrity.xsl for validation.
-->

  <xsl:output method="xml" indent="no" encoding="UTF-8"/>

  <!-- Path to the genericode file containing the model data -->
  <xsl:param name="gc-uri" required="yes"/>

  <!-- Load the genericode file -->
  <xsl:variable name="gc" select="document(translate($gc-uri,'\','/'))"/>

  <!-- Key to look up rows by Dictionary Entry Name (DEN) -->
  <xsl:key name="rows"
           match="gc:Row"
           use="gc:Value[@ColumnRef='DictionaryEntryName']/gc:SimpleValue"/>

  <!-- Identity template: copy everything by default -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!--
    Update the text content of <ulink role="DEN-Row"> elements
    to match the actual row number in the genericode file.

    Algorithm:
    1. Get the DEN from @remap attribute
    2. Look up the row in the .gc file
    3. Calculate row number: 2 + count of preceding rows in same model
    4. Replace the text with the calculated row number
  -->
  <xsl:template match="ulink[@role='DEN-Row']/text()">
    <xsl:variable name="den" select="../@remap"/>

    <!-- Look up the row by DEN -->
    <xsl:variable name="row" select="key('rows', $den, $gc)"/>

    <xsl:choose>
      <xsl:when test="$row">
        <!-- Get the model name for this row -->
        <xsl:variable name="model"
          select="$row/gc:Value[@ColumnRef='ModelName']/gc:SimpleValue"/>

        <!--
          Calculate the row number:
          - Start at row 2 (accounting for header rows)
          - Add the count of preceding rows in the same model
        -->
        <xsl:variable name="rowNum" select="
          2 + count($row/preceding-sibling::gc:Row[
            gc:Value[@ColumnRef='ModelName']/gc:SimpleValue = $model
          ])"/>

        <!-- Output the calculated row number -->
        <xsl:value-of select="$rowNum"/>
      </xsl:when>
      <xsl:otherwise>
        <!--
          DEN not found in .gc file - keep original value and warn
          (hub-integrity.xsl will catch this as an error)
        -->
        <xsl:message>
          <xsl:text>WARNING: DEN not found in .gc file: </xsl:text>
          <xsl:value-of select="$den"/>
        </xsl:message>
        <xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
