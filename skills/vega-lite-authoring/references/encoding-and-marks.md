# Vega-Lite Encoding and Marks

Purpose: Encoding channels, field definitions, mark choice, and mark options.

Source URLs:
- https://vega.github.io/vega-lite/docs/encoding.html
- https://vega.github.io/vega-lite/docs/mark.html

## Encoding

Source URL: https://vega.github.io/vega-lite/docs/encoding.html

[Edit this page](https://github.com/vega/vega-lite/edit/next/site/docs/encoding.md)

An integral part of the data visualization process is encoding data with visual properties of graphical marks. The `encoding` property of a single view specification represents the mapping between [encoding channels](#channels) (such as `x`, `y`, or `color`) and [data fields](#field-def), constant [visual values](#value-def), or constant [data values (datum)](#datum-def).

```js
// Specification of a Single View
{
  "data": ... ,
  "mark": ... ,
  "encoding": {     // Encoding
    // Position Channels
    "x": ...,
    "y": ...,
    "x2": ...,
    "y2": ...,
    "xError": ...,
    "yError": ...,
    "xError2": ...,
    "yError2": ...,

    // Polar Position Channels
    "theta": ...,
    "radius": ...,
    "theta2": ...,
    "radius2": ...,

    // Geographic Position Channels
    "longitude": ...,
    "latitude": ...,
    "longitude2": ...,
    "latitude2": ...,

    // Mark Properties Channels
    "color": ...,
    "opacity": ...,
    "fillOpacity": ...,
    "strokeOpacity": ...,
    "strokeWidth": ...,
    "strokeDash": ...,
    "size": ...,
    "angle": ...,
    "shape": ...,

    // Text and Tooltip Channels
    "text": ...,
    "tooltip": ...,

    // Hyperlink Channel
    "href": ...,

    // Description Channel
    "description": ...,

    // Level of Detail Channel
    "detail": ...,

    // Key Channel
    "key": ...,

    // Order Channel
    "order": ...,

    // Facet Channels
    "facet": ...,
    "row": ...,
    "column": ...
  },
  ...
}
```

## Encoding Channels

The keys in the `encoding` object are encoding channels. Vega-Lite supports the following groups of encoding channels

*   [Position Channels](#position): `x`, `y`, `x2`, `y2`, `xError`, `yError`, `xError2`, `yError2`
*   [Position Offset Channels](#position-offset): `xOffset`, `yOffset`
*   [Polar Position Channels](#polar): `theta`, `theta2`, `radius`, `radius2`
*   [Geographic Position Channels](#geo): `longitude`, `latitude`, `longitude2`, `latitude2`
*   [Mark Property Channels](#mark-prop): `angle`, `color` (and `fill` / `stroke`), `opacity`, `fillOpacity`, `strokeOpacity`, `shape`, `size`, `strokeDash`, `strokeWidth`
*   [Text and Tooltip Channels](#text): `text`, `tooltip`
*   [Hyperlink Channel](#href): `href`
*   [Description Channel](#description): `description`
*   [Level of Detail Channel](#detail): `detail`
*   [Key Channel](#key): `key`
*   [Order Channel](#order): `order`
*   [Facet Channels](#facet): `facet`, `row`, `column`

## Channel Definition

Each channel definition object must be one of the following:

*   [Field definition](#field-def), which describes the data field encoded by the channel.
*   [Value definition](#value-def), which describes an encoded constant visual value.
*   [Datum definition](#datum-def), which describes a constant data value encoded via a scale.

### Field Definition

```js
// Specification of a Single View
{
  ...,
  "encoding": {     // Encoding
    ...: {
      "field": ...,
      "type": ...,
      ...
    },
    ...
  },
  ...
}
```

To encode a particular field in the data set with an encoding channel, the channel’s field definition must describe the [`field`](field.html) name and its data [`type`](type.html). To facilitate data exploration, Vega-Lite also provides inline field transforms ([`aggregate`](aggregate.html), [`bin`](bin.html), [`sort`](sort.html), [`stack`](stack.html), and [`timeUnit`](timeunit.html)) as a part of a field definition in addition to the top-level [`transform`](transform.html).

All field definitions support the following properties:

Property

Type

Description

field

[Field](field.html)

**Required.** A string defining the name of the field from which to pull a data value or an object defining iterated values from the [`repeat`](https://vega.github.io/vega-lite/docs/repeat.html) operator.

**See also:** [`field`](https://vega.github.io/vega-lite/docs/field.html) documentation.

**Notes:** 1) Dots (`.`) and brackets (`[` and `]`) can be used to access nested objects (e.g., `"field": "foo.bar"` and `"field": "foo['bar']"`). If field names contain dots or brackets but are not nested, you can use `\\` to escape dots and brackets (e.g., `"a\\.b"` and `"a\\[0\\]"`). See more details about escaping in the [field documentation](https://vega.github.io/vega-lite/docs/field.html). 2) `field` is not required if `aggregate` is `count`.

type

String

The type of measurement (`"quantitative"`, `"temporal"`, `"ordinal"`, or `"nominal"`) for the encoded field or constant value (`datum`). It can also be a `"geojson"` type for encoding [‘geoshape’](https://vega.github.io/vega-lite/docs/geoshape.html).

Vega-Lite automatically infers data types in many cases as discussed below. However, type is required for a field if: (1) the field is not nominal and the field encoding has no specified `aggregate` (except `argmin` and `argmax`), `bin`, scale type, custom `sort` order, nor `timeUnit` or (2) if you wish to use an ordinal scale for a field with `bin` or `timeUnit`.

**Default value:**

1) For a data `field`, `"nominal"` is the default data type unless the field encoding has `aggregate`, `channel`, `bin`, scale type, `sort`, or `timeUnit` that satisfies the following criteria:

*   `"quantitative"` is the default type if (1) the encoded field contains `bin` or `aggregate` except `"argmin"` and `"argmax"`, (2) the encoding channel is `latitude` or `longitude` channel or (3) if the specified scale type is [a quantitative scale](https://vega.github.io/vega-lite/docs/scale.html#type).
*   `"temporal"` is the default type if (1) the encoded field contains `timeUnit` or (2) the specified scale type is a time or utc scale
*   `"ordinal"` is the default type if (1) the encoded field contains a [custom `sort` order](https://vega.github.io/vega-lite/docs/sort.html#specifying-custom-sort-order), (2) the specified scale type is an ordinal/point/band scale, or (3) the encoding channel is `order`.

2) For a constant value in data domain (`datum`):

*   `"quantitative"` if the datum is a number
*   `"nominal"` if the datum is a string
*   `"temporal"` if the datum is [a date time object](https://vega.github.io/vega-lite/docs/datetime.html)

**Note:**

*   Data `type` describes the semantics of the data rather than the primitive data types (number, string, etc.). The same primitive data type can have different types of measurement. For example, numeric data can represent quantitative, ordinal, or nominal data.
*   Data values for a temporal field can be either a date-time string (e.g., `"2015-03-07 12:32:17"`, `"17:01"`, `"2015-03-16"`. `"2015"`) or a timestamp number (e.g., `1552199579097`).
*   When using with [`bin`](https://vega.github.io/vega-lite/docs/bin.html), the `type` property can be either `"quantitative"` (for using a linear bin scale) or [`"ordinal"` (for using an ordinal bin scale)](https://vega.github.io/vega-lite/docs/type.html#cast-bin).
*   When using with [`timeUnit`](https://vega.github.io/vega-lite/docs/timeunit.html), the `type` property can be either `"temporal"` (default, for using a temporal scale) or [`"ordinal"` (for using an ordinal scale)](https://vega.github.io/vega-lite/docs/type.html#cast-bin).
*   When using with [`aggregate`](https://vega.github.io/vega-lite/docs/aggregate.html), the `type` property refers to the post-aggregation data type. For example, we can calculate count `distinct` of a categorical field `"cat"` using `{"aggregate": "distinct", "field": "cat"}`. The `"type"` of the aggregate output is `"quantitative"`.
*   Secondary channels (e.g., `x2`, `y2`, `xError`, `yError`) do not have `type` as they must have exactly the same type as their primary channels (e.g., `x`, `y`).

**See also:** [`type`](https://vega.github.io/vega-lite/docs/type.html) documentation.

bin

Boolean | [BinParams](bin.html#bin-parameters) | String | Null

A flag for binning a `quantitative` field, [an object defining binning parameters](https://vega.github.io/vega-lite/docs/bin.html#bin-parameters), or indicating that the data for `x` or `y` channel are binned before they are imported into Vega-Lite (`"binned"`).

*   If `true`, default [binning parameters](https://vega.github.io/vega-lite/docs/bin.html#bin-parameters) will be applied.

*   If `"binned"`, this indicates that the data for the `x` (or `y`) channel are already binned. You can map the bin-start field to `x` (or `y`) and the bin-end field to `x2` (or `y2`). The scale and axis will be formatted similar to binning in Vega-Lite. To adjust the axis ticks based on the bin step, you can also set the axis’s [`tickMinStep`](https://vega.github.io/vega-lite/docs/axis.html#ticks) property.

**Default value:** `false`

**See also:** [`bin`](https://vega.github.io/vega-lite/docs/bin.html) documentation.

timeUnit

[TimeUnit](timeunit.html) | String | [TimeUnitParams](timeunit.html#params)

Time unit (e.g., `year`, `yearmonth`, `month`, `hours`) for a temporal field. or [a temporal field that gets casted as ordinal](https://vega.github.io/vega-lite/docs/type.html#cast).

**Default value:** `undefined` (None)

**See also:** [`timeUnit`](https://vega.github.io/vega-lite/docs/timeunit.html) documentation.

aggregate

[Aggregate](aggregate.html)

Aggregation function for the field (e.g., `"mean"`, `"sum"`, `"median"`, `"min"`, `"max"`, `"count"`).

**Default value:** `undefined` (None)

**See also:** [`aggregate`](https://vega.github.io/vega-lite/docs/aggregate.html) documentation.

band

[Any](types.html#any)

title

[Text](types.html#text) | Null

A title for the field. If `null`, the title will be removed.

**Default value:** derived from the field’s name and transformation function (`aggregate`, `bin` and `timeUnit`). If the field has an aggregate function, the function is displayed as part of the title (e.g., `"Sum of Profit"`). If the field is binned or has a time unit applied, the applied function is shown in parentheses (e.g., `"Profit (binned)"`, `"Transaction Date (year-month)"`). Otherwise, the title is simply the field name.

**Notes**:

1) You can customize the default field title format by providing the [`fieldTitle`](https://vega.github.io/vega-lite/docs/config.html#top-level-config) property in the [config](https://vega.github.io/vega-lite/docs/config.html) or [`fieldTitle` function via the `compile` function’s options](https://vega.github.io/vega-lite/usage/compile.html#field-title).

2) If both field definition’s `title` and axis, header, or legend `title` are defined, axis/header/legend title will be used.

In addition, field definitions for different encoding channels may support the following properties:

*   [`scale`](scale.html) - The function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) for [position](#position) and [mark property](#mark-prop) channels.

*   [`axis`](axis.html) - The guiding visualization to aid interpretation of scales for [position channels](#position).

*   [`legend`](legend.html) - The guiding visualization to aid interpretation of [mark property channels](#mark-prop).

*   [`format`](format.html) - The formatting pattern for text value for [text channels](#text).

*   [`stack`](stack.html) - Type of stacking offset if a [position field](#position) with continuous domain should be stacked.

*   [`sort`](sort.html) - Sort order for a field for [position](#position) and [mark property](#mark-prop) channels.

*   [`condition`](condition.html) - The conditional encoding rule for [mark property](#mark-prop) and [text](#text) channels.

To see a list of additional properties for each type of encoding channels, please see the specific sections for [position](#position), [mark property](#mark-prop), [text and tooltip](#text), [detail](#detail), [order](#order), and [facet](#facet) channels.

### Value Definition

```js
// Specification of a Single View
{
  ...,
  "encoding": {     // Encoding
    ...: {
      "value": ...
    },
    ...
  },
  ...
}
```

To map a constant visual value to an encoding channel, the channel’s value definition must describe the `value` property. (See the [`value`](value.html) page for more examples.)

### Datum Definition

```js
// Specification of a Single View
{
  ...,
  "encoding": {     // Encoding
    ...: {
      "datum": ...
    },
    ...
  },
  ...
}
```

To map a constant data value (`datum`) via a scale to an encoding channel, the channel’s value definition must describe the `datum` property. (See the [`datum`](datum.html) page for more examples.)

Property

Type

Description

datum

PrimitiveValue | [DateTime](datetime.html) | [ExprRef](types.html#exprref) | [RepeatRef](field.html#repeat-ref)

A constant value in data domain.

Similar to a field definition, datum definition of different encoding channels may support `band`, `scale`, `axis`, `legend`, `format`, or `condition` properties. However, data transforms (`aggregate`, `bin`, `timeUnit`, `sort` cannot be applied to a datum definition).

## Position Channels

`x` and `y` position channels determine the position of the marks, or width/height of horizontal/vertical `"area"` and `"bar"`. In addition, `x2` and `y2` can specify the span of ranged [`area`](area.html#ranged), [`bar`](bar.html#ranged), [`rect`](rect.html#ranged), and [`rule`](rule.html#ranged).

By default, Vega-Lite automatically generates a [scale](scale.html) and an [axis](axis.html) for each field mapped to a position channel. If unspecified, properties of scales and axes are determined based on a set of rules by the compiler. `scale` and `axis` properties of the field definition can be used to customize their properties.

Property

Type

Description

x

[PositionDef](encoding.html#position)

X coordinates of the marks, or width of horizontal `"bar"` and `"area"` without specified `x2` or `width`.

The `value` of this channel can be a number or a string `"width"` for the width of the plot.

y

[PositionDef](encoding.html#position)

Y coordinates of the marks, or height of vertical `"bar"` and `"area"` without specified `y2` or `height`.

The `value` of this channel can be a number or a string `"height"` for the height of the plot.

x2

Position2Def

X2 coordinates for ranged `"area"`, `"bar"`, `"rect"`, and `"rule"`.

The `value` of this channel can be a number or a string `"width"` for the width of the plot.

y2

Position2Def

Y2 coordinates for ranged `"area"`, `"bar"`, `"rect"`, and `"rule"`.

The `value` of this channel can be a number or a string `"height"` for the height of the plot.

### Position Field Definition and Datum Definition

In addition to the general [field definition properties](#field-def), field definitions for `x` and `y` channels may include the properties listed below. Similarly, [datum definitions](#datum-def) for `x` and `y` channels also support these properties.

Property

Type

Description

scale

[Scale](scale.html) | Null

An object defining properties of the channel’s scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels.

If `null`, the scale will be [disabled and the data value will be directly encoded](https://vega.github.io/vega-lite/docs/scale.html#disable).

**Default value:** If undefined, default [scale properties](https://vega.github.io/vega-lite/docs/scale.html) are applied.

**See also:** [`scale`](https://vega.github.io/vega-lite/docs/scale.html) documentation.

axis

[Axis](axis.html) | Null

An object defining properties of axis’s gridlines, ticks and labels. If `null`, the axis for the encoding channel will be removed.

**Default value:** If undefined, default [axis properties](https://vega.github.io/vega-lite/docs/axis.html) are applied.

**See also:** [`axis`](https://vega.github.io/vega-lite/docs/axis.html) documentation.

sort

[Sort](sort.html)

Sort order for the encoded field.

For continuous fields (quantitative or temporal), `sort` can be either `"ascending"` or `"descending"`.

For discrete fields, `sort` can be one of the following:

*   `"ascending"` or `"descending"` – for sorting by the values’ natural order in JavaScript.
*   [A string indicating an encoding channel name to sort by](https://vega.github.io/vega-lite/docs/sort.html#sort-by-encoding) (e.g., `"x"` or `"y"`) with an optional minus prefix for descending sort (e.g., `"-x"` to sort by x-field, descending). This channel string is short-form of [a sort-by-encoding definition](https://vega.github.io/vega-lite/docs/sort.html#sort-by-encoding). For example, `"sort": "-x"` is equivalent to `"sort": {"encoding": "x", "order": "descending"}`.
*   [A sort field definition](https://vega.github.io/vega-lite/docs/sort.html#sort-field) for sorting by another field.
*   [An array specifying the field values in preferred order](https://vega.github.io/vega-lite/docs/sort.html#sort-array). In this case, the sort order will obey the values in the array, followed by any unspecified values in their original order. For discrete time field, values in the sort array can be [date-time definition objects](types#datetime). In addition, for time units `"month"` and `"day"`, the values can be the month or day names (case insensitive) or their 3-letter initials (e.g., `"Mon"`, `"Tue"`).
*   `null` indicating no sort.

**Default value:** `"ascending"`

**Note:** `null` and sorting by another channel is not supported for `row` and `column`.

**See also:** [`sort`](https://vega.github.io/vega-lite/docs/sort.html) documentation.

impute

ImputeParams | Null

An object defining the properties of the Impute Operation to be applied. The field value of the other positional channel is taken as `key` of the `Impute` Operation. The field of the `color` channel if specified is used as `groupby` of the `Impute` Operation.

**See also:** [`impute`](https://vega.github.io/vega-lite/docs/impute.html) documentation.

stack

String | Null | Boolean

Type of stacking offset if the field should be stacked. `stack` is only applicable for `x`, `y`, `theta`, and `radius` channels with continuous domains. For example, `stack` of `y` can be used to customize stacking for a vertical bar chart.

`stack` can be one of the following values:

*   `"zero"` or `true`: stacking with baseline offset at zero value of the scale (for creating typical stacked [bar](https://vega.github.io/vega-lite/docs/stack.html#bar) and [area](https://vega.github.io/vega-lite/docs/stack.html#area) chart).
*   `"normalize"` - stacking with normalized domain (for creating [normalized stacked bar and area charts](https://vega.github.io/vega-lite/docs/stack.html#normalized) and pie charts [with percentage tooltip](https://vega.github.io/vega-lite/docs/arc.html#tooltip)).
    \-`"center"` - stacking with center baseline (for [streamgraph](https://vega.github.io/vega-lite/docs/stack.html#streamgraph)).
*   `null` or `false` - No-stacking. This will produce layered [bar](https://vega.github.io/vega-lite/docs/stack.html#layered-bar-chart) and area chart.

**Default value:** `zero` for plots with all of the following conditions are true: (1) the mark is `bar`, `area`, or `arc`; (2) the stacked measure channel (x or y) has a linear scale; (3) At least one of non-position channels mapped to an unaggregated field that is different from x and y. Otherwise, `null` by default.

**See also:** [`stack`](https://vega.github.io/vega-lite/docs/stack.html) documentation.

**Note:** `x2` and `y2` do not have their own definitions for `scale`, `axis`, `sort`, and `stack` since they share the same scales and axes with `x` and `y` respectively.

## Position Offset Channels

`xOffset` and `yOffset` position channels determine additional offset to the `x` or `y` position.

### Position Offset Field Definition and Datum Definition

In addition to the general [field definition properties](#field-def), field definitions for `xOffset` and `yOffset` channels may include the properties listed below. Similarly, [datum definitions](#datum-def) for `x` and `y` channels also support these properties.

Property

Type

Description

scale

[Scale](scale.html) | Null

An object defining properties of the channel’s scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels.

If `null`, the scale will be [disabled and the data value will be directly encoded](https://vega.github.io/vega-lite/docs/scale.html#disable).

**Default value:** If undefined, default [scale properties](https://vega.github.io/vega-lite/docs/scale.html) are applied.

**See also:** [`scale`](https://vega.github.io/vega-lite/docs/scale.html) documentation.

sort

[Sort](sort.html)

Sort order for the encoded field.

For continuous fields (quantitative or temporal), `sort` can be either `"ascending"` or `"descending"`.

For discrete fields, `sort` can be one of the following:

*   `"ascending"` or `"descending"` – for sorting by the values’ natural order in JavaScript.
*   [A string indicating an encoding channel name to sort by](https://vega.github.io/vega-lite/docs/sort.html#sort-by-encoding) (e.g., `"x"` or `"y"`) with an optional minus prefix for descending sort (e.g., `"-x"` to sort by x-field, descending). This channel string is short-form of [a sort-by-encoding definition](https://vega.github.io/vega-lite/docs/sort.html#sort-by-encoding). For example, `"sort": "-x"` is equivalent to `"sort": {"encoding": "x", "order": "descending"}`.
*   [A sort field definition](https://vega.github.io/vega-lite/docs/sort.html#sort-field) for sorting by another field.
*   [An array specifying the field values in preferred order](https://vega.github.io/vega-lite/docs/sort.html#sort-array). In this case, the sort order will obey the values in the array, followed by any unspecified values in their original order. For discrete time field, values in the sort array can be [date-time definition objects](types#datetime). In addition, for time units `"month"` and `"day"`, the values can be the month or day names (case insensitive) or their 3-letter initials (e.g., `"Mon"`, `"Tue"`).
*   `null` indicating no sort.

**Default value:** `"ascending"`

**Note:** `null` and sorting by another channel is not supported for `row` and `column`.

**See also:** [`sort`](https://vega.github.io/vega-lite/docs/sort.html) documentation.

### Example: Grouped Bar Chart

**Note:** Read [here](size.html#offset-step) for more details about how to set step size for offset scale.

### Example: Jittering

## Polar Position Channels

`theta` and `radius` position channels determine the position or interval on polar coordinates for `arc` and `text` marks.

Property

Type

Description

theta

[PolarDef](encoding.html#polar)

*   For arc marks, the arc length in radians if theta2 is not specified, otherwise the start arc angle. (A value of 0 indicates up or “north”, increasing values proceed clockwise.)

*   For text marks, polar coordinate angle in radians.

radius

[PolarDef](encoding.html#polar)

The outer radius in pixels of arc marks.

theta2

Position2Def

The end angle of arc marks in radians. A value of 0 indicates up or “north”, increasing values proceed clockwise.

radius2

Position2Def

The inner radius in pixels of arc marks.

### Polar Field Definition and Datum Definition

Polar field and datum definitions may include `scale`, `stack`, and `sort` properties, similar to [position field and datum definitions](#position-field-def).

## Geographic Position Channels

`longitude` and `latitude` channels can be used to encode geographic coordinate data via a [projection](projection.html). In addition, `longitude2` and `latitude2` can specify the span of geographically projected ranged [`area`](area.html#ranged), [`bar`](bar.html#ranged), [`rect`](rect.html#ranged), and [`rule`](rule.html#ranged).

Property

Type

Description

longitude

LatLongDef

Longitude position of geographically projected marks.

latitude

LatLongDef

Latitude position of geographically projected marks.

longitude2

Position2Def

Longitude-2 position for geographically projected ranged `"area"`, `"bar"`, `"rect"`, and `"rule"`.

latitude2

Position2Def

Latitude-2 position for geographically projected ranged `"area"`, `"bar"`, `"rect"`, and `"rule"`.

See [an example that uses `longitude` and `latitude` channels in a map](/vega-lite/examples/geo_circle.html) or [another example that draws line segments (`rule`s) between points in a map](/vega-lite/examples/geo_rule.html).

## Mark Property Channels

Mark properties channels map data fields to visual properties of the marks. By default, Vega-Lite automatically generates a scale and a legend for each field mapped to a mark property channel. If unspecified, properties of scales and legends are determined based on a set of rules by the compiler. `scale` and `legend` properties of the field definition can be used to customize their properties. In addition, definitions of mark property channels can include the `condition` property to specify conditional logic.

Here are the list of mark property channels:

Property

Type

Description

angle

[MarkPropDef](encoding.html#mark-prop)

Rotation angle of point and text marks.

color

[MarkPropDef](encoding.html#mark-prop)

Color of the marks – either fill or stroke color based on the `filled` property of mark definition. By default, `color` represents fill color for `"area"`, `"bar"`, `"tick"`, `"text"`, `"trail"`, `"circle"`, and `"square"` / stroke color for `"line"` and `"point"`.

**Default value:** If undefined, the default color depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#mark-config)’s `color` property.

_Note:_ 1) For fine-grained control over both fill and stroke colors of the marks, please use the `fill` and `stroke` channels. The `fill` or `stroke` encodings have higher precedence than `color`, thus may override the `color` encoding if conflicting encodings are specified. 2) See the scale documentation for more information about customizing [color scheme](https://vega.github.io/vega-lite/docs/scale.html#scheme).

fill

[MarkPropDef](encoding.html#mark-prop)

Fill color of the marks. **Default value:** If undefined, the default color depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#mark-config)’s `color` property.

_Note:_ The `fill` encoding has higher precedence than `color`, thus may override the `color` encoding if conflicting encodings are specified.

stroke

[MarkPropDef](encoding.html#mark-prop)

Stroke color of the marks. **Default value:** If undefined, the default color depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#mark-config)’s `color` property.

_Note:_ The `stroke` encoding has higher precedence than `color`, thus may override the `color` encoding if conflicting encodings are specified.

opacity

[MarkPropDef](encoding.html#mark-prop)

Opacity of the marks.

**Default value:** If undefined, the default opacity depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#mark-config)’s `opacity` property.

fillOpacity

[MarkPropDef](encoding.html#mark-prop)

Fill opacity of the marks.

**Default value:** If undefined, the default opacity depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#mark-config)’s `fillOpacity` property.

strokeOpacity

[MarkPropDef](encoding.html#mark-prop)

Stroke opacity of the marks.

**Default value:** If undefined, the default opacity depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#mark-config)’s `strokeOpacity` property.

shape

[MarkPropDef](encoding.html#mark-prop)

Shape of the mark.

1.  For `point` marks the supported values include: - plotting shapes: `"circle"`, `"square"`, `"cross"`, `"diamond"`, `"triangle-up"`, `"triangle-down"`, `"triangle-right"`, or `"triangle-left"`. - the line symbol `"stroke"` - centered directional shapes `"arrow"`, `"wedge"`, or `"triangle"` - a custom [SVG path string](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths) (For correct sizing, custom shape paths should be defined within a square bounding box with coordinates ranging from -1 to 1 along both the x and y dimensions.)

2.  For `geoshape` marks it should be a field definition of the geojson data

**Default value:** If undefined, the default shape depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#point-config)’s `shape` property. (`"circle"` if unset.)

size

[MarkPropDef](encoding.html#mark-prop)

Size of the mark.

*   For `"point"`, `"square"` and `"circle"`, – the symbol size, or pixel area of the mark.
*   For `"bar"` and `"tick"` – the bar and tick’s size.
*   For `"text"` – the text’s font size.
*   Size is unsupported for `"line"`, `"area"`, and `"rect"`. (Use `"trail"` instead of line with varying size)

strokeDash

NumericArrayMarkPropDef

Stroke dash of the marks.

**Default value:** `[1,0]` (No dash).

strokeWidth

[MarkPropDef](encoding.html#mark-prop)

Stroke width of the marks.

**Default value:** If undefined, the default stroke width depends on [mark config](https://vega.github.io/vega-lite/docs/config.html#mark-config)’s `strokeWidth` property.

### Mark Property Field Definition and Datum Definition

[Field definitions](#field-def) for mark property channels may also include the properties list below (in addition to [`field`](field.html), [`type`](type.html), [`bin`](bin.html), [`timeUnit`](timeunit.html) and [`aggregate`](aggregate.html)).

Similarly, [datum definitions](#datum-def) for mark property channels also support these properties.

Property

Type

Description

scale

[Scale](scale.html) | Null

An object defining properties of the channel’s scale, which is the function that transforms values in the data domain (numbers, dates, strings, etc) to visual values (pixels, colors, sizes) of the encoding channels.

If `null`, the scale will be [disabled and the data value will be directly encoded](https://vega.github.io/vega-lite/docs/scale.html#disable).

**Default value:** If undefined, default [scale properties](https://vega.github.io/vega-lite/docs/scale.html) are applied.

**See also:** [`scale`](https://vega.github.io/vega-lite/docs/scale.html) documentation.

legend

[Legend](legend.html) | Null

An object defining properties of the legend. If `null`, the legend for the encoding channel will be removed.

**Default value:** If undefined, default [legend properties](https://vega.github.io/vega-lite/docs/legend.html) are applied.

**See also:** [`legend`](https://vega.github.io/vega-lite/docs/legend.html) documentation.

condition

[ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

One or more value definition(s) with [a parameter or a test predicate](https://vega.github.io/vega-lite/docs/condition.html).

**Note:** A field definition’s `condition` property can only contain [conditional value definitions](https://vega.github.io/vega-lite/docs/condition.html#value) since Vega-Lite only allows at most one encoded field per encoding channel.

### Mark Property Value Definition

In addition to the constant `value`, [value definitions](#value-def) of mark properties channels can include the `condition` property to specify conditional logic.

Property

Type

Description

condition

[ConditionalFieldDef](condition.html#field) | [ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

A field definition or one or more value definition(s) with a parameter predicate.

See [the `condition`](condition.html) page for examples how to specify condition logic.

## Text and Tooltip Channels

Text and tooltip channels directly encode text values of the data fields. By default, Vega-Lite automatically determines appropriate format for quantitative and temporal values. Users can set `format` property to customize text and time format. Similar to mark property channels, definitions of text and tooltip channels can include the `condition` property to specify conditional logic.

Property

Type

Description

text

[TextFieldDef](encoding.html#text-field-def)

Text of the `text` mark.

tooltip

StringFieldDefWithCondition | StringValueDefWithCondition | StringFieldDef\[\] | Null

The tooltip text to show upon mouse hover. Specifying `tooltip` encoding overrides [the `tooltip` property in the mark definition](https://vega.github.io/vega-lite/docs/mark.html#mark-def).

See the [`tooltip`](https://vega.github.io/vega-lite/docs/tooltip.html) documentation for a detailed discussion about tooltip in Vega-Lite.

### Text and Tooltip Field Definition

In addition to the general [field definition properties](#field-def), field definitions for `text` and `tooltip` channels may also include these properties:

Property

Type

Description

format

Format

The text format specifier for formatting number and date/time in labels of guides (axes, legends, headers) and text marks.

If the format type is `"number"` (e.g., for quantitative fields), this is a D3’s [number format pattern string](https://github.com/d3/d3-format#locale_format).

If the format type is `"time"` (e.g., for temporal fields), this is either: a) D3’s [time format pattern](https://d3js.org/d3-time-format#locale_format) if you desire to set a static time format.

b) [dynamic time format specifier object](https://vega.github.io/vega-lite/docs/format.html#dynamic-time-format) if you desire to set a dynamic time format that uses different formats depending on the granularity of the input date (e.g., if the date lies on a year, month, date, hour, etc. boundary).

When used with a [custom `formatType`](https://vega.github.io/vega-lite/docs/config.html#custom-format-type), this value will be passed as `format` alongside `datum.value` to the registered function.

**Default value:** Derived from [numberFormat](https://vega.github.io/vega-lite/docs/config.html#format) config for number format and from [timeFormat](https://vega.github.io/vega-lite/docs/config.html#format) config for time format.

formatType

String

The format type for labels. One of `"number"`, `"time"`, or a [registered custom format type](https://vega.github.io/vega-lite/docs/config.html#custom-format-type).

**Default value:**

*   `"time"` for temporal fields and ordinal and nominal fields with `timeUnit`.
*   `"number"` for quantitative fields as well as ordinal and nominal fields without `timeUnit`.

condition

[ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

One or more value definition(s) with [a parameter or a test predicate](https://vega.github.io/vega-lite/docs/condition.html).

**Note:** A field definition’s `condition` property can only contain [conditional value definitions](https://vega.github.io/vega-lite/docs/condition.html#value) since Vega-Lite only allows at most one encoded field per encoding channel.

### Text and Tooltip Value Definition

In addition to the constant `value`, [value definitions](#value-def) of `text` and `tooltip` channels can include the `condition` property to specify conditional logic.

Property

Type

Description

condition

ConditionalStringFieldDef | [ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

A field definition or one or more value definition(s) with a parameter predicate.

### Multiple Field Definitions for Tooltips

Similar to [`detail`](#detail), you can use an array of field definitions. Vega-Lite will display a tooltip with multiple fields. [Vega tooltip](https://github.com/vega/vega-tooltip/) will display a table that shows the name of the field and its value. See the [tooltip](tooltip.html) page for details.

## Hyperlink Channel

By setting the `href` channel, a mark becomes a hyperlink. The specified URL is loaded upon a mouse click. When the `href` channel is specified, the [`cursor` mark property](mark.html#hyperlink) is set to `"pointer"` by default to serve as affordance for hyperlinks.

Property

Type

Description

href

StringFieldDefWithCondition | StringValueDefWithCondition

A URL to load upon mouse click.

### Hyperlink Field Definition

In addition to the general [field definition properties](#field-def), field definitions for the `href` channel can include the `condition` property to specify conditional logic.

Property

Type

Description

condition

[Any](types.html#any)

The example below shows how the href channel can be used to provide links to external resources with more details.

### Hyperlink Value Definition

In addition to the constant `value`, [value definitions](#value-def) of the `href` channel can include the `condition` property to specify conditional logic.

Property

Type

Description

condition

ConditionalStringFieldDef | [ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

A field definition or one or more value definition(s) with a parameter predicate.

## Description Channel

By setting the `description` channel, you can add a text description to the mark for ARIA accessibility (SVG output only). The `"aria-label"` attribute in the generated SVG will be set to this description.

By default, Vega-Lite generates a description based on the encoding similar to [default tooltips](/vega-lite/docs/tooltip.html#encoding). To disable automatic descriptions, set [`config.aria`](config.html#aria-config) to false. No description will be generated if [`mark.aria`](/vega-lite/docs/mark.html#general) is set to false.

Property

Type

Description

description

StringFieldDefWithCondition | StringValueDefWithCondition

A text description of this mark for ARIA accessibility (SVG output only). For SVG output the `"aria-label"` attribute will be set to this description.

### Description Field Definition

In addition to the general [field definition properties](#field-def), field definitions for the `description` channel can include these properties:

Property

Type

Description

format

Format

The text format specifier for formatting number and date/time in labels of guides (axes, legends, headers) and text marks.

If the format type is `"number"` (e.g., for quantitative fields), this is a D3’s [number format pattern string](https://github.com/d3/d3-format#locale_format).

If the format type is `"time"` (e.g., for temporal fields), this is either: a) D3’s [time format pattern](https://d3js.org/d3-time-format#locale_format) if you desire to set a static time format.

b) [dynamic time format specifier object](https://vega.github.io/vega-lite/docs/format.html#dynamic-time-format) if you desire to set a dynamic time format that uses different formats depending on the granularity of the input date (e.g., if the date lies on a year, month, date, hour, etc. boundary).

When used with a [custom `formatType`](https://vega.github.io/vega-lite/docs/config.html#custom-format-type), this value will be passed as `format` alongside `datum.value` to the registered function.

**Default value:** Derived from [numberFormat](https://vega.github.io/vega-lite/docs/config.html#format) config for number format and from [timeFormat](https://vega.github.io/vega-lite/docs/config.html#format) config for time format.

formatType

String

The format type for labels. One of `"number"`, `"time"`, or a [registered custom format type](https://vega.github.io/vega-lite/docs/config.html#custom-format-type).

**Default value:**

*   `"time"` for temporal fields and ordinal and nominal fields with `timeUnit`.
*   `"number"` for quantitative fields as well as ordinal and nominal fields without `timeUnit`.

condition

[ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

One or more value definition(s) with [a parameter or a test predicate](https://vega.github.io/vega-lite/docs/condition.html).

**Note:** A field definition’s `condition` property can only contain [conditional value definitions](https://vega.github.io/vega-lite/docs/condition.html#value) since Vega-Lite only allows at most one encoded field per encoding channel.

### Description Value Definition

In addition to the constant `value`, [value definitions](#value-def) of the `description` channel can include the `condition` property to specify conditional logic.

Property

Type

Description

condition

ConditionalStringFieldDef | [ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

A field definition or one or more value definition(s) with a parameter predicate.

## Level of Detail Channel

Grouping data is another important operation in data visualization. For line and area marks, mapping a unaggregated data field (field without `aggregate` function) to any non-[position](#position) channel will group the lines and stacked areas by the field. For [aggregated plots](aggregate.html), all unaggregated fields encoded are used as grouping fields in the aggregation (similar to fields in `GROUP BY` in SQL).

`detail` channel specify an additional grouping field (or fields) for grouping data without mapping the field(s) to any visual properties.

Property

Type

Description

detail

[FieldDef](encoding.html#field) | [FieldDef](encoding.html#field)\[\]

Additional levels of detail for grouping data in aggregate views and in line, trail, and area marks without mapping data to a specific visual channel.

#### Examples

Here is a scatterplot showing average horsepower and displacement for cars from different origins. We map `Origin` to `detail` channel to use the field as a group-by field without mapping it to visual properties of the marks.

Here is a line chart showing stock prices of 5 tech companies over time. We map `symbol` variable (stock market ticker symbol) to `detail` to use them to group lines.

Here is a ranged dot plot showing life expectancy change in the five largest countries between 1955 and 2000. We use `detail` here to group the lines such that they range only from one year to another within a country (as opposed to jumping between countries as well).

## Key Channel

The key channel can enable object constancy for transitions over dynamic data. When a visualization’s data is updated (via [Vega’s View API](https://vega.github.io/vega/docs/api/view/#data)), the key value will be used to match data elements to existing mark instances.

Property

Type

Description

key

[FieldDef](encoding.html#field)

A data field to use as a unique key for data binding. When a visualization’s data is updated, the key value will be used to match data elements to existing mark instances. Use a key channel to enable object constancy for transitions over dynamic data.

## Order Channel

`order` channel can define a data field (or a ordered list of data fields) that are used to sorts stacking order for stacked charts (see [an example in the `stack` page](stack.html#order)), the order of data points in line marks for connected scatterplots (see [an example in the `line` page](line.html#connected-scatter-plot)), and which data points are plotted on top in a chart (the “zorder”, see [an example in the gallery](/vega-lite/examples/selection_type_point_zorder.html)).

Property

Type

Description

order

[OrderFieldDef](encoding.html#order) | [OrderFieldDef](encoding.html#order)\[\] | OrderValueDef | OrderOnlyDef

Order of the marks.

*   For stacked marks, this `order` channel encodes [stack order](https://vega.github.io/vega-lite/docs/stack.html#order).
*   For line and trail marks, this `order` channel encodes order of data points in the lines. This can be useful for creating [a connected scatterplot](https://vega.github.io/vega-lite/examples/connected_scatterplot.html). Setting `order` to `{"value": null}` makes the line marks use the original order in the data sources.
*   Otherwise, this `order` channel encodes layer order of the marks.

**Note**: In aggregate plots, `order` field should be `aggregate`d to avoid creating additional aggregation grouping.

### Order Field Definition

In addition to the general [field definition properties](#field-def), field definitions for the `order` channel can include `sort`.

Property

Type

Description

sort

String

The sort order. One of `"ascending"` (default) or `"descending"`.

### Order Value Definition

In addition to the constant `value`, [value definitions](#value-def) of the `order` channel can include the `condition` property to specify conditional logic.

Property

Type

Description

condition

[ConditionalValueDef](condition.html#value) | [ConditionalValueDef](condition.html#value)\[\]

One or more value definition(s) with [a parameter or a test predicate](https://vega.github.io/vega-lite/docs/condition.html).

**Note:** A field definition’s `condition` property can only contain [conditional value definitions](https://vega.github.io/vega-lite/docs/condition.html#value) since Vega-Lite only allows at most one encoded field per encoding channel.

## Facet Channels

`facet`, `row` and `column` are special encoding channels that facets single plots into [trellis plots (or small multiples)](https://en.wikipedia.org/wiki/Small_multiple).

Property

Type

Description

facet

[FacetFieldDef](facet.html#facet-field-definition)

A field definition for the (flexible) facet of trellis plots.

If either `row` or `column` is specified, this channel will be ignored.

row

[FacetFieldDef](facet.html#facet-field-definition)

A field definition for the vertical facet of trellis plots.

column

[FacetFieldDef](facet.html#facet-field-definition)

A field definition for the horizontal facet of trellis plots.

For more information, read the [facet documentation](facet.html).

## Mark

Source URL: https://vega.github.io/vega-lite/docs/mark.html

[Edit this page](https://github.com/vega/vega-lite/edit/next/site/docs/mark/mark.md)

Marks are the basic visual building block of a visualization. They provide basic shapes whose properties (such as position, size, and color) can be used to visually encode data, either from a data field, or a constant value.

The `mark` property of a [single view specification](spec.html#single) can either be (1) a string describing a [mark type](#types) or (2) a [mark definition object](#mark-def).

```js
// Single View Specification
{
  "data": ... ,
  "mark": ... ,       // mark
  "encoding": ... ,
  ...
}
```

## Documentation Overview

*   [Mark Types](#types)
*   [Mark Definition Object](#mark-def)
    *   [General Mark Properties](#general)
    *   [Position and Offset Properties](#offset)
    *   [Color Properties](#color)
    *   [Stroke Style Properties](#stroke)
    *   [Hyperlink Properties](#hyperlink)
*   [Mark Config](#config)
*   [Mark Style Config](#style-config)
    *   [Example: Styling Labels](#example-styling-labels)

## Mark Types

Vega-Lite supports the following primitive `mark` types: [`"area"`](area.html), [`"bar"`](bar.html), [`"circle"`](circle.html), [`"line"`](line.html), [`"point"`](point.html), [`"rect"`](rect.html), [`"rule"`](rule.html), [`"square"`](square.html), [`"text"`](text.html), [`"tick"`](tick.html), and [`"geoshape"`](geoshape.html). In general, one mark instance is generated per input data element. However, line and area marks represent multiple data elements as a contiguous line or shape.

In addition to primitive marks, Vega-Lite also support composite marks, which are “macros” for complex layered graphics that contain multiple primitive marks. Supported composite mark types include [`"boxplot"`](boxplot.html), [`"errorband"`](errorband.html), [`"errorbar"`](errorbar.html).

For example, a bar chart has `mark` as a simple string `"bar"`.

## Mark Definition Object

```js
// Single View Specification
{
  ...
  "mark": {
    "type": ...,       // mark
    ...
  },
  ...
}
```

To customize properties of a mark, users can set `mark` to be a mark definition object instead of a string describing mark type. The rest of this section lists standard mark properties for primitive mark types. Additionally, some marks may have special mark properties (listed in their documentation page). For example, [point](point.html#properties) marks support `shape` and `size` properties in addition to these standard properties.

Note: If [mark property encoding channels](encoding.html#mark-prop) are specified, these mark properties will be overridden.

### General Mark Properties

Property

Type

Description

type

String

**_Required._** The mark type. This could a primitive mark type (one of `"bar"`, `"circle"`, `"square"`, `"tick"`, `"line"`, `"area"`, `"point"`, `"geoshape"`, `"rule"`, and `"text"`) or a composite mark type (`"boxplot"`, `"errorband"`, `"errorbar"`).

aria

Boolean | [ExprRef](types.html#exprref)

A boolean flag indicating if [ARIA attributes](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) should be included (SVG output only). If `false`, the “aria-hidden” attribute will be set on the output SVG element, removing the mark item from the ARIA accessibility tree.

cursor

String | [ExprRef](types.html#exprref)

The mouse cursor used over the mark. Any valid [CSS cursor type](https://developer.mozilla.org/en-US/docs/Web/CSS/cursor#Values) can be used.

description

String | [ExprRef](types.html#exprref)

A text description of the mark item for [ARIA accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) (SVG output only). If specified, this property determines the [“aria-label” attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Techniques/Using_the_aria-label_attribute).

style

String | String\[\]

A string or array of strings indicating the name of custom styles to apply to the mark. A style is a named collection of mark property defaults defined within the [style configuration](https://vega.github.io/vega-lite/docs/mark.html#style-config). If style is an array, later styles will override earlier styles. Any [mark properties](https://vega.github.io/vega-lite/docs/encoding.html#mark-prop) explicitly defined within the `encoding` will override a style default.

**Default value:** The mark’s name. For example, a bar mark will have style `"bar"` by default. **Note:** Any specified style will augment the default style. For example, a bar mark with `"style": "foo"` will receive from `config.style.bar` and `config.style.foo` (the specified style `"foo"` has higher precedence).

tooltip

Number | String | Boolean | TooltipContent | [ExprRef](types.html#exprref) | Null

The tooltip text string to show upon mouse hover or an object defining which fields should the tooltip be derived from.

*   If `tooltip` is `true` or `{"content": "encoding"}`, then all fields from `encoding` will be used.
*   If `tooltip` is `{"content": "data"}`, then all fields that appear in the highlighted data point will be used.
*   If set to `null` or `false`, then no tooltip will be used.

See the [`tooltip`](https://vega.github.io/vega-lite/docs/tooltip.html) documentation for a detailed discussion about tooltip in Vega-Lite.

**Default value:** `null`

clip

Boolean | [ExprRef](types.html#exprref)

Whether a mark be clipped to the enclosing group’s width and height.

invalid

String | Null

Invalid data mode, which defines how the marks and corresponding scales should represent invalid values (`null` and `NaN` in continuous scales _without_ defined output for invalid values).

*   `"filter"` — _Exclude_ all invalid values from the visualization’s _marks_ and _scales_. For path marks (for line, area, trail), this option will create paths that connect valid points, as if the data rows with invalid values do not exist.

*   `"break-paths-filter-domains"` — Break path marks (for line, area, trail) at invalid values. For non-path marks, this is equivalent to `"filter"`. All _scale_ domains will _exclude_ these filtered data points.

*   `"break-paths-show-domains"` — Break paths (for line, area, trail) at invalid values. Hide invalid values for non-path marks. All _scale_ domains will _include_ these filtered data points (for both path and non-path marks).

*   `"show"` or `null` — Show all data points in the marks and scale domains. Each scale will use the output for invalid values defined in `config.scale.invalid` or, if unspecified, by default invalid values will produce the same visual values as zero (if the scale includes zero) or the minimum value (if the scale does not include zero).

*   `"break-paths-show-path-domains"` (default) — This is equivalent to `"break-paths-show-domains"` for path-based marks (line/area/trail) and `"filter"` for non-path marks.

**Note**: If any channel’s scale has an output for invalid values defined in `config.scale.invalid`, all values for the scales will be considered “valid” since they can produce a reasonable output for the scales. Thus, fields for such channels will not be filtered and will not cause path breaks.

order

Null | Boolean

For line and trail marks, this `order` property can be set to `null` or `false` to make the lines use the original order in the data sources.

### Position and Offset Properties

Property

Type

Description

x

Number | String | [ExprRef](types.html#exprref)

X coordinates of the marks, or width of horizontal `"bar"` and `"area"` without specified `x2` or `width`.

The `value` of this channel can be a number or a string `"width"` for the width of the plot.

x2

Number | String | [ExprRef](types.html#exprref)

X2 coordinates for ranged `"area"`, `"bar"`, `"rect"`, and `"rule"`.

The `value` of this channel can be a number or a string `"width"` for the width of the plot.

width

Number | [ExprRef](types.html#exprref) | RelativeBandSize

Width of the marks. One of:

*   A number representing a fixed pixel width.

*   A relative band size definition. For example, `{band: 0.5}` represents half of the band.

height

Number | [ExprRef](types.html#exprref) | RelativeBandSize

Height of the marks. One of:

*   A number representing a fixed pixel height.

*   A relative band size definition. For example, `{band: 0.5}` represents half of the band

y

Number | String | [ExprRef](types.html#exprref)

Y coordinates of the marks, or height of vertical `"bar"` and `"area"` without specified `y2` or `height`.

The `value` of this channel can be a number or a string `"height"` for the height of the plot.

y2

Number | String | [ExprRef](types.html#exprref)

Y2 coordinates for ranged `"area"`, `"bar"`, `"rect"`, and `"rule"`.

The `value` of this channel can be a number or a string `"height"` for the height of the plot.

xOffset

Number | [ExprRef](types.html#exprref)

Offset for x-position.

x2Offset

Number | [ExprRef](types.html#exprref)

Offset for x2-position.

yOffset

Number | [ExprRef](types.html#exprref)

Offset for y-position.

y2Offset

Number | [ExprRef](types.html#exprref)

Offset for y2-position.

### Color Properties

Property

Type

Description

filled

Boolean

Whether the mark’s color should be used as fill color instead of stroke color.

**Default value:** `false` for all `point`, `line`, and `rule` marks as well as `geoshape` marks for [`graticule`](https://vega.github.io/vega-lite/docs/data.html#graticule) data sources; otherwise, `true`.

**Note:** This property cannot be used in a [style config](https://vega.github.io/vega-lite/docs/mark.html#style-config).

color

[Color](types.html#color) | [Gradient](gradient.html) | [ExprRef](types.html#exprref)

Default color.

**Default value:** ■ `"#4682b4"`

**Note:**

*   This property cannot be used in a [style config](https://vega.github.io/vega-lite/docs/mark.html#style-config).
*   The `fill` and `stroke` properties have higher precedence than `color` and will override `color`.

fill

[Color](types.html#color) | [Gradient](gradient.html) | Null | [ExprRef](types.html#exprref)

Default fill color. This property has higher precedence than `config.color`. Set to `null` to remove fill.

**Default value:** (None)

stroke

[Color](types.html#color) | [Gradient](gradient.html) | Null | [ExprRef](types.html#exprref)

Default stroke color. This property has higher precedence than `config.color`. Set to `null` to remove stroke.

**Default value:** (None)

blend

Blend | [ExprRef](types.html#exprref)

The color blend mode for drawing an item on its current background. Any valid [CSS mix-blend-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode) value can be used.

\_\_Default value: `"source-over"`

opacity

Number | [ExprRef](types.html#exprref)

The overall opacity (value between \[0,1\]).

**Default value:** `0.7` for non-aggregate plots with `point`, `tick`, `circle`, or `square` marks or layered `bar` charts and `1` otherwise.

fillOpacity

Number | [ExprRef](types.html#exprref)

The fill opacity (value between \[0,1\]).

**Default value:** `1`

strokeOpacity

Number | [ExprRef](types.html#exprref)

The stroke opacity (value between \[0,1\]).

**Default value:** `1`

### Stroke Style Properties

Property

Type

Description

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

strokeWidth

Number | [ExprRef](types.html#exprref)

The stroke width, in pixels.

Here is an example to the usage of the stroke dash where 6 is the size of dashes, and 4 is the size of spaces:

### Hyperlink Properties

Marks can act as hyperlinks when the `href` property or [channel](encoding.html#href) is defined. When the `href` property is specified, the [`cursor` mark property](mark.html#hyperlink) is set to `"pointer"` by default to serve as affordance for hyperlinks.

Property

Type

Description

href

URI | [ExprRef](types.html#exprref)

A URL to load upon mouse click. If defined, the mark acts as a hyperlink.

## Mark Config

```js
// Top-level View Specification
{
  ...
  "config": {
    "mark": ...,
    "area": ...,
    "bar": ...,
    "circle": ...,
    "line": ...,
    "point": ...,
    "rect": ...,
    "rule": ...,
    "geoshape": ...,
    "square": ...,
    "text": ...,
    "tick": ...
  }
}
```

The `mark` property of the [`config`](config.html) object sets the default properties for all marks. In addition, the `config` object also provides mark-specific config using its mark type as the property name (e.g., `config.area`) for defining default properties for each mark.

The global mark config (`config.mark`) supports all standard mark properties (except `type`, `style`, `clip`, and `orient`). For mark-specific config, please see the documentation for each mark type.

Note:

1.  If [mark properties in mark definition](#mark-def) or [mark property encoding channels](encoding.html#mark-prop) are specified, these config values will be overridden.
2.  Mark config do not support [offset mark properties](#offset).

## Mark Style Config

```js
{
  // Top Level Specification
  "config": {
    "style": {
      ...
    }
    ...
  }
}
```

In addition to the default mark properties above, default values can be further customized using named _styles_ defined under the `style` property in the config object.

Property

Type

Description

style

Object

An object hash that defines key-value mappings to determine default properties for marks with a given [style](https://vega.github.io/vega-lite/docs/mark.html#mark-def). The keys represent styles names; the values have to be valid [mark configuration objects](https://vega.github.io/vega-lite/docs/mark.html#config).

For example, to set a default shape and stroke width for `point` marks with a style named `"triangle"`:

```json
{
  "style": {
    "triangle": {
      "shape": "triangle-up",
      "strokeWidth": 2
    }
  }
}
```

Styles can then be invoked by including a `style` property within a [mark definition object](#mark-def).

Note: To customize the style for guides (axes, headers, and legends), Vega-Lite also includes the following built-in style names:

*   `"guide-label"`: style for axis, legend, and header labels
*   `"guide-title"`: style for axis, legend, and header titles
*   `"group-title"`: styles for chart titles

### Example: Styling Labels

You can use [`text` marks](text.html) as labels for other marks by setting `style` for the marks and using [style config](mark.html#style-config) to configure offset (`dx` or `dy`), `align`, and `baseline`.

See also: [a similar example that uses mark definition to configure offset, align, and baseline](text.html#labels).
