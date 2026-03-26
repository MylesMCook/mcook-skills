# Deneb PBIR and Visual Editor

Purpose: Visual editor workflow and PBIR implementation guidance.

Source URLs:
- https://deneb.guide/docs/visual-editor
- https://deneb.guide/docs/next/pbir-guide

## Visual Editor | Deneb

Source URL: https://deneb.guide/docs/visual-editor

The Visual Editor is used to define your specification, configuration and any other options.

## Opening the Editor

The Visual Editor is only available when your report is in edit mode - when you're editing in Power BI Desktop or in the Service. If the report is being viewed in the Power BI Service or other application, then it is not eligible for editing and any such options will be unavailable to your end-users.

To use the editor, your visual first needs some data, so please ensure that you have added any appropriate columns or measures to the **Values** data role.

Once data has been provided, the Visual Editor is accessed by selecting the visual header (...) and then **Edit**, e.g.:

This will put the visual into focus mode and display the Visual Editor for you to begin creating or amending your specification.

## Finding your Way Around

The Visual Editor has 3 main components, or panes:

1.  Command Bar - for performing actions on your visual and the editor.
2.  Editor Pane - for creating your visual's definitions.
3.  Preview Area - for seeing what your visual will look like in your report.
4.  Debug Pane - for assisting with the development and refinement process.

Here's One We Made Earlier

We're showing a pre-built specification here; if this is your first time opening the editor in a new visual, then the **New Specification** dialog will be visible, to help you get started. Refer to the [Simple Worked Example](/docs/simple-example) page for an example of this functionality, or the [New Specification](#new-specification-ctrl--alt--n) section below for more details.

## The Command Bar

The Command Bar contains the following operations (from left to right):

#### Specification Editor pane (Ctrl + Alt + 1)

