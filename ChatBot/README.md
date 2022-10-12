# BullionBot Chat Bot

## This program serves as the backend for a simple chat bot that will help moderate Precious Metals sale groups running in Telegram.

### Features

#### General Commands
	+ /bin | Usage '/bin #' | Used to record a "bin" for a posted listing

#### Admin Commands (Only usable in DMs)
	+ /getBins | Usage  '/getBins' | Used to retrieve list of recorded bins (and wipe current list)
	+ /reloadConfig | Usage '/reloadConfig' | Used to relaod config.json
	+ /adminHelp | Usage '/adminHelp' | Display List of Admin Commands

####   Info Commands
	+ /team | Usage '/team' | Display Company Info
	+ /shipping | Usage '/shipping' | Display Shipping and Packing Info
	+ /payments | Usage '/payments' | Display Payment Method Info
	+ /help | Usage '/help' | Display List of General User Commands

#### Debug Commands
	+ /test | Usage '/test' | Posts standard form Test Item text and Image listing (one of each)
	+ /auth | Usage '/auth' | Prints Username and ID to console. Used for Getting values for the Whitelist (see SampleConfig.json)
	
### Notes

Info command outputs are not very general and will need to be changed for each group the bot is used in
