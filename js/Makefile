TSC := npx tsc
TSC_OPTIONS := --noEmitOnError
TSC_SRCS = $(shell sh gen_make_filenames.sh)

%.js: %.ts
	$(TSC) $(TSC_OPTIONS) --outFile ../assets/js/$@ $<

all: $(TSC_SRCS)