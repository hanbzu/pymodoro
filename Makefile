# Makefile for Pymodoro

INSTALL_DIR=/usr/local/bin
LOCAL_DATA_DIR=~/.config/pymodoro

all: test

install:
	@echo "Installing Pymodoro to $(INSTALL_DIR)..."
	@sudo cp pymodoro.py $(INSTALL_DIR)/pymodoro
	@sudo chmod a+x $(INSTALL_DIR)/pymodoro
	@echo "Configuring user accout in $(LOCAL_DATA_DIR)..."
	@mkdir -p $(LOCAL_DATA_DIR)
	@cp -n config.json $(LOCAL_DATA_DIR)/
	@touch $(LOCAL_DATA_DIR)/history.csv
	@touch $(LOCAL_DATA_DIR)/fail.csv
	@touch $(LOCAL_DATA_DIR)/now.csv

test:
	@behave