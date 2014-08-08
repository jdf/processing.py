-- A script to show dialogs if there are java problems
-- Run from main sketch script
on run argv
	set argtype to item 1 of argv
	set sketch_icon to POSIX file (item 2 of argv)
	if argtype is "nojava" then
		set dialog_result to display dialog "You don't have Java installed. This sketch won't work. Would you like to install Java?" with title "Sketchy Behavior" buttons {"Open download page", "Give up"} default button 1 with icon sketch_icon
		if button returned of dialog_result is "Open download page" then
			open location "https://java.com/en/download/"
		end if
	else if argtype is "oldjava" then
		set dialog_result to display dialog "You currently have Java 6 installed. Processing sketches won't work with Java versions less than 7. Would you like to download a more recent Java?" with title "Sketchy Behavior" buttons {"Open download page", "Give up"} default button 1 with icon sketch_icon
		set answer to button returned of dialog_result
		if answer is "Open download page" then
			open location "https://java.com/en/download/"
		end if
	else
		log "pass in the right arguments, please"
	end if
end run
