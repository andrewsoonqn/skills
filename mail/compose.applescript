-- Opens a pre-filled Mail.app compose window for review. Does NOT send.
-- Usage: osascript compose.applescript "<fromAddress>" "<toAddress>" "<subject>" "<body>"
-- from-address selects the account: e1375600@u.nus.edu (NUS) or andrewsoonqn@gmail.com (Gmail)
on run argv
	set theFrom to item 1 of argv
	set theTo to item 2 of argv
	set theSubject to item 3 of argv
	set theBody to item 4 of argv
	tell application "Mail"
		set newMsg to make new outgoing message with properties {subject:theSubject, content:theBody, visible:true}
		tell newMsg
			make new to recipient at end of to recipients with properties {address:theTo}
		end tell
		set sender of newMsg to theFrom
		activate
	end tell
end run
