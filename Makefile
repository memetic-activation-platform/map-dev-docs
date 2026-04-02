.PHONY: clean build-core build-dahn build-mapp-dev build-glossary build-all serve-core serve-dahn serve-mapp-dev serve-glossary

clean:
	rm -rf site

build-core:
	mkdocs build -f mkdocs-core.yml

build-dahn:
	mkdocs build -f mkdocs-dahn.yml

build-home:
	mkdocs build -f mkdocs-home.yml

build-mapp-dev:
	mkdocs build -f mkdocs-mapp-dev.yml

build-glossary:
	mkdocs build -f mkdocs-glossary.yml

build-roadmap:
	mkdocs build -f mkdocs-roadmap.yml


build-all: clean build-home build-core build-dahn build-mapp-dev build-glossary build-roadmap

serve-core:
	mkdocs serve -f mkdocs-core.yml

serve-dahn:
	mkdocs serve -f mkdocs-dahn.yml

serve-home:
	mkdocs serve -f mkdocs-home.yml

serve-mapp-dev:
	mkdocs serve -f mkdocs-mapp-dev.yml

serve-glossary:
	mkdocs serve -f mkdocs-glossary.yml

serve-roadmap:
	mkdocs serve -f mkdocs-roadmap.yml