*   Selecting this option will display the Specification Editor pane. You can read more about this in the [Specification Editor Pane section below](#specification-editor-pane).

#### Config Editor pane (Ctrl + Alt + 2)

*   Selecting this option will display the Config Editor pane. You can read more about this in the [Config Editor Pane section below](#config-editor-pane).

#### Settings pane (Ctrl + Alt + 3)

*   Selecting this option will display the Settings pane. You can read more about this in the [Settings Pane section below](#settings-pane).

#### Apply Changes (Ctrl + Enter)

*   Selecting this option will apply any changes you have made in either the _Specification_ or _Config_ and update your visual.
*   This option is disabled if you have _Auto-Apply_ enabled (see below).

Apply Often

If you exit focus mode (and out of the Visual Editor) **any unapplied changes may not be saved**, so please ensure that you apply changes before returning to the standard view. Refer to the [Unapplied Changes](#unapplied-changes) section below for more details as to how you can mitigate this.

#### Auto-Apply Changes as you Type (Ctrl + Shift + Enter)

*   Selecting this option will apply changes to the _Specification_ or _Config_ editors as you type them.
*   Enabling this option will disable the _Apply_ command.

Consider Performance

Whilst this option is convenient for seeing changes take effect immediately, it can have negative performance implications if you're working with a large number of data points or elements within your visualization. Please refer to the [Performance Considerations](/docs/performance) page for further details on potential risks and mitigation approaches.

#### New Specification (Ctrl + Alt + N)

*   Selecting this option will open the _Create New Specification_ dialog.
*   The dialog can be used to replace the current Specification and Config with either an bare-minimum set of JSON for each, or you can choose from a number of simple templates to get started.
*   Templates are currently packaged in with the visual and it's not yet possible to import them, although hopefully this will be something we can work on bringing in later on.

First Time Use

This dialog is also displayed by default if this is the first time opening the Visual Editor for any new instance of Deneb that you add to the report canvas.

#### Generate JSON Template (Ctrl + Alt + E)

*   Selecting this option will open the **Generate JSON Template** dialog.
*   The dialog can be used to create an exportable version of the your specification. Refer to the [appropriate section in the Templates page](/docs/templates#generating-a-template) for more information on usage.

#### Theme Toggle (Ctrl + Shift + Alt + T)

*   Selecting this option will toggle the theme of the Visual Editor between light and dark modes.
*   By default, this will not affect the preview area, which will always attempt to mimic the background color of the report canvas. You can disable this in the [Preview Area settings](#preview-area) if you wish to see the visual in a consistent theme.

#### **Help (Ctrl + Alt + H)**

*   Selecting this option will cause Power BI to confirm you wish to open the link to this documentation site. Selecting **OK** will open it in a new browser tab.

## Editor Pane

The Editor Pane is where you will edit your specification, config and apply any other settings you need to.

### Resizing the Editor Pane

The Editor Pane can be resized if you wish to allocate more space on the screen for your Preview and/or Debug panes.

Some points to note:

*   The pane can be resized to use a maximum of 60% of the visible canvas by click-dragging.
*   Double-clicking the resizer will revert the pane to its default size (40% of the visible canvas).

### JSON Editor Properties

The **Advanced editor > JSON editor** property card in Power BI's formatting pane lets you modify the following properties of the JSON editor:

#### Position

Allows you to toggle the position of the Editor Pane between the left and right-hand sides of the screen. By default, the editor is on the left.

#### JSON Editor Font Size

Allows you to modify the size of the font used in the JSON editor. By default, this is set to 10px.

#### Word Wrap

By default, any content in the editor that overflows the width will wrap onto a new line. By disabling this property, you can keep content on a single line, and the editor will display a horizontal scrollbar as appropriate.

#### Line Numbers

By default, the editor will show line numbers in the left-hand gutter. You can disable this property to hide them.

#### Change Event Detect Interval

This property allows you to specify the interval (in milliseconds) at which the editor will check for changes. By default, this is set to 700ms. It's recommended that you don't change this setting unless you're experiencing performance issues with the editor.

### Specification Editor Pane

Keyboard shortcut

**\[ Ctrl + Alt + 1 \]**

*   This pane contains an editor that you can use to enter and amend your specification's JSON as desired.

    *   The Vega JSON specification reference [can be found here](https://vega.github.io/vega/docs/specification/).
    *   The Vega-Lite JSON specification reference [can be found here](https://vega.github.io/vega-lite/docs/spec.html).
*   To view the results of your changes, you can either **Apply** your changes, or ensure that **Auto-apply changes as you type** is enabled.

*   The JSON must produce a valid specification for your selected provider (either Vega or Vega-Lite).

*   The editor will perform validation against the schema for the specified provider and warnings are displayed that you can inspect, e.g.:

### Config Editor Pane

Keyboard shortcut

**\[ Ctrl + Alt + 2 \]**

*   This pane contains an editor that you can use to enter and amend any JSON you wish to add for your visual's config as desired.
    *   The Vega JSON config reference [can be found here](https://vega.github.io/vega/docs/config/).
    *   The Vega-Lite JSON config reference [can be found here](https://vega.github.io/vega-lite/docs/config.html).
*   To view the results of your changes, you can either **Apply** your changes, or ensure that **Auto-apply changes as you type** is enabled.
*   The JSON must produce a valid config for your selected provider (either Vega or Vega-Lite).
*   It's generally advised to try and use the config for anything that can "theme" your chart and keep this separate from the specification. This makes easier to port across to other instances of the visual.

### Status Bar

The status bar at the bottom of each editor re-states which provider you are using (Vega or Vega-Lite) and which version is embedded.

Check the Provider Version Can Do What You're Looking Up

Deneb doesn't automatically support new releases of Vega or Vega-Lite. Because the runtimes are embedded, any new releases need to be be tested, implemented and deployed to AppSource, which can take some time. As such, you can use this information in the toolbar to confirm if the embedded version might be behind any new features published by the Vega team.

The status bar also shows the current cursor position.

### Settings Pane

Keyboard shortcut

**\[ Ctrl + Alt + 3 \]**

*   This pane is used to configure specific behavior of Deneb when generating output:

*   The **Provider** section allows you to specify whether to use Vega or Vega-Lite for your Specification and Config.

    *   Vega-Lite is much simpler for newcomers as it is much more concise and abstracts away a lot of the things that you would normally need to prescribe when using Vega.
    *   Vega does provide a lot more in the way of control over your visualization at the cost of a higher-learning curve.
*   _The_ **Render mode** section specifies whether to use either Vega's SVG renderer or Canvas renderer when compiling, parsing and producing your design.

    *   _Canvas_ renders your design as pixel graphics.
    *   _SVG_ creates your design from vector graphics, results in a number of component elements within the visual to produce the output.
    *   Please refer to the [Performance Considerations](/docs/performance#selection-of-renderer) page for further details on potential risks and mitigation approaches when it comes to selecting a renderer.
*   The **Vega > Power BI interactivity** section specifies which interactivity features to enable.

    *   As these require some additional setup in your specification, as well as some internal logic to link everything together you are able to specify whether they should be set-up or not.
    *   Please refer to the [Interactivity Features](/docs/interactivity-overview) and related pages ([Tooltips](/docs/interactivity-tooltips) | [Context-Menu](/docs/interactivity-context-menu) | [Cross-Filtering](/docs/interactivity-selection) | [Cross-Highlighting](/docs/interactivity-highlight)) for further details on how to configure these for your specification.

### Column and Measure Completion

Specification editor only

Deneb offers auto-completion based on the Vega and Vega-Lite language schemas. In addition to this, any columns or measures that are added to the **Values** data role, will be offered in the Specification editor’s auto-completion, e.g.:

### Unapplied Changes

If you've made changes in the Visual Editor and select _Back to report_ without applying them, you will get a prompt alerting you of this:

caution

This is a 'last chance' to make sure that any changes you want to keep are applied. If changes are discarded, they cannot be recovered.

## Preview Area

Deneb captures the dimensions of your visual prior to opening the Visual Editor and shows this at 100% scale. This is so that you know how your design should look within the confines of the visual viewport when you return to the report, e.g.:

Your visual may not fit entirely into the preview area at 100% scale, so you can use the [Zoom Controls in the Debug Pane](#zoom-controls) (or collapse it) to adjust this accordingly, [or resize (or collapse) the editor pane](#editor-pane) to accommodate.

The **Advanced editor > Preview area** property card in Power BI's formatting pane lets you modify the following properties of the Preview Area:

#### Viewport Marker

The dashed line represents the viewport (boundaries) of your visual in standard view. **Power BI does not allow visuals to resize themselves dynamically**, so if you wish to change the physical width and/or height of your visual in the report view, you will need to exit the Visual Editor, resize your visual, and then re-open the Visual Editor.

If you would prefer to not see the viewport marker, you can disable this in the properties pane by selecting **Show viewport marker > Off**.

#### Show Scrollbars

If your visual specification overflows the viewport, the default behavior of the preview area is to show the output overflowing the content. This is so that you can see the full output of your specification and what might get truncated in the report view.

If you wish to mimic the behavior of the report view, you can enable the **Show scrollbars on overflow** property. This will cause the preview area to use scrollbars as appropriate rather than overflowing the content outside the viewport marker area.

To learn more about scrolling and overflow behavior, please refer to the [Scrolling and Overflow](/docs/scrolling-overflow) page.

#### Background Settings

This setting attempts to mimic the background color of the report canvas, so that you can see how your visual will look in the report. If this is not to your liking (for instance, you would like dark mode to affect the entire interface, noting that your visual preview might not truly represent how it looks in your report), you can disable this property.

## Debug Pane

The Debug Pane provides you with additional tooling to inspect and debug your visual design, as well as exposing information about the Vega or Vega-Lite view used to generate it.

From left to right, the components of the pane are as follows:

### Data Pane

The Data Pane exposes information about data sets from the Vega view, and is the default view in the Debug Pane. Assuming that your visual parses correctly, this will provide a dropdown to choose the desired data stream to inspect, and the details of this will then be shown in the table underneath.

*   The default selection is the `dataset` entry, which is the data supplied to Deneb from your data model. This includes [any additional fields](/docs/interactivity-overview#additional-datum-fields) Deneb adds to assist you for interactivity purposes, so that you can inspect their values much more easily than [using tooltips to expose a mark's datum](/docs/interactivity-tooltips#debugging-with-tooltips).

*   Complex objects will only render if they are small enough; larger ones will be truncated with `{...}` (but can be inspected further in a tooltip by hovering over the placeholder value), e.g.:

*   Tooltips for interactivity values and headers are also contextual, to better assist you with what things might mean, e.g.:

*   For performance reasons with rendering (mainly because a data stream can contain complex objects), the number of visible rows is capped at 10 per page. You may therefore need to navigate the table using the pagination tools underneath it to look at any specific records; however, columns can be sorted by clicking on the appropriate header.

### Signals Pane

The Signals Pane can be used to inspect the state of [signals](https://vega.github.io/vega/docs/signals/) from the Vega view. Signals are often auto-generated for features in Vega-Lite, such as [parameters](https://vega.github.io/vega-lite/docs/parameter.html).

The functionality of the table is very much the same as for the Data Pane.

### Logs Pane

The Logs pane is used to monitor [logging](https://vega.github.io/vega/docs/api/util/#logging) events emitted by the Vega view. Here, you can set the desired log level and this will update when the specification is (re)parsed.

*   The default logging level is `warn`.
*   Note that due to the verbosity of the output created by the `debug` level, this is not available in Deneb.

### Zoom Controls

The Zoom Controls are intended to assist you with detail work; particularly as Power BI custom visuals can only occupy a certain amount of the main interface. These functions are:

*   Zoom preview out by 10%

*   Zoom level slider - allows manual adjustment of zoom level from 10% to 400%.

*   Zoom preview in by 10%

*   Current zoom level - click to set a specific zoom level:

*   Zoom preview to fit available space

### Collapse or Expand Debug Pane

This control will allow you to toggle the visible state of the Debug Pane.

## PBIR Implementation Guide | Deneb

Source URL: https://deneb.guide/docs/next/pbir-guide

This is unreleased documentation for Deneb **Canary 🚧** version.

For up-to-date documentation, see the **[latest version](/docs/pbir-guide)** (1.9).

Optimized for Deneb 1.9 and Above

This guide is valid for Deneb 1.9 and above. This _should_ work with earlier versions, but you may need to manually step through or dismiss the _Create or import new specification_ dialog in the Advanced Editor for new visuals, and this experience has been improved from 1.9 onwards.

With [Power BI Enhanced Report Format (PBIR)](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report?WT.mc_id=DP-MVP-5003712&tabs=v2%2Cdesktop#pbir-format) becoming the default for Power BI reports, this page provides guidance on how you may wish to understand what is needed to make Deneb features work, if you are manually editing or programmatically generating Deneb visuals, or if you are using an LLM or other tool to help generate report content (or if you are an LLM reading this page for guidance).

In addition to PBIR, the detail on this page may also help understand Deneb's internal structure better, for use with building [report themes](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes??WT.mc_id=DP-MVP-5003712) containing Deneb visuals.

## The Short Version

It's advisable to read the full guide below, but if you just want the quick reference for the minimum properties needed to create a working Deneb visual in PBIR, here they are:

### Minimal Deneb Visual Definition

In a `visual.json` file for a visual instance:

Path

Value

`visual.visualType`

`"deneb7E15AEF80B9E4D4F8E12924291ECE89A"`

`visual.objects.vega[0].properties.jsonSpec`

Your stringified Vega/Vega-Lite spec, surrounded by `''`

`visual.objects.vega[0].properties.jsonConfig`

`"'{}'"`

### Validating Your PBIR Configuration

Before loading your report:

1.  Ensure all JSON strings are properly escaped.
2.  Verify integer values end with `D` suffix.
3.  Confirm text values are wrapped in single quotes within the `Value` field.
4.  Confirm boolean values are set to `true` or `false` as literals.

Refer to the [Property Implementation Guide](#property-implementation-guide) section below for more details on these types.

## Visual GUID

All Power BI visuals have a unique identifier (GUID) that is used to identify the visual type. For the AppSource (certified) version of Deneb, this GUID is:

`deneb7E15AEF80B9E4D4F8E12924291ECE89A`

The GUID is also used by Power BI to determine where to look for visual updates. If the GUID Matches a published visual in AppSource, Power BI will attempt to update the visual when a new version is available. Also, if using PBIR/PBIP, this ensures that the visual code does not need to be included in the PBIP assets, as Power BI can retrieve it from AppSource directly and therefore does not need to be source controlled.

#### Other Visual Editions

If you're using the other editions of Deneb, the GUIDs are as follows:

*   Standalone: `STANDALONEdeneb7E15AEF80B9E4D4F8E12924291ECE89A`
*   Alpha Channel: `ALPHAdeneb7E15AEF80B9E4D4F8E12924291ECE89A`
*   Beta Channel: `BETAdeneb7E15AEF80B9E4D4F8E12924291ECE89A`

These editions are not tied to AppSource and will have additional setup required, as the .pbiviz code will need to be included in the PBIP assets for these editions to work correctly.

Much like the legacy .pbix format for Power BI workbooks, .pbiviz files are compressed folders that can be opened with a tool like 7-Zip to extract the contents for inspection. Extracting the .pbiviz into `/CustomVisuals/{GUID}/` will provide the necessary structure to include the visual in PBIR/PBIP.

## Understanding Visual Capabilities

Visual [capabilities](https://learn.microsoft.com/en-us/power-bi/developer/visuals/capabilities?WT.mc_id=DP-MVP-5003712) are special metadata that are effectively a visual's "contract" with Power BI, including what data roles it supports (and how it gets organized), formatting options, and interactivity features. In PBIR, these capabilities are defined in a JSON format and are one of the first touchpoints Power BI uses when a visual is added to a report to determine how it should integrate with the report environment.

When you add a visual to a report and start configuring it, information persisted into the JSON for that visual instance will include things that tie to this capabilities definition, allowing the visual to be re-generated from persisted state whenever you re-open the page (or report).

It can be easy to assume that these work in a particular way, but it is important to realize that (particularly in the case of persisted properties), visuals often have logic to act upon these values as part of their internal operation. So, it can therefore be assumed how they work but this document serves to provide you with details of what properties are set and how they affect your generated Deneb visuals so that you can understand how to work with them rather than guess at what they do (and possibly do the wrong things in some cases).

## Dissecting The Simplest Scenario: A Manually Added Deneb Visual

To try and get an understanding of the structure, let's have a look at what happens when we add a Deneb visual to a report canvas, without adding data or configuring anything. The base definition may look like this:

Visual added manually to report, with no additional configuration or data

```
{  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",  "name": "2c2722561a0b6c3deded",  "position": {    "x": 80,    "y": 56,    "z": 0,    "height": 280,    "width": 280,    "tabOrder": 0  },  "visual": {    "visualType": "deneb7E15AEF80B9E4D4F8E12924291ECE89A",    "objects": {      "stateManagement": [        {          "properties": {            "viewportHeight": {              "expr": {                "Literal": {                  "Value": "270D"                }              }            },            "viewportWidth": {              "expr": {                "Literal": {                  "Value": "270D"                }              }            }          }        }      ]    },    "drillFilterOtherVisuals": true  }}
```

The `visual.objects` section is where Deneb persists its configuration settings.

We can already see that there is information under `visual.objects.stateManagement`. These are internal settings that deneb generates every time the visual receives updated information from Power BI, such as when the visual is resized or data changes, and is needed to ensure that when we open the editor, the visual preview matches the dimensions of the visual in the report. **It is therefore not something you need to set manually**, as Deneb will manage this for you (refer to the [properties reference](#objectsstatemanagement) section below for more details).

### Equivalent Minimal Definition

Therefore, if you were to add your own visual to the report using PBIR, the example below is functionally equivalent to the above:

Minimal Deneb visual definition for PBIR

```
{  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",  "name": "2c2722561a0b6c3deded",  "position": {    "x": 80,    "y": 56,    "z": 0,    "height": 280,    "width": 280,    "tabOrder": 0  },  "visual": {    "visualType": "deneb7E15AEF80B9E4D4F8E12924291ECE89A",    "drillFilterOtherVisuals": true  }}
```

This will display a Deneb visual on the report canvas and will show the landing page, as there is no active project.

## Adding Data to the Visual

So now, I want to add some data to my visual. In this case, I am going to add a simple table with the `Product` column from my **Product** Table, and the `$ Sales` measure from my **Financials** Table. After adding these fields to the visual, the definition now looks like this:

Deneb visual definition with data roles mapped

```
{  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",  "name": "2c2722561a0b6c3deded",  "position": {    /* same as previous example */  },  "visual": {    "visualType": "deneb7E15AEF80B9E4D4F8E12924291ECE89A",    "query": {      "queryState": {        "dataset": {          "projections": [            {              "field": {                "Column": {                  "Expression": {                    "SourceRef": {                      "Entity": "Product"                    }                  },                  "Property": "Product"                }              },              "queryRef": "Product.Product",              "nativeQueryRef": "Product"            },            {              "field": {                "Measure": {                  "Expression": {                    "SourceRef": {                      "Entity": "Financials"                    }                  },                  "Property": "$ Sales"                }              },              "queryRef": "Financials.$ Sales",              "nativeQueryRef": "$ Sales"            }          ]        }      },      "sortDefinition": {        "sort": [          {            "field": {              "Column": {                "Expression": {                  "SourceRef": {                    "Entity": "Product"                  }                },                "Property": "Product"              }            },            "direction": "Ascending"          }        ],        "isDefaultSort": true      }    },    "drillFilterOtherVisuals": true  }}
```

This is standard stuff for any visual under PBIR, so let's choose to focus on the bits that are important for Deneb.

*   `visual.query.queryState.dataset` represents any columns or measures added to the visual's **Values** data role. This is known internally in the visual capabilities as `dataset`, matching how Deneb maps and assigns this data into your specification.

*   Fields in the `dataset` are created and referenced to the display name of the field in the well. If you don't rename this, it will match the column or measure name as defined in the data model. Otherwise there will be a `displayName` property present in the metadata for the field. For example, if I rename `$ Sales` to `Total Sales` in the visual well, the field definition will now include this:

    ```
    {  "field": {    "Measure": {      "Expression": {        "SourceRef": {          "Entity": "Financials"        }      },      "Property": "$ Sales"    }  },  "queryRef": "Financials.$ Sales",  "nativeQueryRef": "$ Sales", // <-- This  is used if unmodified in the 'Values' well  "displayName": "Total Sales" // <-- This will be used by Deneb when building the dataset, if present}
    ```

*   In addition to this above consideration, Deneb will also [sanitize field names](/docs/next/dataset#special-characters-in-column-and-measure-names) if they include characters that are not valid in [Vega](https://vega.github.io/vega/docs/types/#Field) or [Vega-Lite](https://vega.github.io/vega-lite/docs/field.html) specifications. While this is not important for this step, it is important when building a specification that references these fields, so please refer to the linked documentation for more details.

## Creating A Bare Minimum Specification

Let's say I have this simple specification that creates a simple bar chart with Vega-Lite:

Simple Vega-Lite bar chart specification

```
{  "data": {    "name": "dataset"  },  "mark": {    "type": "bar"  },  "encoding": {    "y": {      "field": "Product",      "type": "nominal"    },    "x": {      "field": "$ Sales",      "type": "quantitative"    }  }}
```

Due to how Power BI's property system works, the JSON for the specification and configuration will be serialized and escaped ("[stringified](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)") before being stored in the visual's properties. As our visual has an empty config (`{}`), the property storage should be prepared as follows:

Deneb visual definition with specification added

```
{  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",  "name": "2c2722561a0b6c3deded",  "position": {    /* same as previous example */  },  "visual": {    "visualType": "deneb7E15AEF80B9E4D4F8E12924291ECE89A",    "query": {      /* same as previous example */    },    "objects": {      "vega": [        {          "properties": {            "jsonSpec": {              "expr": {                "Literal": {                  "Value": "'{\n  \"data\": {\n    \"name\": \"dataset\"\n  },\n  \"mark\": {\n    \"type\": \"bar\"\n  },\n  \"encoding\": {\n    \"y\": {\n      \"field\": \"Product\",\n      \"type\": \"nominal\"\n    },\n    \"x\": {\n      \"field\": \"$ Sales\",\n      \"type\": \"quantitative\"\n    }\n  }\n}'"                }              }            },            "jsonConfig": {              "expr": {                "Literal": {                  "Value": "'{}'"                }              }            }          }        }      ]    },    "drillFilterOtherVisuals": true  }}
```

Our specification and configuration are now stored under `visual.objects.vega` in the properties `jsonSpec` and `jsonConfig` respectively. These will be deserialized and parsed by Deneb when the visual is loaded in Power BI, and the visual will render as expected. So as long as your JSON string is valid (and this can contain comments, as Deneb will parse using JSONC), then Deneb will be able to work with it.

Deneb's default provider configuration is Vega-Lite, so we only need to provide the specification itself and the logic will work as expected. We will provide a reference for each `objects` section further below, to help you understand how to assemble more complex configurations based on your needs.

If we open our workbook with this configuration, we will see our simple bar chart rendered as expected, e.g.:

## Properties Reference

The following sections provide a reference for each of the `objects` that Deneb uses to persist configuration and state. Where possible we'll provide as much detail as as we can as to what each property does, and how it affects the visual's operation.

May Also Be Useful for Theming

Some of these properties are used for advanced editor configuration and therefore may not be relevant if you are only generating visuals for consumption, but may help with creating [report themes](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes??WT.mc_id=DP-MVP-5003712) and understanding what setting their defaults may do for you and your users.

### `objects.vega`

Properties in this groups are concerned with the specification and configuration for the Vega or Vega-Lite runtime within a Deneb visual instance.

Property

Default Value (if Omitted)

Type

Remarks

`jsonSpec`

`'{}'`

[text](#text)

The Vega or Vega-Lite specification, which is JSON (or JSONC) turned into a string representation.

`jsonConfig`

`'{}'`

[text](#text)

The Deneb configuration object, which is JSON (or JSONC) turned into a string representation.

`provider`

`'vegaLite'`

[text](#text) (enum)

The provider to use when parsing a specification. Either `vega` or `vegaLite`.

`renderMode`

`'svg'`

[text](#text) (enum)

The rendering mode to use. Either `canvas` or `svg`.

`logLevel`

`3D` (vega.Info)

[integer](#integer)

The [logging verbosity level](https://github.com/vega/vega-util?tab=readme-ov-file#logging) for the Vega/Vega-Lite runtime. One of: `0` (None), `1` (Error), `2` (Warn), `3` (Info).

`enableTooltips`

`true`

[boolean](#boolean)

Enables the [Power BI tooltip handler](/docs/next/interactivity-tooltips) instead of Vega's built in one. Analogous to checking the _Tooltip handler_ checkbox in the interactivity settings.

`enableContextMenu`

`true`

[boolean](#boolean)

Ensures that data points are resolved in [Power BI's context menu](/docs/next/interactivity-context-menu) when right-clicking a visual. Analogous to checking the _Resolve data points in context menu_ checkbox in the interactivity settings.

`enableHighlight`

`false`

[boolean](#boolean)

Enables support for tracking and responding to [highlight events](/docs/next/interactivity-highlight) from other visuals. Analogous to checking the _Expose cross-highlight values for measures_ checkbox in the interactivity settings.

`enableSelection`

`false`

[boolean](#boolean)

Enables support for tracking and responding to [cross-filter](/docs/next/interactivity-selection) events when interacting with your visual and tracking state. Analogous to checking the _Expose cross-filtering values for dataset rows_ checkbox in the interactivity settings.

`selectionMaxDataPoints`

`50D`

[integer](#integer)

The maximum number of data points to consolidate for cross-filtering operations and is only relevant when `enableSelection` is `true`.

`selectionMode`

`simple`

[text](#text) (enum)

The selection mode to use when `enableSelection` is `true`. `simple` will monitor the Vega view, attempt to resolve data points and apply cross-filtering. `advanced` relies upon [advanced cross filtering](/docs/next/interactivity-selection-advanced), which is only supported and functional when `provider` is `'vega'` and you have defined the relevant events in your spec to initiate it.

`version`

\[managed by Deneb\]

[text](#text)

Deneb uses this as a checkpoint to store the version of the provider last used to render your visual, and is assumed to be the currently packaged version of Vega or Vega-Lite if omitted. It is automatically populated when the visual is updated and used to track any migration requirements.

### `objects.display`

Properties in this group are displayed in the _Rendered visual_ property menu in the formatting pane and are concerned with any processing Deneb does to the visual output on top of the Vega view.

Property

Default Value (if Omitted)

Type

Remarks

`scrollbarColor`

`#000000`

[color](#color)

The color of the [container scrollbar](/docs/next/scrolling-overflow#configuring-scrollbar-appearance) when it is shown.

`scrollbarOpacity`

`20D`

[integer](#integer)

The opacity of the [container scrollbar](/docs/next/scrolling-overflow#configuring-scrollbar-appearance) when it is shown. Values are converted to decimal percentage by Deneb and valid values are `0D` to `100D`.

`scrollbarRadius`

`0D`

[integer](#integer)

The border radius of the [container scrollbar](/docs/next/scrolling-overflow#configuring-scrollbar-appearance) in px when it is shown. Valid values are `0D` to `3D`; anything higher than `3D` will be artificially capped due to the scrollbar's thickness.

`scrollEventThrottle`

`5D`

[integer](#integer)

The throttle delay in ms for updating the container scroll position values [in the `pbiContainer` signal](/docs/next/scrolling-overflow#using-pbicontainer-to-track-scrolling-events). Valid values are `0D` to `1000D`.

### `objects.dataLimit`

Properties in this group are displayed in the _Data limit options_ menu and used to dictate how Deneb should handle [data row limits](/docs/next/dataset#data-row-limits) imposed by Power BI.

Property

Default Value (if Omitted)

Type

Remarks

`override`

`false`

[boolean](#boolean)

When `true`, this will enable the [_Override row limit_ property](/docs/next/dataset#data-row-limits), instructing Deneb to fetch more data when the standard 10,000 row limit is reached.

`showCustomVisualNotes`

`true`

[boolean](#boolean)

When `true`, this will show the _Custom visual notes_ section in the editor's data panel when data is being fetched.

### `objects.developer`

Properties in this group are intended for internal use.

Property

Default Value (if Omitted)

Type

Remarks

`version`

\[managed by Deneb\]

[text](#text)

Deneb uses this as a checkpoint to store the version of the visual last used in your report, and is assumed to be the current visual version from the manifest if omitted. It is automatically populated when the visual is updated and used to track any migration requirements when a newer version of the visual is applied to the report (or warnings if downgraded).

### `objects.stateManagement`

Properties in this group are intended for internal use and transient state management between sessions.

Property

Default Value (if Omitted)

Type

Remarks

`viewportHeight`

`null` \[managed by Deneb\]

[integer](#integer)

The last known height of the visual viewport when viewing normally (in px). If omitted, Deneb will calculate this and update whenever the visual is updated, to ensure that it matches the visual container on the canvas. It is only needed to ensure that the preview is correctly sized in the Advanced Editor and is not necessary for any automation. Details have ony been included for completeness.

`viewportWidth`

`null` \[managed by Deneb\]

[integer](#integer)

The last known width of the visual viewport when viewing normally (in px). If omitted, Deneb will calculate this and update whenever the visual is updated, to ensure that it matches the visual container on the canvas. It is only needed to ensure that the preview is correctly sized in the Advanced Editor and is not necessary for any automation. Details have ony been included for completeness.

### `objects.editor`

Properties in this group are displayed in the _Advanced Editor_ property menu in the formatting pane and are concerned with the editor's operation and appearance. Setting them can be used to 'prime' the editor experience for users but will have no effect on the visual's rendering or operation outside of the editor.

Property

Default Value (if Omitted)

Type

Remarks

`theme`

`light`

[text](#text) (enum)

The theme to use for the editor interface. Either `light` or `dark`.

`showViewportMarker`

`true`

[boolean](#boolean)

When `true`, shows the viewport marker in the editor [preview area](/docs/next/visual-editor#preview-area).

`previewScrollbars`

`true`

[boolean](#boolean)

When `true`, shows scrollbars in the editor [preview area](/docs/next/visual-editor#preview-area) when the rendered specification overflows the container viewport.

`backgroundPassthrough`

`true`

[boolean](#boolean)

When `true`, the editor [preview area](/docs/next/visual-editor#preview-area) will render with a transparent background, allowing you to see through to any underlying report canvas background.

`position`

`left`

[text](#text) (enum)

The position of the [JSON editor](/docs/next/visual-editor#json-editor-properties) pane. Either `left` or `right`.

`fontSize`

`10D`

[integer](#integer)

The font size in px for the [JSON editor](/docs/next/visual-editor#json-editor-properties). Valid values are `8D` to `30D`.

`wordWrap`

`true`

[boolean](#boolean)

When `true`, enables word wrapping in the [JSON editor](/docs/next/visual-editor#json-editor-properties).

`showLineNumbers`

`true`

[boolean](#boolean)

When `true`, shows line numbers in the [JSON editor](/docs/next/visual-editor#json-editor-properties).

`debouncePeriod`

`300D`

[integer](#integer)

How frequently to track changes to the content inside the [JSON editor](/docs/next/visual-editor#json-editor-properties).

`debugTableRowsPerPage`

`50D`

[integer](#integer)

The number of rows to show per page for the Advanced Editor's [data tables in the debug pane](/docs/next/visual-editor#debug-pane). This can be any integer value, but the interface provides options for `10`, `25`, `50`, `100`, `150` and `200`.

## Property Implementation Guide

The PBIR documentation does not elaborate on property specifics too well, so here are some notes regarding types that may help you understand how to work with them in Deneb. Note that we only cover how we support them instead of the whole PBIR property system.

### Common Pitfalls

1.  **Forgetting the `D` suffix** on numeric values - Power BI will fail to parse
2.  **Double-escaping JSON** in `jsonSpec` - results in parse errors
3.  **Using double quotes** instead of single quotes for text literals
4.  **Missing `expr.Literal.Value` wrapper** - properties won't be recognized

### `boolean`

Boolean properties should use `true` or `false` literals. For example, to set a boolean property to `true`, you would use:

Boolean property structure

```
{  "enableTooltips": {    "expr": {      "Literal": {        "Value": "true"      }    }  }}
```

### `color`

Color properties match the structure of `#/definitions/fill` from the [Report Theme JSON Schema](https://github.com/microsoft/powerbi-desktop-samples/tree/main/Report%20Theme%20JSON%20Schema) published by MS. For Deneb, we currently only use (and support) `solid`.

Colors can be supplied using `Literal` values that should support any known HTML/CSS color format, but the structure is slightly different to regular text properties. It is also worth noting that the color value should be enclosed in single quotes due to them being stored like a [text](#text) literal within the JSON structure. For example, to set a color property to red, you would use:

Color property structure using 'Literal' value

```
{  "scrollbarColor": {    "solid": {      "color": {        "expr": {          "Literal": {            "Value": "'#FF0000'" // or "'red'", "'rgb(255,0,0)'", etc.          }        }      }    }  }}
```

And you can use `ThemeDataValue` for binding to your theme, e.g.:

Color property structure using 'ThemeDataValue' value

```
{  "scrollbarColor": {    "solid": {      "color": {        "expr": {          "ThemeDataColor": {            "ColorId": 1,            "Percent": 0          }        }      }    }  }}
```

### `integer`

Integer values should be suffixed with a `D` to indicate that they are numeric literals. For example, to set an integer property to `50`, you would use:

Integer property structure

```
{  "selectionMaxDataPoints": {    "expr": {      "Literal": {        "Value": "50D"      }    }  }}
```

### `text`

Text properties should be enclosed in single quotes (`'`) to indicate that they are string literals. For example, to set a text property to `vegaLite`, you would use:

Text property structure

```
{  "provider": {    "expr": {      "Literal": {        "Value": "'vegaLite'"      }    }  }}
```

Any JSON objects or arrays that need to be stored as text (such as the Vega specification) should be stringified and escaped accordingly, as shown in the earlier examples.
