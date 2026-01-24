# Lightroom Custom Metadata Plugin Creator

This project aims to be a simple way for non-technical lightroom users to add custom metadata tags to their Lightroom Classic Catalog.

## Usage

There's a [demo hosted here](https://lightroom.shadowlerone.ca).

Fill out the form, click Generate Plugin, then install the plugin in Lightroom.

Plugin Installation instructions: [written](docs/plugin-installation.md), [video](https://www.adobe.com/ca/learn/lightroom-classic/web/lightroom-use-manage-plugins).



## Notes about Lightroom Metadata Plugins

Lightroom metadata plugins can officially have three kinds of fields:
- string
- URL
- Enum

### `String`

Standard metadata field.
Basis for the other fields.
Has a `value` and a `title`. `value` is stored data. `title` is the human readable name of the field. `value` is user input, stored as a `string`.

### `URL`

Similar to String. This generator treats them the same, Lightroom differentiates them. `title` and `value` are the same as `String`.

### `Enum`

A choice between multiple values. Each `title` must be unique. At most one `value` can be `nil`. `title` is the name shown to users, `value` is the data stored by Lightroom. 

## TODO

### Main Feature Goals

- Feature: Allow uploading and editing previously generated Metadata Plugin

### Stretch Feature Goals

- Plugin writes to XMP so data is accessible outside of Lightroom.
