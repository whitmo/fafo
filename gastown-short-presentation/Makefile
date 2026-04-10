slide-theme := wildclouds
SHOWOFF := ../labs/showoff/bin/showoff

index.html: slides.md js/reveal.js dist/theme/$(slide-theme).css ## build presentation and theme
	pandoc -t revealjs -s -V revealjs-url=. \
		-V theme=$(slide-theme) \
		-V width=1200 \
		-V center=false \
		-V autoPlayMedia=false \
		-V hash=true \
		-o "$@" "$<"

js/reveal.js:
	curl -LO https://github.com/hakimel/reveal.js/archive/master.zip
	bsdtar --strip-components=1 --exclude .gitignore --exclude LICENSE --exclude README.md --exclude demo.html --exclude index.html -xf master.zip
	rm master.zip
	npm install
	@# Copy built plugins to paths expected by Pandoc's revealjs template
	@for p in notes search zoom math highlight markdown; do \
		if [ -f dist/plugin/$$p.js ]; then \
			mkdir -p plugin/$$p; \
			cp dist/plugin/$$p.js plugin/$$p/$$p.js; \
		fi; \
	done

css/theme/$(slide-theme).scss: themes/$(slide-theme).scss
	cp "$<" "$@"

dist/theme/$(slide-theme).css: css/theme/$(slide-theme).scss
	npm run build:styles

start: index.html ## build presentation and start server
	@echo "Starting the local presentation server"
	@npm start

demo: ## Run showoff demo
	$(SHOWOFF) demo/steps demo/workspace

demo-reset: ## Reset showoff demo state
	$(SHOWOFF) --reset demo/steps demo/workspace

clean: ## clean up the working directory
	rm -f CONTRIBUTING.md LICENSE
	rm -rf css/ js/ public/ plugin/ scripts/ test/ react/
	rm -rf node_modules/ dist/
	rm -f index.html package-lock.json package.json
	rm -f tsconfig.json tsconfig.node.json vite.config.ts vite.config.styles.ts
	rm -rf demo/workspace/

watch: ## Watch for changes and rebuild
	@echo "Watching for changes..."
	@watchmedo tricks-from tricks.yaml

help: ## This help.
	@awk 'BEGIN 	{ FS = ":.*##"; target="";printf "\nUsage:\n  make \033[36m<target>\033[33m\n\nTargets:\033[0m\n" } \
		/^[a-zA-Z_-]+:.*?##/ { if(target=="")print ""; target=$$1; printf " \033[36m%-10s\033[0m %s\n\n", $$1, $$2 } \
		/^([a-zA-Z_-]+):/ {if(target=="")print "";match($$0, "(.*):"); target=substr($$0,RSTART,RLENGTH) } \
		/^\t## (.*)/ { match($$0, "[^\t#:\\\\]+"); txt=substr($$0,RSTART,RLENGTH);printf " \033[36m%-10s\033[0m", target; printf " %s\n", txt ; target=""} \
		/^## .*/ {match($$0, "## (.+)$$"); txt=substr($$0,4,RLENGTH);printf "\n\033[33m%s\033[0m\n", txt ; target=""} \
	' $(MAKEFILE_LIST)

.PHONY: help clean start watch demo demo-reset
