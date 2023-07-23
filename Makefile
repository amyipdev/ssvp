SASS := sass
SASS_OPTIONS :=
SASS_SRCS = $(shell find scss/ -name '*.scss')

# TODO: automatically compile sass instead of manual

all:
	$(SASS) scss/custom.scss:assets/css/custom_bootstrap.css $(SASS_OPTIONS)
	$(MAKE) -C js
	