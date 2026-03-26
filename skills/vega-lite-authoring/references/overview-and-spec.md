# Vega-Lite Overview and Specification

Purpose: Top-level grammar and how the high-level spec is structured.

Source URLs:
- https://vega.github.io/vega-lite/docs/
- https://vega.github.io/vega-lite/docs/spec.html

## Overview

Source URL: https://vega.github.io/vega-lite/docs/

[Edit this page](https://github.com/vega/vega-lite/edit/next/site/docs/overview.md)

**Vega-Lite** is a high-level grammar for interactive graphics. It provides a concise JSON syntax for supporting rapid generation of interactive multi-view visualizations to support analysis. Vega-Lite can serve as a declarative format for describing and creating data visualizations. To use Vega-Lite, our compiler compiles a Vega-Lite specification into a lower-level, more detailed [Vega](https://vega.github.io/vega) specifications and rendered using Vega’s compiler.

This documentation describes the [JSON specification language](spec.html) and how to [use Vega-Lite visualizations](/vega-lite/usage/embed.html) in a web application.

  Search

## Table of Contents

Below is an overview of the documentation for Vega-Lite properties. See [the specification page](spec.html) for an overview of Vega-Lite specifications.

*   [Overview](/vega-lite/docs/index.html)
    *   [Table of Contents](/vega-lite/docs/index.html#toc)
*   [View Specification](/vega-lite/docs/spec.html)
    *   [Documentation Overview](/vega-lite/docs/spec.html#documentation-overview)
    *   [Common Properties of Specifications](/vega-lite/docs/spec.html#common)
    *   [Top-Level Specifications](/vega-lite/docs/spec.html#top-level)
    *   [Single View Specifications](/vega-lite/docs/spec.html#single)
    *   [Layered and Multi-view Specifications](/vega-lite/docs/spec.html#layered-and-multi-view-specifications)
    *   [View Configuration](/vega-lite/docs/spec.html#config)
    *   [Title](/vega-lite/docs/title.html)
        *   [Title Properties Object](/vega-lite/docs/title.html#props)
        *   [Title Config](/vega-lite/docs/title.html#config)
    *   [Width / Height](/vega-lite/docs/size.html)
        *   [Documentation Overview](/vega-lite/docs/size.html#documentation-overview)
        *   [Width and Height of Single and Layered Plots](/vega-lite/docs/size.html#width-and-height-of-single-and-layered-plots)
        *   [Width and Height of Multi-View Displays](/vega-lite/docs/size.html#width-and-height-of-multi-view-displays)
*   [Data / Datasets](/vega-lite/docs/data.html)
    *   [Documentation Overview](/vega-lite/docs/data.html#documentation-overview)
    *   [Types of Data Sources](/vega-lite/docs/data.html#types-of-data-sources)
    *   [Format](/vega-lite/docs/data.html#format)
    *   [Data Generators](/vega-lite/docs/data.html#data-generators)
    *   [Datasets](/vega-lite/docs/data.html#datasets)
*   [Transform](/vega-lite/docs/transform.html)
    *   [View-level Transform Property](/vega-lite/docs/transform.html#view-level-transform-property)
    *   [Aggregate](/vega-lite/docs/aggregate.html)
        *   [Documentation Overview](/vega-lite/docs/aggregate.html#documentation-overview)
        *   [Aggregate in Encoding Field Definition](/vega-lite/docs/aggregate.html#encoding)
        *   [Aggregate Transform](/vega-lite/docs/aggregate.html#transform)
        *   [Supported Aggregation Operations](/vega-lite/docs/aggregate.html#ops)
        *   [Argmin / Argmax](/vega-lite/docs/aggregate.html#argmax)
    *   [Bin](/vega-lite/docs/bin.html)
        *   [Documentation Overview](/vega-lite/docs/bin.html#documentation-overview)
        *   [Binning in Encoding Field Definition](/vega-lite/docs/bin.html#encoding)
        *   [Bin Transform](/vega-lite/docs/bin.html#transform)
        *   [Bin Parameters](/vega-lite/docs/bin.html#bin-parameters)
        *   [Ordinal Bin](/vega-lite/docs/bin.html#ordinal-bin)
    *   [Calculate](/vega-lite/docs/calculate.html)
        *   [Calculate Transform Definition](/vega-lite/docs/calculate.html#calculate-transform-definition)
        *   [Example](/vega-lite/docs/calculate.html#example)
    *   [Density](/vega-lite/docs/density.html)
        *   [Density Transform Definition](/vega-lite/docs/density.html#density-transform-definition)
        *   [Usage](/vega-lite/docs/density.html#usage)
    *   [Extent](/vega-lite/docs/extent.html)
        *   [Extent Transform Definition](/vega-lite/docs/extent.html#extent-transform-definition)
        *   [Usage](/vega-lite/docs/extent.html#usage)
        *   [Example](/vega-lite/docs/extent.html#example)
    *   [Filter](/vega-lite/docs/filter.html)
    *   [Flatten](/vega-lite/docs/flatten.html)
        *   [Flatten Transform Definition](/vega-lite/docs/flatten.html#flatten-transform-definition)
        *   [Usage](/vega-lite/docs/flatten.html#usage)
        *   [Examples](/vega-lite/docs/flatten.html#examples)
    *   [Fold](/vega-lite/docs/fold.html)
        *   [Fold Transform Definition](/vega-lite/docs/fold.html#fold-transform-definition)
        *   [Usage](/vega-lite/docs/fold.html#usage)
        *   [Example](/vega-lite/docs/fold.html#example)
    *   [Impute](/vega-lite/docs/impute.html)
        *   [Documentation Overview](/vega-lite/docs/impute.html#documentation-overview)
        *   [Impute in Encoding Field Definition](/vega-lite/docs/impute.html#encoding)
        *   [Impute Transform](/vega-lite/docs/impute.html#transform)
    *   [Join Aggregate](/vega-lite/docs/joinaggregate.html)
        *   [Documentation Overview](/vega-lite/docs/joinaggregate.html#documentation-overview)
        *   [Join Aggregate Field Definition](/vega-lite/docs/joinaggregate.html#join-aggregate-field-definition)
        *   [Join Aggregate Transform Definition](/vega-lite/docs/joinaggregate.html#join-aggregate-transform-definition)
        *   [Examples](/vega-lite/docs/joinaggregate.html#ops)
    *   [Loess](/vega-lite/docs/loess.html)
        *   [Loess Transform Definition](/vega-lite/docs/loess.html#loess-transform-definition)
        *   [Usage](/vega-lite/docs/loess.html#usage)
        *   [Example](/vega-lite/docs/loess.html#example)
    *   [Lookup](/vega-lite/docs/lookup.html)
        *   [Lookup Transform](/vega-lite/docs/lookup.html#lookup-transform)
    *   [Pivot](/vega-lite/docs/pivot.html)
        *   [Pivot Transform Definition](/vega-lite/docs/pivot.html#pivot-transform-definition)
        *   [Usage](/vega-lite/docs/pivot.html#usage)
        *   [Example](/vega-lite/docs/pivot.html#example)
    *   [Quantile](/vega-lite/docs/quantile.html)
        *   [Quantile Transform Definition](/vega-lite/docs/quantile.html#quantile-transform-definition)
        *   [Usage](/vega-lite/docs/quantile.html#usage)
    *   [Regression](/vega-lite/docs/regression.html)
        *   [Regression Transform Definition](/vega-lite/docs/regression.html#regression-transform-definition)
        *   [Usage](/vega-lite/docs/regression.html#usage)
        *   [Example](/vega-lite/docs/regression.html#example)
    *   [Sample](/vega-lite/docs/sample.html)
        *   [Sample Transform Definition](/vega-lite/docs/sample.html#sample-transform-definition)
        *   [Usage](/vega-lite/docs/sample.html#usage)
        *   [Example](/vega-lite/docs/sample.html#example)
    *   [Stack](/vega-lite/docs/stack.html)
        *   [Documentation Overview](/vega-lite/docs/stack.html#documentation-overview)
        *   [Stack in Encoding Field Definition](/vega-lite/docs/stack.html#encoding)
        *   [Stack Transform](/vega-lite/docs/stack.html#transform)
    *   [Time Unit](/vega-lite/docs/timeunit.html)
        *   [Documentation Overview](/vega-lite/docs/timeunit.html#documentation-overview)
        *   [Time Unit in Encoding Field Definition](/vega-lite/docs/timeunit.html#encoding)
        *   [Time Unit Transform](/vega-lite/docs/timeunit.html#transform)
        *   [UTC time](/vega-lite/docs/timeunit.html#utc)
        *   [Time Unit Parameters](/vega-lite/docs/timeunit.html#params)
    *   [Window](/vega-lite/docs/window.html)
        *   [Documentation Overview](/vega-lite/docs/window.html#documentation-overview)
        *   [Window Field Definition](/vega-lite/docs/window.html#window-field-definition)
        *   [Window Transform Definition](/vega-lite/docs/window.html#window-transform-definition)
        *   [Window Only Operation Reference](/vega-lite/docs/window.html#ops)
        *   [Examples](/vega-lite/docs/window.html#examples)
*   [Mark](/vega-lite/docs/mark.html)
    *   [Documentation Overview](/vega-lite/docs/mark.html#documentation-overview)
    *   [Mark Types](/vega-lite/docs/mark.html#types)
    *   [Mark Definition Object](/vega-lite/docs/mark.html#mark-def)
    *   [Mark Config](/vega-lite/docs/mark.html#config)
    *   [Mark Style Config](/vega-lite/docs/mark.html#style-config)
    *   [Arc](/vega-lite/docs/arc.html)
        *   [Documentation Overview](/vega-lite/docs/arc.html#documentation-overview)
        *   [Arc Mark Properties](/vega-lite/docs/arc.html#properties)
        *   [Examples](/vega-lite/docs/arc.html#examples)
        *   [Arc Config](/vega-lite/docs/arc.html#arc-config)
        *   [Faceted Pie Charts](/vega-lite/docs/arc.html#faceted-pie-charts)
    *   [Area](/vega-lite/docs/area.html)
        *   [Documentation Overview](/vega-lite/docs/area.html#documentation-overview)
        *   [Area Mark Properties](/vega-lite/docs/area.html#properties)
        *   [Examples](/vega-lite/docs/area.html#examples)
        *   [Area Config](/vega-lite/docs/area.html#config)
    *   [Bar](/vega-lite/docs/bar.html)
        *   [Documentation Overview](/vega-lite/docs/bar.html#documentation-overview)
        *   [Bar Mark Properties](/vega-lite/docs/bar.html#properties)
        *   [Examples](/vega-lite/docs/bar.html#examples)
        *   [Bar Config](/vega-lite/docs/bar.html#config)
    *   [Box Plot](/vega-lite/docs/boxplot.html)
        *   [Documentation Overview](/vega-lite/docs/boxplot.html#documentation-overview)
        *   [Box Plot Mark Properties](/vega-lite/docs/boxplot.html#properties)
        *   [Types of Box Plot](/vega-lite/docs/boxplot.html#boxplot-types)
        *   [Dimension & Orientation](/vega-lite/docs/boxplot.html#dims-orient)
        *   [The Parts of Box Plots](/vega-lite/docs/boxplot.html#parts)
        *   [Color, Size, and Opacity Encoding Channels](/vega-lite/docs/boxplot.html#color-size-and-opacity-encoding-channels)
        *   [Tooltip Encoding Channels](/vega-lite/docs/boxplot.html#tooltip-encoding-channels)
        *   [Mark Config](/vega-lite/docs/boxplot.html#config)
        *   [Box Plot with Pre-Calculated Summaries](/vega-lite/docs/boxplot.html#box-plot-with-pre-calculated-summaries)
    *   [Circle](/vega-lite/docs/circle.html)
        *   [Circle Mark Properties](/vega-lite/docs/circle.html#properties)
        *   [Examples](/vega-lite/docs/circle.html#examples)
        *   [Circle Config](/vega-lite/docs/circle.html#config)
    *   [Error Band](/vega-lite/docs/errorband.html)
        *   [Documentation Overview](/vega-lite/docs/errorband.html#documentation-overview)
        *   [Error Band Mark Properties](/vega-lite/docs/errorband.html#properties)
        *   [Comparing the usage of Error Band to the usage of Error Bar](/vega-lite/docs/errorband.html#compare-to-errorbar)
        *   [Using Error Band to Aggregate Raw Data](/vega-lite/docs/errorband.html#raw-usage)
        *   [Using Error Band to Visualize Aggregated Data](/vega-lite/docs/errorband.html#pre-aggregated-usage)
        *   [Dimension](/vega-lite/docs/errorband.html#dimension)
        *   [The Parts of Error Band](/vega-lite/docs/errorband.html#parts)
        *   [Color, and Opacity Encoding Channels](/vega-lite/docs/errorband.html#color-and-opacity-encoding-channels)
        *   [Tooltip Encoding Channels](/vega-lite/docs/errorband.html#config)
        *   [Mark Config](/vega-lite/docs/errorband.html#mark-config)
    *   [Error Bar](/vega-lite/docs/errorbar.html)
        *   [Documentation Overview](/vega-lite/docs/errorbar.html#documentation-overview)
        *   [Error Bar Mark Properties](/vega-lite/docs/errorbar.html#properties)
        *   [Using Error Bars to Aggregate Raw Data](/vega-lite/docs/errorbar.html#raw-usage)
        *   [Using Error Bars to Visualize Aggregated Data](/vega-lite/docs/errorbar.html#pre-aggregated-usage)
        *   [Dimension & Orientation](/vega-lite/docs/errorbar.html#dimension--orientation)
        *   [The Parts of Error Bars](/vega-lite/docs/errorbar.html#parts)
        *   [Color, and Opacity Encoding Channels](/vega-lite/docs/errorbar.html#color-and-opacity-encoding-channels)
        *   [Tooltip Encoding Channels](/vega-lite/docs/errorbar.html#tooltip-encoding-channels)
        *   [Mark Config](/vega-lite/docs/errorbar.html#config)
    *   [Geoshape](/vega-lite/docs/geoshape.html)
        *   [Geoshape Config](/vega-lite/docs/geoshape.html#config)
    *   [Image](/vega-lite/docs/image.html)
        *   [Documentation Overview](/vega-lite/docs/image.html#documentation-overview)
        *   [Image Mark Properties](/vega-lite/docs/image.html#properties)
        *   [Examples](/vega-lite/docs/image.html#examples)
        *   [Image Config](/vega-lite/docs/image.html#image-config)
    *   [Line](/vega-lite/docs/line.html)
        *   [Documentation Overview](/vega-lite/docs/line.html#documentation-overview)
        *   [Line Mark Properties](/vega-lite/docs/line.html#properties)
        *   [Examples](/vega-lite/docs/line.html#examples)
        *   [Line Config](/vega-lite/docs/line.html#config)
    *   [Point](/vega-lite/docs/point.html)
        *   [Documentation Overview](/vega-lite/docs/point.html#documentation-overview)
        *   [Point Mark Properties](/vega-lite/docs/point.html#properties)
        *   [Examples](/vega-lite/docs/point.html#examples)
        *   [Point Config](/vega-lite/docs/point.html#config)
    *   [Rect](/vega-lite/docs/rect.html)
        *   [Documentation Overview](/vega-lite/docs/rect.html#documentation-overview)
        *   [Rect Mark Properties](/vega-lite/docs/rect.html#properties)
        *   [Examples](/vega-lite/docs/rect.html#examples)
        *   [Rect Config](/vega-lite/docs/rect.html#config)
    *   [Rule](/vega-lite/docs/rule.html)
        *   [Documentation Overview](/vega-lite/docs/rule.html#documentation-overview)
        *   [Rule Mark Properties](/vega-lite/docs/rule.html#properties)
        *   [Examples](/vega-lite/docs/rule.html#examples)
        *   [Rule Config](/vega-lite/docs/rule.html#config)
    *   [Square](/vega-lite/docs/square.html)
        *   [Square Mark Properties](/vega-lite/docs/square.html#properties)
        *   [Example: Scatterplot with Square](/vega-lite/docs/square.html#example-scatterplot-with-square)
        *   [Square Config](/vega-lite/docs/square.html#config)
    *   [Text](/vega-lite/docs/text.html)
        *   [Documentation Overview](/vega-lite/docs/text.html#documentation-overview)
        *   [Text Mark Properties](/vega-lite/docs/text.html#properties)
        *   [Examples](/vega-lite/docs/text.html#examples)
        *   [Text Config](/vega-lite/docs/text.html#config)
    *   [Tick](/vega-lite/docs/tick.html)
        *   [Documentation Overview](/vega-lite/docs/tick.html#documentation-overview)
        *   [Tick Mark Properties](/vega-lite/docs/tick.html#properties)
        *   [Examples](/vega-lite/docs/tick.html#examples)
        *   [Tick Config](/vega-lite/docs/tick.html#config)
    *   [Trail](/vega-lite/docs/trail.html)
        *   [Documentation Overview](/vega-lite/docs/trail.html#documentation-overview)
        *   [Trail Mark Properties](/vega-lite/docs/trail.html#properties)
        *   [Examples](/vega-lite/docs/trail.html#examples)
        *   [Trail Config](/vega-lite/docs/trail.html#config)
*   [Encoding](/vega-lite/docs/encoding.html)
    *   [Encoding Channels](/vega-lite/docs/encoding.html#channels)
    *   [Channel Definition](/vega-lite/docs/encoding.html#channel-definition)
    *   [Position Channels](/vega-lite/docs/encoding.html#position)
    *   [Position Offset Channels](/vega-lite/docs/encoding.html#position-offset)
    *   [Polar Position Channels](/vega-lite/docs/encoding.html#polar)
    *   [Geographic Position Channels](/vega-lite/docs/encoding.html#geo)
    *   [Mark Property Channels](/vega-lite/docs/encoding.html#mark-prop)
    *   [Text and Tooltip Channels](/vega-lite/docs/encoding.html#text)
    *   [Hyperlink Channel](/vega-lite/docs/encoding.html#href)
    *   [Description Channel](/vega-lite/docs/encoding.html#description)
    *   [Level of Detail Channel](/vega-lite/docs/encoding.html#detail)
    *   [Key Channel](/vega-lite/docs/encoding.html#key)
    *   [Order Channel](/vega-lite/docs/encoding.html#order)
    *   [Facet Channels](/vega-lite/docs/encoding.html#facet)
    *   [Aggregate](/vega-lite/docs/aggregate.html)
        *   [Documentation Overview](/vega-lite/docs/aggregate.html#documentation-overview)
        *   [Aggregate in Encoding Field Definition](/vega-lite/docs/aggregate.html#encoding)
        *   [Aggregate Transform](/vega-lite/docs/aggregate.html#transform)
        *   [Supported Aggregation Operations](/vega-lite/docs/aggregate.html#ops)
        *   [Argmin / Argmax](/vega-lite/docs/aggregate.html#argmax)
    *   [Axis](/vega-lite/docs/axis.html)
        *   [Documentation Overview](/vega-lite/docs/axis.html#documentation-overview)
        *   [Axis Properties](/vega-lite/docs/axis.html#axis-properties)
        *   [Axis Config](/vega-lite/docs/axis.html#config)
    *   [Band Position](/vega-lite/docs/bandposition.html)
        *   [Examples](/vega-lite/docs/bandposition.html#examples)
    *   [Bin](/vega-lite/docs/bin.html)
        *   [Documentation Overview](/vega-lite/docs/bin.html#documentation-overview)
        *   [Binning in Encoding Field Definition](/vega-lite/docs/bin.html#encoding)
        *   [Bin Transform](/vega-lite/docs/bin.html#transform)
        *   [Bin Parameters](/vega-lite/docs/bin.html#bin-parameters)
        *   [Ordinal Bin](/vega-lite/docs/bin.html#ordinal-bin)
    *   [Condition](/vega-lite/docs/condition.html)
        *   [Conditional Field Definition](/vega-lite/docs/condition.html#field)
        *   [Conditional Value Definition](/vega-lite/docs/condition.html#value)
    *   [Datum](/vega-lite/docs/datum.html)
        *   [Examples](/vega-lite/docs/datum.html#examples)
    *   [Field](/vega-lite/docs/field.html)
    *   [Format](/vega-lite/docs/format.html)
        *   [Formatting Text Marks and Tooltips](/vega-lite/docs/format.html#formatting-text-marks-and-tooltips)
        *   [Formatting Axis, Legend, and Header Labels](/vega-lite/docs/format.html#formatting-axis-legend-and-header-labels)
    *   [Header](/vega-lite/docs/header.html)
        *   [Documentation Overview](/vega-lite/docs/header.html#documentation-overview)
        *   [Header Properties](/vega-lite/docs/header.html#header-properties)
        *   [Header Config](/vega-lite/docs/header.html#config)
    *   [Impute](/vega-lite/docs/impute.html)
        *   [Documentation Overview](/vega-lite/docs/impute.html#documentation-overview)
        *   [Impute in Encoding Field Definition](/vega-lite/docs/impute.html#encoding)
        *   [Impute Transform](/vega-lite/docs/impute.html#transform)
    *   [Legend](/vega-lite/docs/legend.html)
        *   [Legend Types](/vega-lite/docs/legend.html#legend-types)
        *   [Combined Legend](/vega-lite/docs/legend.html#combined-legend)
        *   [Legend Properties](/vega-lite/docs/legend.html#legend-properties)
        *   [Legend Config](/vega-lite/docs/legend.html#config)
    *   [Scale](/vega-lite/docs/scale.html)
        *   [Documentation Overview](/vega-lite/docs/scale.html#documentation-overview)
        *   [Scale Types](/vega-lite/docs/scale.html#type)
        *   [Scale Domains](/vega-lite/docs/scale.html#domain)
        *   [Scale Ranges](/vega-lite/docs/scale.html#range)
        *   [Common Scale Properties](/vega-lite/docs/scale.html#continuous)
        *   [Continuous Scales](/vega-lite/docs/scale.html#continuous-scales)
        *   [Discrete Scales](/vega-lite/docs/scale.html#discrete)
        *   [Discretizing Scales](/vega-lite/docs/scale.html#discretizing)
        *   [Disabling Scale](/vega-lite/docs/scale.html#disable)
        *   [Configuration](/vega-lite/docs/scale.html#config)
    *   [Stack](/vega-lite/docs/stack.html)
        *   [Documentation Overview](/vega-lite/docs/stack.html#documentation-overview)
        *   [Stack in Encoding Field Definition](/vega-lite/docs/stack.html#encoding)
        *   [Stack Transform](/vega-lite/docs/stack.html#transform)
    *   [Sort](/vega-lite/docs/sort.html)
        *   [Documentation Overview](/vega-lite/docs/sort.html#documentation-overview)
        *   [Sorting Continuous Fields](/vega-lite/docs/sort.html#sorting-continuous-fields)
        *   [Sorting Discrete Fields](/vega-lite/docs/sort.html#sorting-discrete-fields)
    *   [Time Unit](/vega-lite/docs/timeunit.html)
        *   [Documentation Overview](/vega-lite/docs/timeunit.html#documentation-overview)
        *   [Time Unit in Encoding Field Definition](/vega-lite/docs/timeunit.html#encoding)
        *   [Time Unit Transform](/vega-lite/docs/timeunit.html#transform)
        *   [UTC time](/vega-lite/docs/timeunit.html#utc)
        *   [Time Unit Parameters](/vega-lite/docs/timeunit.html#params)
    *   [Type](/vega-lite/docs/type.html)
        *   [Quantitative](/vega-lite/docs/type.html#quantitative)
        *   [Temporal](/vega-lite/docs/type.html#temporal)
        *   [Ordinal](/vega-lite/docs/type.html#ordinal)
        *   [Nominal](/vega-lite/docs/type.html#nominal)
        *   [GeoJSON](/vega-lite/docs/type.html#geojson)
    *   [Value](/vega-lite/docs/value.html)
*   [Projection](/vega-lite/docs/projection.html)
    *   [Documentation Overview](/vega-lite/docs/projection.html#documentation-overview)
    *   [Projection Properties](/vega-lite/docs/projection.html#projection-properties)
    *   [Projection Types](/vega-lite/docs/projection.html#projection-types)
    *   [Projection Configuration](/vega-lite/docs/projection.html#config)
*   [View Composition](/vega-lite/docs/composition.html)
    *   [Documentation Overview](/vega-lite/docs/composition.html#documentation-overview)
    *   [Faceting](/vega-lite/docs/composition.html#faceting)
    *   [Layering](/vega-lite/docs/composition.html#layering)
    *   [Concatenation](/vega-lite/docs/composition.html#concatenation)
    *   [Repeating](/vega-lite/docs/composition.html#repeating)
    *   [Resolution](/vega-lite/docs/composition.html#resolution)
    *   [Facet](/vega-lite/docs/facet.html)
        *   [Documentation Overview](/vega-lite/docs/facet.html#documentation-overview)
        *   [Facet Operator](/vega-lite/docs/facet.html#facet-operator)
        *   [Facet, Row, and Column Encoding Channels](/vega-lite/docs/facet.html#facet-row-and-column-encoding-channels)
        *   [Resolve](/vega-lite/docs/facet.html#resolve)
        *   [Facet Configuration](/vega-lite/docs/facet.html#config)
    *   [Layer](/vega-lite/docs/layer.html)
        *   [Example](/vega-lite/docs/layer.html#example)
    *   [Concat](/vega-lite/docs/concat.html)
        *   [Documentation Overview](/vega-lite/docs/concat.html#documentation-overview)
        *   [Horizontal Concatenation](/vega-lite/docs/concat.html#hconcat)
        *   [Vertical Concatenation](/vega-lite/docs/concat.html#vconcat)
        *   [General (Wrappable) Concatenation](/vega-lite/docs/concat.html#concat)
        *   [Resolve](/vega-lite/docs/concat.html#resolve)
        *   [Concat Configuration](/vega-lite/docs/concat.html#config)
    *   [Repeat](/vega-lite/docs/repeat.html)
        *   [Documentation Overview](/vega-lite/docs/repeat.html#documentation-overview)
        *   [Repeat Operator](/vega-lite/docs/repeat.html#repeat-operator)
        *   [Row/Column/Layer Repeat Mapping](/vega-lite/docs/repeat.html#repeat-mapping)
        *   [Examples](/vega-lite/docs/repeat.html#examples)
        *   [Resolve](/vega-lite/docs/repeat.html#resolve)
        *   [Repeat Configuration](/vega-lite/docs/repeat.html#config)
    *   [Resolve](/vega-lite/docs/resolve.html)
        *   [Example](/vega-lite/docs/resolve.html#example)
*   [Parameter](/vega-lite/docs/parameter.html)
    *   [Documentation Overview](/vega-lite/docs/parameter.html#documentation-overview)
    *   [Defining a Parameter](/vega-lite/docs/parameter.html#defining-a-parameter)
    *   [Using Parameters](/vega-lite/docs/parameter.html#using-parameters)
    *   [Selection Configuration](/vega-lite/docs/parameter.html#config)
    *   [Value](/vega-lite/docs/param-value.html)
        *   [Examples](/vega-lite/docs/param-value.html#examples)
    *   [Expr](/vega-lite/docs/parameter.html)
        *   [Documentation Overview](/vega-lite/docs/parameter.html#documentation-overview)
        *   [Defining a Parameter](/vega-lite/docs/parameter.html#defining-a-parameter)
        *   [Using Parameters](/vega-lite/docs/parameter.html#using-parameters)
        *   [Selection Configuration](/vega-lite/docs/parameter.html#config)
    *   [Bind](/vega-lite/docs/bind.html)
        *   [Input Element Binding](/vega-lite/docs/bind.html#input-element-binding)
        *   [Legend Binding](/vega-lite/docs/bind.html#legend-binding)
        *   [Scale Binding](/vega-lite/docs/bind.html#scale-binding)
    *   [Select](/vega-lite/docs/selection.html)
        *   [Documentation Overview](/vega-lite/docs/selection.html#documentation-overview)
        *   [Common Selection Properties](/vega-lite/docs/selection.html#selection-props)
        *   [Point Selection Properties](/vega-lite/docs/selection.html#point)
        *   [Interval Selection Properties](/vega-lite/docs/selection.html#interval)
*   [Config](/vega-lite/docs/config.html)
    *   [Top-level Configuration](/vega-lite/docs/config.html#top-level-config)
    *   [Format Configuration](/vega-lite/docs/config.html#format)
    *   [Guide Configurations](/vega-lite/docs/config.html#axis-config)
    *   [Mark Configurations](/vega-lite/docs/config.html#mark-config)
    *   [Style Configuration](/vega-lite/docs/config.html#style-configuration)
    *   [Scale and Scale Range Configuration](/vega-lite/docs/config.html#scale-config)
    *   [Projection Configuration](/vega-lite/docs/config.html#projection-config)
    *   [Selection Configuration](/vega-lite/docs/config.html#selection-config)
    *   [Title Configuration](/vega-lite/docs/config.html#title-config)
    *   [View & View Composition Configuration](/vega-lite/docs/config.html#view-config)
    *   [Locale Configuration](/vega-lite/docs/config.html#aria-config)
    *   [ARIA Configuration](/vega-lite/docs/config.html#aria-configuration)
*   [Property Types](/vega-lite/docs/types.html)
    *   [Documentation Overview](/vega-lite/docs/types.html#documentation-overview)
    *   [Primitive Types](/vega-lite/docs/types.html#primitive-types)
    *   [Special Object Types](/vega-lite/docs/types.html#special-object-types)
    *   [Date Time](/vega-lite/docs/datetime.html)
    *   [Gradient](/vega-lite/docs/gradient.html)
        *   [Linear Gradient](/vega-lite/docs/gradient.html#linear-gradient)
        *   [Radial Gradient](/vega-lite/docs/gradient.html#radial-gradient)
        *   [Gradient Stop](/vega-lite/docs/gradient.html#gradient-stop)
    *   [Predicate](/vega-lite/docs/predicate.html)
        *   [Field Predicate](/vega-lite/docs/predicate.html#field-predicate)
        *   [Parameter Predicate](/vega-lite/docs/predicate.html#selection-predicate)
        *   [Predicate Composition](/vega-lite/docs/predicate.html#composition)
*   [Tooltip](/vega-lite/docs/tooltip.html)
    *   [Documentation Overview](/vega-lite/docs/tooltip.html#documentation-overview)
    *   [Tooltip Based on Encoding](/vega-lite/docs/tooltip.html#encoding)
    *   [Tooltip Based on Underlying Data Point](/vega-lite/docs/tooltip.html#data)
    *   [Tooltip channel](/vega-lite/docs/tooltip.html#channel)
    *   [Tooltip image](/vega-lite/docs/tooltip.html#tooltip-image)
    *   [Disable tooltips](/vega-lite/docs/tooltip.html#disable-tooltips)
    *   [Vega Tooltip plugin](/vega-lite/docs/tooltip.html#plugin)
*   [Invalid Data](/vega-lite/docs/invalid-data.html)
    *   [Documentation Overview](/vega-lite/docs/invalid-data.html#documentation-overview)
    *   [Mark Invalid Mode](/vega-lite/docs/invalid-data.html#mark-invalid-mode)
    *   [Scale Output for Invalid Values](/vega-lite/docs/invalid-data.html#scale-output-for-invalid-values)
    *   [Other solutions](/vega-lite/docs/invalid-data.html#other-solutions)

## Vega-Lite View Specification

Source URL: https://vega.github.io/vega-lite/docs/spec.html

[Edit this page](https://github.com/vega/vega-lite/edit/next/site/docs/spec.md)

Vega-Lite specifications are JSON objects that describe a diverse range of interactive visualizations. The simplest form of specification is a specification of a [single view](#single), which describes a view that uses a single [mark type](mark.html) to visualize the data. Besides using a single view specification as a standalone visualization, Vega-Lite also provides operators for composing multiple view specifications into a layered or multi-view specification. These operators include [`layer`](layer.html), [`facet`](facet.html), [`concat`](concat.html), and [`repeat`](repeat.html).

## Documentation Overview

*   [Common Properties of Specifications](#common)
*   [Top-Level Specifications](#top-level)
*   [Single View Specifications](#single)
    *   [View Background](#view-background)
        *   [Example: Background](#example-background)
*   [Layered and Multi-view Specifications](#layered-and-multi-view-specifications)
*   [View Configuration](#config)

## Common Properties of Specifications

All view specifications in Vega-Lite can contain the following properties:

Property

Type

Description

name

String

Name of the visualization for later reference.

description

String

Description of this mark for commenting purpose.

title

[Text](types.html#text) | [TitleParams](title.html#params)

Title for the plot.

data

[Data](data.html) | Null

**_Required._** An object describing the data source. Set to `null` to ignore the parent’s data source. If no data is set, it is derived from the parent.

transform

[Transform](transform.html)\[\]

An array of data transformations such as filter and new field calculation.

params

TopLevelParameter\[\]

An array of parameters that may either be simple variables, or more complex selections that map user input to data queries.

In addition, all view composition specifications ([`layer`](layer.html), [`facet`](facet.html), [`concat`](concat.html), and [`repeat`](repeat.html)) can have the [`resolve` property for scale, axes, and legend resolution](resolve.html):

Property

Type

Description

resolve

[Resolve](resolve.html)

Scale, axis, and legend resolutions for view composition specifications.

Finally, all view layout composition ([`facet`](facet.html), [`concat`](concat.html), and [`repeat`](repeat.html)) can have the following layout properties:

Property

Type

Description

align

String | Object

The alignment to apply to grid rows and columns. The supported string values are `"all"`, `"each"`, and `"none"`.

*   For `"none"`, a flow layout will be used, in which adjacent subviews are simply placed one after the other.
*   For `"each"`, subviews will be aligned into a clean grid structure, but each row or column may be of variable size.
*   For `"all"`, subviews will be aligned and each row or column will be sized identically based on the maximum observed size. String values for this property will be applied to both grid rows and columns.

Alternatively, an object value of the form `{"row": string, "column": string}` can be used to supply different alignments for rows and columns.

**Default value:** `"all"`.

bounds

String

The bounds calculation method to use for determining the extent of a sub-plot. One of `full` (the default) or `flush`.

*   If set to `full`, the entire calculated bounds (including axes, title, and legend) will be used.
*   If set to `flush`, only the specified width and height values for the sub-view will be used. The `flush` setting can be useful when attempting to place sub-plots without axes or legends into a uniform grid structure.

**Default value:** `"full"`

center

Boolean | Object

Boolean flag indicating if subviews should be centered relative to their respective rows or columns.

An object value of the form `{"row": boolean, "column": boolean}` can be used to supply different centering values for rows and columns.

**Default value:** `false`

spacing

Number | Object

The spacing in pixels between sub-views of the composition operator. An object of the form `{"row": number, "column": number}` can be used to set different spacing values for rows and columns.

**Default value**: Depends on `"spacing"` property of [the view composition configuration](https://vega.github.io/vega-lite/docs/config.html#view-config) (`20` by default)

## Top-Level Specifications

In addition to the [common properties](#common), any kind of top-level specifications (including a standalone single view specification as well as layered and multi-view specifications) can contain the following properties:

Property

Type

Description

$schema

String

URL to [JSON schema](http://json-schema.org/) for a Vega-Lite specification. Unless you have a reason to change this, use `https://vega.github.io/schema/vega-lite/v6.json`. Setting the `$schema` property allows automatic validation and autocomplete in editors that support JSON schema.

background

[Color](types.html#color) | [ExprRef](types.html#exprref)

CSS color property to use as the background of the entire view.

**Default value:** `"white"`

padding

Number | Object | [ExprRef](types.html#exprref)

The default visualization padding, in pixels, from the edge of the visualization canvas to the data rectangle. If a number, specifies padding for all sides. If an object, the value should have the format `{"left": 5, "top": 5, "right": 5, "bottom": 5}` to specify padding for each side of the visualization.

**Default value**: `5`

autosize

String | [AutoSizeParams](size.html#autosize)

How the visualization size should be determined. If a string, should be one of `"pad"`, `"fit"` or `"none"`. Object values can additionally specify parameters for content sizing and automatic resizing.

**Default value**: `pad`

config

[Config](config.html)

Vega-Lite configuration object. This property can only be defined at the top-level of a specification.

usermeta

Object

Optional metadata that will be passed to Vega. This object is completely ignored by Vega and Vega-Lite and can be used for custom metadata.

## Single View Specifications

```js
{
  // Properties for top-level specification (e.g., standalone single view specifications)
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "background": ...,
  "padding": ...,
  "autosize": ...,
  "config": ...,
  "usermeta": ...,

  // Properties for any specifications
  "title": ...,
  "name": ...,
  "description": ...,
  "data": ...,
  "transform": ...,

  // Properties for any single view specifications
  "width": ...,
  "height": ...,
  "mark": ...,
  "encoding": {
    "x": {
      "field": ...,
      "type": ...,
      ...
    },
    "y": ...,
    "color": ...,
    ...
  }
}
```

A single view specification describes a graphical [`mark`](mark.html) type (e.g., `point`s or `bar`s) and its [`encoding`](encoding.html), or the mapping between data values and properties of the mark. By simply providing the mark type and the encoding mapping, Vega-Lite automatically produces other visualization components including [axes](axis.html), [legends](legend.html), and [scales](scale.html). Unless explicitly specified, Vega-Lite determines properties of these components based on a set of carefully designed rules. This approach allows Vega-Lite specifications to be succinct and expressive, but also enables customization.

As it is designed for analysis, Vega-Lite also supports data transformation such as [aggregation](aggregate.html), [binning](bin.html), [time unit conversion](timeunit.html), [filtering](transform.html), and [sorting](sort.html).

To summarize, a single-view specification in Vega-Lite can have the following properties (in addition to [common properties of a specification](#common)):

Property

Type

Description

mark

[Mark](mark.html)

**_Required._** A string describing the mark type (one of `"bar"`, `"circle"`, `"square"`, `"tick"`, `"line"`, `"area"`, `"point"`, `"rule"`, `"geoshape"`, and `"text"`) or a [mark definition object](https://vega.github.io/vega-lite/docs/mark.html#mark-def).

encoding

[Encoding](encoding.html)

A key-value mapping between encoding channels and definition of fields.

width

Number | String | Object

The width of a visualization.

*   For a plot with a continuous x-field, width should be a number.
*   For a plot with either a discrete x-field or no x-field, width can be either a number indicating a fixed width or an object in the form of `{step: number}` defining the width per discrete step. (No x-field is equivalent to having one discrete step.)
*   To enable responsive sizing on width, it should be set to `"container"`.

**Default value:** Based on `config.view.continuousWidth` for a plot with a continuous x-field and `config.view.discreteWidth` otherwise.

**Note:** For plots with [`row` and `column` channels](https://vega.github.io/vega-lite/docs/encoding.html#facet), this represents the width of a single view and the `"container"` option cannot be used.

**See also:** [`width`](https://vega.github.io/vega-lite/docs/size.html) documentation.

height

Number | String | Object

The height of a visualization.

*   For a plot with a continuous y-field, height should be a number.
*   For a plot with either a discrete y-field or no y-field, height can be either a number indicating a fixed height or an object in the form of `{step: number}` defining the height per discrete step. (No y-field is equivalent to having one discrete step.)
*   To enable responsive sizing on height, it should be set to `"container"`.

**Default value:** Based on `config.view.continuousHeight` for a plot with a continuous y-field and `config.view.discreteHeight` otherwise.

**Note:** For plots with [`row` and `column` channels](https://vega.github.io/vega-lite/docs/encoding.html#facet), this represents the height of a single view and the `"container"` option cannot be used.

**See also:** [`height`](https://vega.github.io/vega-lite/docs/size.html) documentation.

view

[ViewBackground](spec.html#view-background)

An object defining the view background’s fill and stroke.

**Default value:** none (transparent)

projection

[Projection](projection.html)

An object defining properties of geographic projection, which will be applied to `shape` path for `"geoshape"` marks and to `latitude` and `"longitude"` channels for other marks.

### View Background

The `background` property of a _top-level_ view specification defines the background of the whole visualization canvas. Meanwhile, the `view` property of a single-view or [layer](layer.html) specification can define the background of the view with the following properties:

Property

Type

Description

style

String | String\[\]

A string or array of strings indicating the name of custom styles to apply to the view background. A style is a named collection of mark property defaults defined within the [style configuration](https://vega.github.io/vega-lite/docs/mark.html#style-config). If style is an array, later styles will override earlier styles.

**Default value:** `"cell"` **Note:** Any specified view background properties will augment the default style.

cornerRadius

Number | [ExprRef](types.html#exprref)

The radius in pixels of rounded rectangles or arcs’ corners.

**Default value:** `0`

cursor

String

The mouse cursor used over the view. Any valid [CSS cursor type](https://developer.mozilla.org/en-US/docs/Web/CSS/cursor#Values) can be used.

fill

[Color](types.html#color) | Null | [ExprRef](types.html#exprref)

The fill color.

**Default value:** `undefined`

fillOpacity

Number | [ExprRef](types.html#exprref)

The fill opacity (value between \[0,1\]).

**Default value:** `1`

opacity

Number | [ExprRef](types.html#exprref)

The overall opacity (value between \[0,1\]).

**Default value:** `0.7` for non-aggregate plots with `point`, `tick`, `circle`, or `square` marks or layered `bar` charts and `1` otherwise.

stroke

[Color](types.html#color) | Null | [ExprRef](types.html#exprref)

The stroke color.

**Default value:** `"#ddd"`

strokeCap

String | [ExprRef](types.html#exprref)

The stroke cap for line ending style. One of `"butt"`, `"round"`, or `"square"`.

**Default value:** `"butt"`

strokeDash

Number\[\] | [ExprRef](types.html#exprref)

An array of alternating stroke, space lengths for creating dashed or dotted lines.

strokeDashOffset

Number | [ExprRef](types.html#exprref)

The offset (in pixels) into which to begin drawing with the stroke dash array.

strokeJoin

String | [ExprRef](types.html#exprref)

The stroke line join method. One of `"miter"`, `"round"` or `"bevel"`.

**Default value:** `"miter"`

strokeMiterLimit

Number | [ExprRef](types.html#exprref)

The miter limit at which to bevel a line join.

strokeOpacity

Number | [ExprRef](types.html#exprref)

The stroke opacity (value between \[0,1\]).

**Default value:** `1`

strokeWidth

Number | [ExprRef](types.html#exprref)

The stroke width, in pixels.

#### Example: Background

For example, the following plot has orange as the whole visualization background color while setting the view background to yellow.

## Layered and Multi-view Specifications

To create layered and multi-view graphics, please refer to the following pages:

*   [`layer`](layer.html)
*   [`facet`](facet.html)
*   [`concat`](concat.html)
*   [`repeat`](repeat.html)

## View Configuration

```js
// Top-level View Specification
{
  ...,
  "config": { // Configuration Object

    "view": { // - View Configuration

      // View Size
      "continuousWidth": ...,
      "continuousHeight": ...,
      "discreteWidth": ...,
      "discreteHeight": ...,
      // View Background Properties
      "fill": ...,
      "stroke": ...,
      ...
    },
    ...
  }
}
```

The style of a single view visualization can be customized by specifying the `view` property of the `config` object. The view config support all [view background properties](#view-background) except `"style"`.

In addition, the following properties of the `view` configuration determine the default width and height of single and layered views.

Property

Type

Description

continuousWidth

Number

The default width when the plot has a continuous field for x or longitude, or has arc marks.

**Default value:** `300`

continuousHeight

Number

The default height when the plot has a continuous y-field for x or latitude, or has arc marks.

**Default value:** `300`

discreteWidth

Number | Object

The default width when the plot has non-arc marks and either a discrete x-field or no x-field. The width can be either a number indicating a fixed width or an object in the form of `{step: number}` defining the width per discrete step.

**Default value:** a step size based on `config.view.step`.

discreteHeight

Number | Object

The default height when the plot has non arc marks and either a discrete y-field or no y-field. The height can be either a number indicating a fixed height or an object in the form of `{step: number}` defining the height per discrete step.

**Default value:** a step size based on `config.view.step`.

step

Number

Default step size for x-/y- discrete fields.

For example, setting the `step` property in the view config can adjust default discrete step in the plot.

**For more information about view size, please see the [size](size.html) documentation.**
