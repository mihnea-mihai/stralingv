# strălingv

## Description

Inspired by Wikimedia's project [Etytree](https://github.com/esterpantaleo/etymology) and my own manually drawn [infographics](https://etimologiavietii.wordpress.com/), this project aims to programatically generate etymology trees from [Wiktionary](https://www.wiktionary.org/) data.

## Method

This Python application parses Wiktionary API output to recursively retrieve etymological data of input words and render their etymological connections using [Graphviz](https://www.graphviz.org/).

## Examples

### Ascendants and descendants of a particular word

![Etymology tree of Romanian "crește"](showcase/Romanian%20crește.svg)

### All descendants of a particular PIE root

![Etymology tree of PIE root "*ḱer-"](showcase/Proto-Indo-European%20*ḱer-.svg)

## Errors

This project is still in its very early stages, so errors regarding meaning or connections are to be expected.