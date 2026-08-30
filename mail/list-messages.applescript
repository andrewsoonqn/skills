-- Usage: osascript list-messages.applescript "<accountName>" "<mailboxName>" <count>
-- Example: osascript list-messages.applescript "Exchange" "Inbox" 12
on run argv
	set acctName to item 1 of argv
	set mbName to item 2 of argv
	set maxN to (item 3 of argv) as integer
	tell application "Mail"
		set acc to first account whose name is acctName
		set mb to mailbox mbName of acc
		set n to count of messages of mb
		if n > maxN then set n to maxN
		set out to ""
		repeat with i from 1 to n
			set m to message i of mb
			set rs to read status of m
			set flag to "UNREAD"
			if rs then set flag to "read"
			set out to out & flag & " | " & (date received of m as string) & " | " & (sender of m) & " | " & (subject of m) & linefeed
		end repeat
		return out
	end tell
end run
