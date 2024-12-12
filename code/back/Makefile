# init back end
init-back:
	@python -m venv data-extraction/venv
	@echo "Please execute the following steps"
	@echo "> Active venv (depends on your system)"
	@echo "> exec : pip install -r data-extraction/requirements.txt"
	@echo "> exec : python -m spacy download fr_core_news_lg"
	@echo "> exec: pip install --upgrade transformers sentencepiece"
	@composer install
	@composer dumpautoload -o

# launch application back end
launch-back:
	php -S 127.0.0.1:8080 public/index.php