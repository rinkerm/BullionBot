ma# BullionBot Chat Bot

## This program serves as the backend for a simple chat bot that will help moderate Precious Metals sale groups running in Telegram.

### Features

#### General Commands
	+ /bin | Usage '/bin #' | Used to record a "bin" for a posted listing
	+ /bin | Usage '/bin # /spot' | Used to record a "bin" for a posted listing and include spot price
	+ /spot | Usage '/spot' | Posts the KITCO spot prices

#### Admin Commands (Only usable in DMs)
	+ /getBins | Usage  '/getBins' | Used to retrieve list of recorded bins (and wipe current list)
	+ /reloadConfig | Usage '/reloadConfig' | Used to relaod config.json
	+ /adminHelp | Usage '/adminHelp' | Display List of Admin Commands

####   Info Commands
	+ /airtites | Usage '/airtites' | Post airtites info Image
	+ /buyback | Usage '/team' | Post buyback info Image
	+ /payments | Usage '/team' | Post payments info Image
	+ /policy | Usage '/team' | Post policy info Image
	+ /shipping | Usage '/team' | Post shipping info Image
	+ /team | Usage '/team' | Post team info Image
	+ /welcome | Usage '/welcome' | Post link to welcome message
	+ /help | Usage '/help' | Display List of General User Commands

#### Debug Commands
	+ /test | Usage '/test' | Posts standard form Test Item text and Image listing (one of each)
	+ /auth | Usage '/auth' | Prints Username and ID to console. Used for Getting values for the Whitelist (see SampleConfig.json)
	+ /debugGetBins | Usage '/debugGetBins' | Dumps Bin Log to Chat
	+ /get_reply_id| Usage '/get_reply_id' | Prints Message ID of the message being replied to
	+ /except | Usage '/except' | Raises a generic exception
	
### Notes

Info command outputs are images specified in config.json
