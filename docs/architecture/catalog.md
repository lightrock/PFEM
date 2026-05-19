# PFEM Catalog

The PFEM catalog is a read-only view of the design pattern on disk.

It lists:

- capabilities
- adapters
- profiles
- examples

The catalog does not define objects. It reads the registries and manifests that
already exist.

## Purpose

The catalog helps humans and AI assistants quickly answer:

- what behaviors exist?
- what input adapters exist?
- what node shapes exist?
- what examples prove the shape?
- where are the source files?

Run:

```bat
pfem_catalog.bat
```

or:

```bat
python tools\pfem_catalog.py
```

The catalog should stay boring, readable, and dependency-free.
