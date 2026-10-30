# Lightroom Custom Metadata Plugin Creator

This project aims to be a simple way for non-technical lightroom users to add custom metadata tags to their Lightroom Classic Catalog.

Based on [notes](https://regex.info/blog/2016-09-15/2731) from [Jeffrey Friedl, perhaps the GOAT of Lightroom Plugins](https://regex.info/blog/lightroom-goodies).

## Usage

There's a [demo hosted here](https://lightroom.shadowlerone.ca).

Fill out the form, click Generate Plugin, then install the plugin in Lightroom.

Plugin Installation instructions: [written](docs/plugin-installation.md), [video](https://www.adobe.com/ca/learn/lightroom-classic/web/lightroom-use-manage-plugins).

## The Stack 

Front end:

- [VueJS](https://vuejs.org/)
- [Bulma](https://bulma.io/)

Backend:

- [Flask](https://flask.palletsprojects.com/en/stable/)


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

- Feature: Allow uploading and editing previously generated Metadata Plugin
- Feature: Implement Advanced mode: more control over the underlying plugin
- Feature: Plugin writes to XMP so data is accessible outside of Lightroom.
- Maintenance: Finish writing tests
- Maintenance: Finish writing documentation




.test