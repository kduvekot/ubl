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
      -o:UBL.xml \
      gc-uri=UBL-Entities-2.5.gc

  This script updates all <ulink role="DEN-Row"> elements to match the
  actual row numbers calculated from the .gc file, using the same algorithm
  as hub-integrity.xsl for validation.

  WORKFLOW FOR ADDING NEW REFERENCES:

  1. When adding a new link in UBL.xml, use "0" as a placeholder:
     <ulink role="DEN-Row" remap="Party. Details">0</ulink>

  2. The @remap attribute must contain the exact Dictionary Entry Name (DEN)
     from the .gc file (e.g., "Party. Details", "Invoice. Details", etc.)

  3. Run this script to automatically fill in the correct row numbers

  4. The script will warn you if a DEN is not found in the .gc file
-->

  <xsl:output method="xml" indent="no" encoding="UTF-8"/>

  <!-- Path to the genericode file containing the model data -->
  <xsl:param name="gc-uri" required="yes"/>

  <!-- Load the genericode file -->
  <xsl:variable name="gc" select="document(translate($gc-uri,'\','/'))"/>

  <!-- Track statistics -->
  <xsl:variable name="total-refs" select="count(//ulink[@role='DEN-Row'])"/>

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

        <!-- Log if we're updating a value (not just confirming it's correct) -->
        <xsl:if test=". != $rowNum">
          <xsl:message>
            <xsl:text>  Updated: </xsl:text>
            <xsl:value-of select="$den"/>
            <xsl:text> (</xsl:text>
            <xsl:value-of select="."/>
            <xsl:text> → </xsl:text>
            <xsl:value-of select="$rowNum"/>
            <xsl:text>)</xsl:text>
          </xsl:message>
        </xsl:if>

        <!-- Output the calculated row number -->
        <xsl:value-of select="$rowNum"/>
      </xsl:when>
      <xsl:otherwise>
        <!--
          DEN not found in .gc file - keep original value and warn
          (hub-integrity.xsl will catch this as an error)
        -->
        <xsl:message terminate="no">
          <xsl:text>ERROR: DEN not found in .gc file: "</xsl:text>
          <xsl:value-of select="$den"/>
          <xsl:text>" - keeping original value </xsl:text>
          <xsl:value-of select="."/>
        </xsl:message>
        <xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Print summary report at the end -->
  <xsl:template match="/">
    <xsl:message>
      <xsl:text>&#xa;========================================&#xa;</xsl:text>
      <xsl:text>UBL Row Number Auto-Update&#xa;</xsl:text>
      <xsl:text>========================================&#xa;</xsl:text>
      <xsl:text>Source: </xsl:text>
      <xsl:value-of select="base-uri(/)"/>
      <xsl:text>&#xa;</xsl:text>
      <xsl:text>GC file: </xsl:text>
      <xsl:value-of select="$gc-uri"/>
      <xsl:text>&#xa;</xsl:text>
      <xsl:text>Total DEN-Row references: </xsl:text>
      <xsl:value-of select="$total-refs"/>
      <xsl:text>&#xa;</xsl:text>
      <xsl:text>========================================&#xa;</xsl:text>
    </xsl:message>
    <xsl:next-match/>
    <xsl:message>
      <xsl:text>&#xa;Done. Check output for any ERROR messages.&#xa;</xsl:text>
    </xsl:message>
  </xsl:template>

</xsl:stylesheet>
