PLIST_TEMPLATE := com.lockmacbybluetooth.zhouyh.plist.template
PLIST := com.lockmacbybluetooth.zhouyh.plist
SCRIPT := main.py

all: clean $(PLIST)

$(PLIST): $(PLIST_TEMPLATE)
	@sed "s|path/to/your/$(SCRIPT)|$(shell pwd)/$(SCRIPT)|g" $< > $@
	@cat $@

install: $(PLIST)
	cp $(PLIST) ~/Library/LaunchAgents/
	cat ~/Library/LaunchAgents/$(PLIST)
	launchctl load ~/Library/LaunchAgents/$(PLIST)
	launchctl list | grep $(PLIST)


uninstall:
	launchctl unload ~/Library/LaunchAgents/$(PLIST)
	rm ~/Library/LaunchAgents/$(PLIST)

clean:
	@-rm -f $(PLIST)

